# -*- coding: utf-8 -*-
"""
ServerEvents - 网易基岩版
服务端事件由 server_system.py 桥接，此处保留业务逻辑接口。
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import logging

from progression.corruption_data import CorruptionData
from progression.corruption_stage import CorruptionStage
from network.corruption_sync_packet import CorruptionSyncPacket
from network.verity_network import VerityNetwork

_logger = logging.getLogger(__name__)


class ServerEvents(object):
    """服务端事件处理逻辑，由 VerityServerSystem 调用。"""

    _last_broadcast_level = -1

    @staticmethod
    def tick(corruption, scare, network):
        """每秒调用：推进腐化 + 广播 + 触发惊吓。"""
        before = corruption.get_level()
        corruption.tick_playtime()
        if corruption.get_level() != before:
            ServerEvents._broadcast_corruption(corruption, network)

    @staticmethod
    def _broadcast_corruption(corruption, network):
        if corruption.get_level() == ServerEvents._last_broadcast_level:
            return
        ServerEvents._last_broadcast_level = corruption.get_level()
        stage_idx = CorruptionStage.values().index(corruption.get_stage())
        pkt = CorruptionSyncPacket(corruption.get_level(), stage_idx)
        network.to_all(None, pkt.to_dict())

    @staticmethod
    def on_player_login(player_id, corruption, network):
        """玩家登录处理。"""
        stage_idx = CorruptionStage.values().index(corruption.get_stage())
        pkt = CorruptionSyncPacket(corruption.get_level(), stage_idx)
        network.to_player(player_id, pkt.to_dict())

    @staticmethod
    def on_player_logout(player_id, corruption):
        """玩家登出处理。"""
        pass

    @staticmethod
    def on_player_death(player_id, corruption):
        """玩家死亡处理。"""
        pass

    @staticmethod
    def reset_broadcast_cache():
        ServerEvents._last_broadcast_level = -1

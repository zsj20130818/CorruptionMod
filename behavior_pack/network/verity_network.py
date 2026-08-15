# -*- coding: utf-8 -*-
"""
网络通信适配 - 网易基岩版
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.server.extraServerApi as serverApi


class VerityNetwork(object):
    """网易 SDK 网络通信层，替代原 Forge PacketDistributor。"""

    @staticmethod
    def to_player(player, data):
        """发送数据包到单个玩家客户端。"""
        if hasattr(player, "id"):
            player_id = player.id
        elif isinstance(player, str):
            player_id = player
        else:
            player_id = str(player)
        event_name = data.get("event_name", "verity.generic")
        serverApi.NotifyToClient(player_id, event_name, data)

    @staticmethod
    def to_all(server, data):
        """广播数据包到所有在线玩家。"""
        event_name = data.get("event_name", "verity.generic")
        players = serverApi.GetPlayerList()
        for player_id in players:
            serverApi.NotifyToClient(player_id, event_name, data)

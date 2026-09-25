# -*- coding: utf-8 -*-
"""VerityCommand - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import math

import mod.server.extraServerApi as serverApi

from progression.corruption_data import CorruptionData
from progression.corruption_stage import CorruptionStage


class VerityCommand(object):
    """
    /verity 命令处理。
    网易基岩版通过监听聊天事件解析命令，非 Brigadier。
    实际命令路由在 server_system.py 中完成。
    """

    @staticmethod
    def register(server_system):
        """注册命令（网易基岩版无需显式注册，通过聊天监听实现）。"""
        pass

    @staticmethod
    def compass_direction(dx, dz):
        """计算罗盘方向字符串。"""
        if dx == 0 and dz == 0:
            return "here"
        angle = math.atan2(dz, dx) * 180.0 / math.pi
        if angle < 0:
            angle += 360.0
        directions = ["E", "SE", "S", "SW", "W", "NW", "N", "NE"]
        idx = int((angle + 22.5) / 45.0) % 8
        return directions[idx]

    @staticmethod
    def get_player_stage(player_id):
        data = CorruptionData.get()
        return data.get_stage()

    @staticmethod
    def get_player_corruption(player_id):
        data = CorruptionData.get()
        return data.get_level()


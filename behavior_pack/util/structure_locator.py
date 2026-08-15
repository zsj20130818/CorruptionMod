# -*- coding: utf-8 -*-
"""StructureLocator - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.server.extraServerApi as serverApi
import math


class StructureLocator(object):
    """结构定位器。"""

    @staticmethod
    def nearest_structure(level, origin, tag, radius=100):
        """查找最近的村庄/建筑。"""
        # TODO: 网易 SDK 结构查找 API
        # 返回 (x, y, z) 或 None
        return None

    @staticmethod
    def nearest_block(level, origin, block_tag, radius=24):
        """查找最近的方块（如矿石）。"""
        ox, oy, oz = int(origin[0]), int(origin[1]), int(origin[2])
        for x in range(ox - radius, ox + radius + 1):
            for y in range(oy - radius, oy + radius + 1):
                for z in range(oz - radius, oz + radius + 1):
                    # TODO: level.GetBlock(x, y, z)
                    pass
        return None

    @staticmethod
    def compass_direction(dx, dz):
        """罗盘方向。"""
        if dx == 0 and dz == 0:
            return "here"
        angle = math.atan2(dz, dx) * 180.0 / math.pi
        if angle < 0:
            angle += 360.0
        directions = ["E", "SE", "S", "SW", "W", "NW", "N", "NE"]
        idx = int((angle + 22.5) / 45.0) % 8
        return directions[idx]

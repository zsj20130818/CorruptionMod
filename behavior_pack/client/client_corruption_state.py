# -*- coding: utf-8 -*-
"""ClientCorruptionState - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class ClientCorruptionState(object):
    """客户端腐化状态镜像。"""

    def __init__(self):
        self._level = 0
        self._stage_index = 0

    def set(self, level, stage_index):
        self._level = level
        self._stage_index = stage_index

    def level(self):
        return self._level

    def stage_index(self):
        return self._stage_index

    def normalized(self):
        return min(1.0, self._level / 100.0)

    def tick(self):
        """客户端 tick（暂无逻辑）。"""
        pass

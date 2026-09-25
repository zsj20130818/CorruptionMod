# -*- coding: utf-8 -*-
"""
腐化值阶段 - 网易基岩版
"""

from __future__ import print_function, division, absolute_import, unicode_literals


class CorruptionStage(object):
    """
    5 个腐化阶段，替代原 Java enum。
    每个成员是 CorruptionStage 实例。
    """

    _all_stages = []
    __members__ = {}

    def __init__(self, name, threshold):
        self._name = name
        self._threshold = threshold

    def __eq__(self, other):
        if isinstance(other, CorruptionStage):
            return self._name == other._name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return "CorruptionStage(%s, %d)" % (self._name, self._threshold)

    @property
    def name(self):
        return self._name

    @property
    def threshold(self):
        return self._threshold

    def display_number(self):
        for i, s in enumerate(CorruptionStage._all_stages):
            if s == self:
                return i + 1
        return 1

    def is_horror(self):
        horror_start = CorruptionStage.PSYCHOLOGICAL
        for i, s in enumerate(CorruptionStage._all_stages):
            if s == self:
                return i >= 2
        return False

    @staticmethod
    def from_level(level):
        """根据腐化值返回对应阶段。"""
        result = CorruptionStage.FRIENDLY
        for stage in CorruptionStage._all_stages:
            if level >= stage._threshold:
                result = stage
        return result

    @staticmethod
    def values():
        return list(CorruptionStage._all_stages)

    @staticmethod
    def progress_within(level):
        """当前阶段内 0.0-1.0 进度。"""
        current = CorruptionStage.from_level(level)
        idx = CorruptionStage._all_stages.index(current)
        next_threshold = 100 if idx == len(CorruptionStage._all_stages) - 1 else CorruptionStage._all_stages[idx + 1]._threshold
        span = max(1, next_threshold - current._threshold)
        return min(1.0, float(level - current._threshold) / span)


# 实例化 5 个阶段
CorruptionStage.FRIENDLY = CorruptionStage("FRIENDLY", 0)
CorruptionStage.UNSETTLING = CorruptionStage("UNSETTLING", 20)
CorruptionStage.PSYCHOLOGICAL = CorruptionStage("PSYCHOLOGICAL", 40)
CorruptionStage.HOSTILE = CorruptionStage("HOSTILE", 70)
CorruptionStage.FINAL = CorruptionStage("FINAL", 90)

CorruptionStage._all_stages = [
    CorruptionStage.FRIENDLY,
    CorruptionStage.UNSETTLING,
    CorruptionStage.PSYCHOLOGICAL,
    CorruptionStage.HOSTILE,
    CorruptionStage.FINAL,
]

CorruptionStage.__members__ = {s._name: s for s in CorruptionStage._all_stages}

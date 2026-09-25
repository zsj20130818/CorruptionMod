# -*- coding: utf-8 -*-
"""
腐化值数据管理 - 网易基岩版
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import logging

from progression.corruption_stage import CorruptionStage

_logger = logging.getLogger(__name__)


class PlayerMemory(object):
    """Verity 对每个玩家的记忆。"""

    def __init__(self, name):
        self.name = name
        self.encounters = 0
        self.last_seen_tick = 0


class CorruptionData(object):
    """
    服务端全局腐化值真相源。
    替代原 Java SavedData，使用内存存储（网易基岩版无 NBT 持久化）。
    """

    BASE_RATE_PER_SECOND = 0.0025

    def __init__(self):
        self._level = 0
        self._accumulator = 0.0
        self._memory = {}
        self._boss_triggered = False
        self._rate_override = -1.0

    @staticmethod
    def get(level=None):
        """获取全局实例（单例模式）。"""
        if not hasattr(CorruptionData, "_instance"):
            CorruptionData._instance = CorruptionData()
        return CorruptionData._instance

    def tick_playtime(self):
        """每秒推进腐化值。"""
        self._accumulator += CorruptionData.BASE_RATE_PER_SECOND * self.get_effective_speed()
        self._flush_accumulator()

    def add_interaction(self, multiplier):
        """交互增加腐化值。"""
        self._accumulator += 0.05 * 1.0 * multiplier
        self._flush_accumulator()

    def _flush_accumulator(self):
        cap = 100
        while self._accumulator >= 1.0 and self._level < cap:
            self._accumulator -= 1.0
            self._level += 1

    def get_level(self):
        return self._level

    def set_level(self, value):
        self._level = max(0, min(100, value))
        self._accumulator = 0.0

    def get_stage(self):
        return CorruptionStage.from_level(self._level)

    def get_effective_speed(self):
        return self._rate_override if self._rate_override >= 0 else 1.0

    def has_rate_override(self):
        return self._rate_override >= 0

    def set_speed_multiplier(self, multiplier):
        self._rate_override = max(0.0, multiplier)

    def reset_rate(self):
        self._rate_override = -1.0

    def set_time_to_full(self, minutes):
        safe_minutes = max(0.1, minutes)
        self.set_speed_multiplier(100.0 / (CorruptionData.BASE_RATE_PER_SECOND * 60.0) / safe_minutes)

    def estimated_minutes_to_full(self):
        speed = self.get_effective_speed()
        if speed <= 0:
            return float("inf")
        return 100.0 / (CorruptionData.BASE_RATE_PER_SECOND * 60.0) / speed

    def is_at_final(self):
        return self._level >= 100

    def is_boss_triggered(self):
        return self._boss_triggered

    def set_boss_triggered(self, flag):
        self._boss_triggered = flag

    def remember(self, player_id, name=None):
        mem = self._memory.setdefault(player_id, PlayerMemory(name or "Player"))
        if name:
            mem.name = name
        return mem

    def get_memory(self, player_id):
        return self._memory.get(player_id)

    def record_encounter(self, player_id, name=None):
        mem = self.remember(player_id, name)
        mem.encounters += 1
        return mem

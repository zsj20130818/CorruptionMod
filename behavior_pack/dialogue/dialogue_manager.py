# -*- coding: utf-8 -*-
"""
DialogueManager - 网易基岩版
从 data/dialogue/*.json 加载对话池，支持加权随机 + 反重复 + 令牌替换。
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import json
import os
import random
import logging
from collections import deque

from dialogue.dialogue_entry import DialogueEntry

_logger = logging.getLogger(__name__)

# 阶段 → 对话池名映射
_POOL_MAP = {
    "FRIENDLY": "friendly",
    "UNSETTLING": "unsettling",
    "PSYCHOLOGICAL": "psychological",
    "HOSTILE": "hostile",
    "FINAL": "final",
}

RECENT_MEMORY = 5


class DialogueManager(object):
    """对话管理器：加载 JSON 对话池，按阶段选择回复。"""

    def __init__(self):
        self._pools = {}
        self._recent = {}
        self._load_all()

    def _load_all(self):
        base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dialogue")
        for stage_name, pool_name in _POOL_MAP.items():
            path = os.path.join(base, pool_name + ".json")
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                entries = [DialogueEntry.from_json(e) for e in data.get("entries", [])]
                self._pools[pool_name] = entries
            except (IOError, ValueError):
                self._pools[pool_name] = []
                _logger.warning("[Verity] Failed to load dialogue pool: %s", path)

    def pool_for(self, stage):
        name = stage.name if hasattr(stage, "name") else str(stage)
        pool_key = _POOL_MAP.get(name.upper(), "friendly")
        return pool_key

    def pick_for_stage(self, stage, player_name, encounters):
        """选择一条对话回复。"""
        pool_key = self.pool_for(stage)
        pool = self._pools.get(pool_key, [])
        if not pool:
            return "..."

        # 反重复过滤
        recent = self._recent.setdefault(pool_key, deque(maxlen=RECENT_MEMORY))
        candidates = [e for e in pool if e.text not in recent]
        if not candidates:
            candidates = pool

        # 加权随机
        total = sum(e.weight for e in candidates)
        roll = random.random() * total
        cumulative = 0
        chosen = candidates[0]
        for entry in candidates:
            cumulative += entry.weight
            if roll <= cumulative:
                chosen = entry
                break

        recent.append(chosen.text)

        # 令牌替换
        reply = chosen.text
        reply = reply.replace("{player}", player_name or "Player")
        reply = reply.replace("{encounters}", str(encounters))
        return reply

    def reload(self):
        """重新加载所有对话池。"""
        self._pools.clear()
        self._recent.clear()
        self._load_all()

# -*- coding: utf-8 -*-
"""
Verity API 模拟层 - 用于网易封闭环境的本地数据替代
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import json
import os
import random


class ApiMock(object):
    """伪 API - 替代外部 HTTP API，用于网易封闭环境。"""

    def __init__(self):
        self._base_dir = os.path.join(os.path.dirname(__file__), "data")
        self._dialogues = self._load_json(os.path.join(self._base_dir, "api_mock", "dialogues.json"), {})
        self._player_data = self._load_json(os.path.join(self._base_dir, "api_mock", "player_data.json"), {})
        self._leaderboard = self._load_json(os.path.join(self._base_dir, "api_mock", "leaderboard.json"), [])

    def _load_json(self, path, default):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (IOError, ValueError):
            return default

    def get_dialogue(self, key, **kwargs):
        pool = self._dialogues.get(key, ["..."])
        if isinstance(pool, list):
            return random.choice(pool)
        return pool

    def get_player_data(self, player_id):
        data = dict(self._player_data) if self._player_data else {}
        data["id"] = player_id
        data["name"] = "Player_" + str(player_id)[:4]
        data["level"] = random.randint(1, 20)
        return data

    def get_leaderboard(self, limit=10):
        return self._leaderboard[:limit] if self._leaderboard else []

    def post_event(self, event_data):
        return {"status": "success", "code": 200, "message": "Event received (mock)"}

    def post_corruption_event(self, event_type, data):
        return {"status": "received", "event_type": event_type, "data": data}

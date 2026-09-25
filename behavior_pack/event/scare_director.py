# -*- coding: utf-8 -*-
"""
ScareDirector - 网易基岩版
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import math
import random
import logging

import mod.server.extraServerApi as serverApi

from progression.corruption_data import CorruptionData
from progression.corruption_stage import CorruptionStage
from network.verity_network import VerityNetwork
from network.whisper_packet import WhisperPacket
from network.fake_chat_packet import FakeChatPacket
from network.hallucination_packet import HallucinationPacket
from network.screen_effect_packet import ScreenEffectPacket

_logger = logging.getLogger(__name__)


class _ScheduledTask(object):
    def __init__(self, run_at, action):
        self.run_at = run_at
        self.action = action


class ScareDirector(object):
    """Verity 的恐怖大脑 —— 按阶段触发惊吓事件。"""

    _random = random.Random()
    _last_scare_tick = 0
    _schedule = []

    _FAKE_NAMES = ["Player", "Steve", "Notch", "Herobrine", "null", "Verity", "you"]
    _FAKE_LINES = [
        "is anyone else seeing this?", "where did you go?", "don't turn around.",
        "i can see you.", "why is it so quiet?", "help", "behind you",
    ]

    @staticmethod
    def tick(players, data, network):
        now = serverApi.GetWorldTime()
        ScareDirector._run_due_tasks(now)

        if not players:
            return

        stage = data.get_stage()
        if stage == CorruptionStage.FRIENDLY:
            return

        cooldowns = {
            CorruptionStage.UNSETTLING: 600,
            CorruptionStage.PSYCHOLOGICAL: 400,
            CorruptionStage.HOSTILE: 240,
        }
        base_cd = cooldowns.get(stage, 200)
        if now - ScareDirector._last_scare_tick < base_cd:
            return

        if ScareDirector._random.random() > 0.6:
            return

        target = players[ScareDirector._random.randint(0, len(players) - 1)]
        ScareDirector._fire_scare(players, data, stage, target, network)
        ScareDirector._last_scare_tick = now

    @staticmethod
    def _fire_scare(players, data, stage, target, network):
        if stage == CorruptionStage.UNSETTLING:
            c = ScareDirector._random.randint(0, 2)
            if c == 0: ScareDirector._behind_you(target)
            elif c == 1: ScareDirector._whisper(target, 0, network)
            else: ScareDirector._stare(target)
        elif stage == CorruptionStage.PSYCHOLOGICAL:
            c = ScareDirector._random.randint(0, 5)
            if c == 0: ScareDirector._fake_chat(target, network)
            elif c == 1: ScareDirector._hallucination(target, network)
            elif c == 2: ScareDirector._whisper(target, ScareDirector._random.randint(0, 1), network)
            elif c == 3: ScareDirector._stare(target)
            elif c == 4: ScareDirector._door_scare(target)
            else: ScareDirector._screen_pulse(target, ScreenEffectPacket.VIGNETTE, 0.5, 30, network)
        elif stage == CorruptionStage.HOSTILE:
            c = ScareDirector._random.randint(0, 6)
            if c == 0: ScareDirector._hallucination(target, network)
            elif c == 1: ScareDirector._screen_pulse(target, ScreenEffectPacket.DISTORTION, 0.8, 60, network)
            elif c == 2: ScareDirector._screen_pulse(target, ScreenEffectPacket.GLITCH, 0.9, 25, network)
            elif c == 3: ScareDirector._whisper(target, 2, network)
            elif c == 4: ScareDirector._behind_you(target)
            elif c == 5: ScareDirector._fake_chat(target, network)
            else: ScareDirector._jumpscare(target, network)

    @staticmethod
    def _behind_you(player_id):
        pos = serverApi.GetPlayerPosition(player_id)
        if pos is None:
            return
        rot = serverApi.GetPlayerRotation(player_id)
        yaw = rot[1] if rot else 0
        dx = math.sin(yaw * math.pi / 180.0) * 2.5
        dz = -math.cos(yaw * math.pi / 180.0) * 2.5
        comp = serverApi.CreateComponent(player_id, "Minecraft", "Transform")
        if comp:
            comp.SetPosition(pos[0] + dx, pos[1], pos[2] + dz)

    @staticmethod
    def _stare(player_id):
        # TODO: 设置实体注视标志
        pass

    @staticmethod
    def _whisper(player_id, sound_id, network):
        pos = serverApi.GetPlayerPosition(player_id)
        if pos is None:
            return
        angle = ScareDirector._random.random() * math.pi * 2
        dist = 2.0 + ScareDirector._random.random() * 2.0
        x = pos[0] + math.cos(angle) * dist
        z = pos[2] + math.sin(angle) * dist
        pkt = WhisperPacket(x, pos[1] + 1, z, sound_id, 0.7, 0.9 + ScareDirector._random.random() * 0.2)
        network.to_player(player_id, pkt.to_dict())

    @staticmethod
    def _fake_chat(player_id, network):
        roll = ScareDirector._random.randint(0, 4)
        if roll == 0:
            pkt = FakeChatPacket(ScareDirector._random_name(), FakeChatPacket.JOIN)
        elif roll == 1:
            pkt = FakeChatPacket(ScareDirector._random_name(), FakeChatPacket.LEAVE)
        else:
            line = "<" + ScareDirector._random_name() + "> " + ScareDirector._FAKE_LINES[
                ScareDirector._random.randint(0, len(ScareDirector._FAKE_LINES) - 1)]
            pkt = FakeChatPacket(line, FakeChatPacket.CHAT)
        network.to_player(player_id, pkt.to_dict())

    @staticmethod
    def _hallucination(player_id, network):
        pos = serverApi.GetPlayerPosition(player_id)
        if pos is None:
            return
        angle = ScareDirector._random.random() * math.pi * 2
        dist = 6.0 + ScareDirector._random.random() * 6.0
        x = pos[0] + math.cos(angle) * dist
        z = pos[2] + math.sin(angle) * dist
        pkt = HallucinationPacket(x, pos[1], z, 60 + ScareDirector._random.randint(0, 59), 0)
        network.to_player(player_id, pkt.to_dict())

    @staticmethod
    def _door_scare(player_id):
        # TODO: 查找附近门并开/关
        pass

    @staticmethod
    def _jumpscare(player_id, network):
        ScareDirector._behind_you(player_id)
        pkt = ScreenEffectPacket(ScreenEffectPacket.JUMPSCARE, 1.0, 15)
        network.to_player(player_id, pkt.to_dict())

    @staticmethod
    def _screen_pulse(player_id, effect, intensity, duration, network):
        pkt = ScreenEffectPacket(effect, intensity, duration)
        network.to_player(player_id, pkt.to_dict())

    @staticmethod
    def _random_name():
        return ScareDirector._FAKE_NAMES[
            ScareDirector._random.randint(0, len(ScareDirector._FAKE_NAMES) - 1)]

    @staticmethod
    def _schedule_task(run_at, action):
        ScareDirector._schedule.append(_ScheduledTask(run_at, action))

    @staticmethod
    def _run_due_tasks(now):
        remaining = []
        for task in ScareDirector._schedule:
            if now >= task.run_at:
                try:
                    task.action()
                except Exception:
                    pass
            else:
                remaining.append(task)
        ScareDirector._schedule = remaining

    @staticmethod
    def reset():
        ScareDirector._schedule = []
        ScareDirector._last_scare_tick = 0
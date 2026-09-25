# -*- coding: utf-8 -*-
"""
音效注册 - 网易基岩版
"""

from __future__ import print_function, division, absolute_import, unicode_literals


class VeritySounds(object):
    """音效标识符常量，替代原 Forge DeferredRegister。"""

    VOICE_LETMEOUT = "verity.voice_letmeout"
    VOICE_GREETING = "verity.voice_greeting"
    VOICE_INTRO = "verity.voice_intro"

    AMBIENT_DRONE = "verity.ambient_drone"
    AMBIENT_DISTORTED = "verity.ambient_distorted"
    HEARTBEAT = "verity.heartbeat"
    GLITCH = "verity.glitch"
    WHISPER = "verity.whisper"

    BOSS_SPAWN = "verity.boss_spawn"
    BOSS_MUSIC = "verity.boss_music"
    JUMPSCARE_STINGER = "verity.jumpscare_stinger"

    @staticmethod
    def get_sound(name):
        return name

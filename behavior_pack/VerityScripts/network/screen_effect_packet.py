# -*- coding: utf-8 -*-
"""ScreenEffectPacket - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class ScreenEffectPacket(object):
    event_name = "verity.screen_effect"
    VIGNETTE = 0
    DISTORTION = 1
    GLITCH = 2
    JUMPSCARE = 3

    def __init__(self, effect, intensity, duration_ticks):
        self.effect = effect
        self.intensity = intensity
        self.duration_ticks = duration_ticks

    def to_dict(self):
        return {"event_name": self.event_name, "effect": self.effect,
                "intensity": self.intensity, "duration": self.duration_ticks}

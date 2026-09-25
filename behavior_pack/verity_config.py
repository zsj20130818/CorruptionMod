# -*- coding: utf-8 -*-
"""
Verity 配置 - 网易基岩版
"""

from __future__ import print_function, division, absolute_import, unicode_literals


class VerityConfig(object):
    """模组配置，替代原 ForgeConfigSpec。"""

    class SERVER(object):
        progression_enabled = True
        progression_speed = 1.0
        interaction_weight = 1.0
        starting_corruption = 0
        scare_frequency = 1.0
        enable_jumpscares = True
        enable_hallucinations = True
        enable_fake_chat = True
        enable_environment_scares = True
        enable_final_boss = True

    class CLIENT(object):
        screen_effect_intensity = 1.0
        horror_volume = 1.0
        enable_fog = True
        enable_screen_distortion = True

# -*- coding: utf-8 -*-
"""ScreenEffectHandler - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.client.extraClientApi as clientApi

from client.client_corruption_state import ClientCorruptionState


class ScreenEffectHandler(object):
    """客户端屏幕特效处理器。"""

    def __init__(self):
        self._active_effect = -1
        self._remaining_ticks = 0
        self._total_ticks = 1
        self._effect_intensity = 0.0

    def trigger(self, effect, intensity, duration_ticks):
        self._active_effect = effect
        self._effect_intensity = intensity
        self._remaining_ticks = duration_ticks
        self._total_ticks = max(1, duration_ticks)

        if effect == 3:  # JUMPSCARE
            clientApi.ShowScreenEffect("black_flash", intensity, duration_ticks)

    def tick(self):
        if self._remaining_ticks > 0:
            self._remaining_ticks -= 1
            if self._remaining_ticks <= 0:
                self._active_effect = -1
                self._effect_intensity = 0.0

        # 腐化雾效
        self._update_fog()

    def _update_fog(self):
        corruption = ClientCorruptionState().normalized()
        if corruption <= 0.01:
            return
        # TODO: 调用客户端渲染 API 调整雾距离
        # far_plane = max(6, vanilla_far * (1.0 - 0.6 * corruption))

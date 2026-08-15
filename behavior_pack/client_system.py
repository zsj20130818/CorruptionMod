# -*- coding: utf-8 -*-
"""
Verity 客户端系统 - 网易基岩版 ModSDK
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import logging

import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()

_logger = logging.getLogger(__name__)


class VerityClientSystem(ClientSystem):
    """
    客户端主系统 —— 接收服务端网络包，驱动客户端视觉效果。
    """

    def __init__(self, namespace, system_name):
        super(VerityClientSystem, self).__init__(namespace, system_name)

        # 客户端腐化状态
        self._corruption_level = 0
        self._stage_index = 0
        self._stage_names = ["Friendly", "Unsettling", "Psychological", "Hostile", "Final"]

        # 屏幕特效状态
        self._active_effect = -1
        self._effect_intensity = 0.0
        self._effect_remaining = 0
        self._effect_total = 1

        # 注册事件
        self._register_events()

        _logger.info("[Verity] Client system initialized.")

    def _register_events(self):
        """注册客户端事件监听。"""
        self.ListenForEvent(
            clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),
            "OnClientTick", self, self._on_tick
        )
        # 注册自定义网络事件
        self.ListenForEvent(
            "VerityMod", "VerityServerSystem",
            "verity.corruption_sync", self, self._on_corruption_sync
        )
        self.ListenForEvent(
            "VerityMod", "VerityServerSystem",
            "verity.system_message", self, self._on_system_message
        )
        self.ListenForEvent(
            "VerityMod", "VerityServerSystem",
            "verity.screen_effect", self, self._on_screen_effect
        )
        self.ListenForEvent(
            "VerityMod", "VerityServerSystem",
            "verity.fake_chat", self, self._on_fake_chat
        )
        self.ListenForEvent(
            "VerityMod", "VerityServerSystem",
            "verity.hallucination", self, self._on_hallucination
        )
        self.ListenForEvent(
            "VerityMod", "VerityServerSystem",
            "verity.whisper", self, self._on_whisper
        )

    # -----------------------------------------------------------------------
    # 客户端 tick
    # -----------------------------------------------------------------------

    def _on_tick(self, args):
        """每 tick 调用，处理特效衰减。"""
        if self._effect_remaining > 0:
            self._effect_remaining -= 1
            if self._effect_remaining <= 0:
                self._active_effect = -1
                self._effect_intensity = 0.0

        # 根据腐化等级渲染雾效
        self._update_fog()

    def _update_fog(self):
        """根据腐化值更新雾密度。"""
        if self._corruption_level <= 1:
            return
        normalized = min(1.0, self._corruption_level / 100.0)
        # TODO: 调用客户端渲染 API 设置雾距离
        # 网易 SDK: clientApi.GetEngineCompFactory().CreateEngine fog
        # far_plane = max(6, vanilla_far * (1.0 - 0.6 * normalized))

    # -----------------------------------------------------------------------
    # 网络包处理
    # -----------------------------------------------------------------------

    def _on_corruption_sync(self, data):
        """腐化值同步。"""
        self._corruption_level = data.get("level", 0)
        self._stage_index = data.get("stage", 0)
        _logger.info("[Verity] Corruption synced: %d/100, stage=%s",
                     self._corruption_level, self._stage_names[self._stage_index])

    def _on_system_message(self, data):
        """系统消息显示。"""
        msg = data.get("msg", "")
        if msg:
            clientApi.ShowChatMsg(msg)

    def _on_screen_effect(self, data):
        """屏幕特效。"""
        effect = data.get("effect", 0)
        intensity = data.get("intensity", 1.0)
        duration = data.get("duration", 20)
        self._active_effect = effect
        self._effect_intensity = intensity
        self._effect_remaining = duration
        self._effect_total = duration

        # 跳脸特效：全屏闪黑
        if effect == 3:  # JUMPSCARE
            clientApi.ShowScreenEffect("black_flash", intensity, duration)

    def _on_fake_chat(self, data):
        """假聊天/加入/离开消息。"""
        text = data.get("text", "")
        kind = data.get("kind", 0)
        if kind == 1:  # JOIN
            clientApi.ShowChatMsg("[+] " + text + " joined the game")
        elif kind == 2:  # LEAVE
            clientApi.ShowChatMsg("[-] " + text + " left the game")
        else:
            clientApi.ShowChatMsg(text)

    def _on_hallucination(self, data):
        """客户端幻觉实体生成。"""
        x = data.get("x", 0)
        y = data.get("y", 64)
        z = data.get("z", 0)
        lifespan = data.get("lifespan", 100)
        # TODO: 在客户端生成幻觉实体
        # clientApi.SpawnClientEntity("verity:hallucination", (x, y, z))

    def _on_whisper(self, data):
        """定位低语音效。"""
        x = data.get("x", 0)
        y = data.get("y", 64)
        z = data.get("z", 0)
        sound_id = data.get("soundId", 0)
        volume = data.get("volume", 0.7)
        pitch = data.get("pitch", 1.0)
        # TODO: 播放定位音效
        # clientApi.PlayLocalSound(sound_name, volume, pitch, (x, y, z))

    # -----------------------------------------------------------------------
    # 公开接口
    # -----------------------------------------------------------------------

    def get_corruption_level(self):
        return self._corruption_level

    def get_stage_name(self):
        if 0 <= self._stage_index < len(self._stage_names):
            return self._stage_names[self._stage_index]
        return "Unknown"

    def Destroy(self):
        """系统销毁。"""
        pass

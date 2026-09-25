# -*- coding: utf-8 -*-
"""ClientPacketHandlers - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.client.extraClientApi as clientApi

from client.client_corruption_state import ClientCorruptionState
from registry.verity_sounds import VeritySounds


class ClientPacketHandlers(object):
    """客户端网络包处理器。"""

    _fake_id = -2000000

    @staticmethod
    def on_corruption_sync(data):
        ClientCorruptionState().set(data.get("level", 0), data.get("stage", 0))

    @staticmethod
    def on_screen_effect(data):
        effect = data.get("effect", 0)
        intensity = data.get("intensity", 1.0)
        duration = data.get("duration", 20)
        if intensity <= 0:
            return
        # TODO: 调用客户端屏幕特效 API
        if effect == 3:  # JUMPSCARE
            clientApi.ShowScreenEffect("black_flash", intensity, duration)

    @staticmethod
    def on_hallucination(data):
        x = data.get("x", 0)
        y = data.get("y", 64)
        z = data.get("z", 0)
        # TODO: 客户端生成幻觉实体
        pass

    @staticmethod
    def on_fake_chat(data):
        text = data.get("text", "")
        kind = data.get("kind", 0)
        if kind == 1:
            clientApi.ShowChatMsg("[+] " + text + " joined the game")
        elif kind == 2:
            clientApi.ShowChatMsg("[-] " + text + " left the game")
        else:
            clientApi.ShowChatMsg(text)

    @staticmethod
    def on_whisper(data):
        x = data.get("x", 0)
        y = data.get("y", 64)
        z = data.get("z", 0)
        sound_id = data.get("soundId", 0)
        volume = data.get("volume", 0.7)
        # TODO: 播放定位音效
        pass

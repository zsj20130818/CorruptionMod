# -*- coding: utf-8 -*-
"""VeritySpeech - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.server.extraServerApi as serverApi

from registry.verity_sounds import VeritySounds


class VeritySpeech(object):
    """Verity 说话工具：发送聊天行 + 播放语音。"""

    @staticmethod
    def speak(player_id, text, is_horror=False):
        """发送聊天消息给玩家并播放语音。"""
        prefix = "[Verity] "
        serverApi.NotifyToClient(player_id, "verity.system_message", {"msg": prefix + text})

    @staticmethod
    def lookup_sound(name):
        """按名称查找音效。"""
        return "verity." + name

# -*- coding: utf-8 -*-
"""VerityKeybinds - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.client.extraClientApi as clientApi

from client.verity_chat_screen import VerityChatScreen


class VerityKeybinds(object):
    """按键绑定 —— 打开 Ask Verity 屏幕。"""

    ASK_KEY = "V"

    def __init__(self):
        self._chat_screen = VerityChatScreen()

    def on_key_press(self, key):
        """按键回调。"""
        if key == self.ASK_KEY:
            self._chat_screen.show()

    def register(self):
        """注册按键（网易 SDK 通过客户端系统注册）。"""
        pass

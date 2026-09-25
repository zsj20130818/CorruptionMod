# -*- coding: utf-8 -*-
"""VerityChatScreen - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import mod.client.extraClientApi as clientApi


class VerityChatScreen(object):
    """Ask Verity 屏幕 —— 网易基岩版 UI。"""

    def __init__(self):
        self._text = ""

    def show(self):
        """显示聊天输入界面。"""
        # TODO: 调用网易 SDK 创建 UI 面板
        # clientApi.CreateUI("verity_chat_screen", layout_json)
        pass

    def send(self, text):
        """发送问题到服务端。"""
        text = (text or "").strip()
        if not text:
            return
        # 通过网络发送到服务端
        import mod.client.extraClientApi as ca
        ca.NotifyToServer("verity.ask_question", {"question": text})
        self.close()

    def close(self):
        """关闭界面。"""
        # TODO: 关闭 UI 面板
        pass

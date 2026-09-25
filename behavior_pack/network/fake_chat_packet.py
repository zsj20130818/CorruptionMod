# -*- coding: utf-8 -*-
"""FakeChatPacket - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class FakeChatPacket(object):
    event_name = "verity.fake_chat"
    CHAT = 0
    JOIN = 1
    LEAVE = 2

    def __init__(self, text, kind):
        self.text = text
        self.kind = kind

    def to_dict(self):
        return {"event_name": self.event_name, "text": self.text, "kind": self.kind}

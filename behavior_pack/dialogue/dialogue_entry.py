# -*- coding: utf-8 -*-
"""DialogueEntry - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class DialogueEntry(object):
    """单条对话条目。"""

    def __init__(self, text, weight=1, voice="", emotion="CALM"):
        self.text = text
        self.weight = max(1, weight)
        self.voice = voice
        self.emotion = emotion

    @staticmethod
    def from_json(obj):
        return DialogueEntry(
            text=obj.get("text", ""),
            weight=obj.get("weight", 1),
            voice=obj.get("voice", ""),
            emotion=obj.get("emotion", "CALM"),
        )

    def to_dict(self):
        return {"text": self.text, "weight": self.weight,
                "voice": self.voice, "emotion": self.emotion}

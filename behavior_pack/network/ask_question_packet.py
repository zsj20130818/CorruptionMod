# -*- coding: utf-8 -*-
"""AskQuestionPacket - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class AskQuestionPacket(object):
    event_name = "verity.ask_question"

    def __init__(self, question):
        self.question = question

    def to_dict(self):
        return {"event_name": self.event_name, "question": self.question}

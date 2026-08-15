# -*- coding: utf-8 -*-
"""CorruptionSyncPacket - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class CorruptionSyncPacket(object):
    event_name = "verity.corruption_sync"

    def __init__(self, level, stage):
        self.level = level
        self.stage = stage

    def to_dict(self):
        return {"event_name": self.event_name, "level": self.level, "stage": self.stage}

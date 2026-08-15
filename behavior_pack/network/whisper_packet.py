# -*- coding: utf-8 -*-
"""WhisperPacket - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class WhisperPacket(object):
    event_name = "verity.whisper"

    def __init__(self, x, y, z, sound_id, volume, pitch):
        self.x = x
        self.y = y
        self.z = z
        self.sound_id = sound_id
        self.volume = volume
        self.pitch = pitch

    def to_dict(self):
        return {"event_name": self.event_name, "x": self.x, "y": self.y,
                "z": self.z, "soundId": self.sound_id,
                "volume": self.volume, "pitch": self.pitch}

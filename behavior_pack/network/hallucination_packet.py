# -*- coding: utf-8 -*-
"""HallucinationPacket - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class HallucinationPacket(object):
    event_name = "verity.hallucination"

    def __init__(self, x, y, z, lifespan, variant):
        self.x = x
        self.y = y
        self.z = z
        self.lifespan = lifespan
        self.variant = variant

    def to_dict(self):
        return {"event_name": self.event_name, "x": self.x, "y": self.y,
                "z": self.z, "lifespan": self.lifespan, "variant": self.variant}

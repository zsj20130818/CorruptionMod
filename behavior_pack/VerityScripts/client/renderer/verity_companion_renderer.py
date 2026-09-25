# -*- coding: utf-8 -*-
"""VerityCompanionRenderer - 网易基岩版（渲染由 entity.json 定义）"""

from __future__ import print_function, division, absolute_import, unicode_literals


class VerityCompanionRenderer(object):
    """伙伴渲染器 —— 网易基岩版通过 resource_pack/entity/ 定义。"""

    @staticmethod
    def get_texture_for_stage(smile_state):
        if hasattr(smile_state, "texture"):
            return smile_state.texture
        return "textures/entity/verity_smile_normal.png"

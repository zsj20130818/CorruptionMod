# -*- coding: utf-8 -*-
"""ClientSetup - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals


class ClientSetup(object):
    """客户端初始化设置。"""

    @staticmethod
    def on_client_setup():
        """客户端启动时的初始化。"""
        pass

    @staticmethod
    def on_register_renderers():
        """注册实体渲染器（网易基岩版通过 entity.json 定义）。"""
        pass

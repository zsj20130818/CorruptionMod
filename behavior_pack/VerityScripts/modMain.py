# -*- coding: utf-8 -*-
"""
Verity 模组 - 网易基岩版入口
"""

import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from mod.common.mod import Mod


@Mod.Binding(name="VerityMod", version="1.0.0")
class VerityMod(object):
    def __init__(self):
        pass

    @Mod.InitServer()
    def init_server(self):
        from server_system import VerityServerSystem
        serverApi.RegisterSystem("VerityMod", "VerityServerSystem", "server_system.VerityServerSystem")

    @Mod.InitClient()
    def init_client(self):
        from client_system import VerityClientSystem
        clientApi.RegisterSystem("VerityMod", "VerityClientSystem", "client_system.VerityClientSystem")

    @Mod.DestroyServer()
    def destroy_server(self):
        pass

    @Mod.DestroyClient()
    def destroy_client(self):
        pass
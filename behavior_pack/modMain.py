# -*- coding: utf-8 -*-
"""
Verity 模组 - 网易基岩版入口
"""

import sys
import os

# 获取 behavior_pack/ 根目录
base_dir = os.path.dirname(__file__)

# 把根目录加入搜索路径
sys.path.insert(0, base_dir)

# 把所有子目录也加入搜索路径
sub_dirs = ["event", "network", "progression", "dialogue", "command", "registry", "client"]
for sub in sub_dirs:
    sub_path = os.path.join(base_dir, sub)
    if os.path.exists(sub_path):
        sys.path.insert(0, sub_path)

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
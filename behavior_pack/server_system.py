# -*- coding: utf-8 -*-
"""
Verity 服务端系统 - 网易基岩版 ModSDK
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import json
import os
import random
import logging
import math  # ✅ 添加 math 导入（原代码里用了但没导入）

import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 从业务包导入
# ---------------------------------------------------------------------------
from progression.corruption_data import CorruptionData
from progression.corruption_stage import CorruptionStage
from event.scare_director import ScareDirector
from event.server_events import ServerEvents
from command.verity_command import VerityCommand
from dialogue.dialogue_manager import DialogueManager
from network.verity_network import VerityNetwork
from registry.verity_items import VerityItems
from registry.verity_sounds import VeritySounds
from item.verity_box_item import VerityBoxItem


class VerityServerSystem(ServerSystem):
    """
    服务端主系统 —— 桥接网易 MC 事件到 Verity 业务逻辑。
    """

    def __init__(self, namespace, system_name):
        super(VerityServerSystem, self).__init__(namespace, system_name)

        # ---- 仅声明属性，不执行任何业务逻辑 ----
        # 业务实例在 OnWorldReady 中创建
        self._corruption = None
        self._scare = None
        self._dialogue = None
        self._network = None
        self._companions = {}
        self._tick_counter = 0
        self._dialogue_pools = {}
        self._world_ready = False

        # 引擎事件监听可以在 __init__ 中注册（仅注册，不执行业务）
        self._register_events()

        _logger.info("[Verity] Server system __init__ done (deferred init pending).")

    # -----------------------------------------------------------------------
    # 世界就绪回调 —— 真正的业务初始化
    # -----------------------------------------------------------------------

    def OnWorldReady(self, args=None):
        """世界加载完成后执行真正的业务初始化。

        在 __init__ 阶段，世界尚未加载完成，get_world_record 返回 None，
        global_chat_mgr 等管理器也不可用。所有依赖这些的代码必须在此执行。
        """
        if self._world_ready:
            return
        self._world_ready = True

        # 创建业务实例
        self._corruption = CorruptionData()
        self._scare = ScareDirector()
        self._dialogue = DialogueManager()
        self._network = VerityNetwork()

        # 加载对话池（依赖文件系统，确保世界目录已就绪）
        self._load_dialogue_pools()

        # ✅ 注册 /verity 命令
        self._register_commands()

        # ✅ 注册 Verity 物品
        self._register_items()

        _logger.info("[Verity] Server system fully initialized (world ready).")

    # -----------------------------------------------------------------------
    # 命令注册
    # -----------------------------------------------------------------------

    def _register_commands(self):
        """注册自定义命令到网易游戏。"""
        try:
            # 方法1：尝试使用网易的 RegisterCommand API
            serverApi.RegisterCommand("/verity", self._on_command_callback, "Verity mod commands")
            _logger.info("[Verity] Command /verity registered via RegisterCommand.")
        except AttributeError:
            # 方法2：如果 RegisterCommand 不存在，使用监听聊天事件的方式（已通过 ServerChatEvent 实现）
            _logger.info("[Verity] RegisterCommand not available, using ServerChatEvent fallback.")

    def _on_command_callback(self, args):
        """RegisterCommand 的回调函数。"""
        if not self._world_ready:
            return
        # args 可能包含 playerId, command, args 等字段
        player_id = args.get("playerId", args.get("player_id", ""))
        message = args.get("command", args.get("message", ""))
        if player_id and message:
            self._handle_verity_command(player_id, message)

    # -----------------------------------------------------------------------
    # 物品注册
    # -----------------------------------------------------------------------

    def _register_items(self):
        """注册 Verity 物品（仅创造模式可见的生物蛋）。"""
        level_id = serverApi.GetLevelId()
        if level_id is None:
            _logger.warning("[Verity] level id is None, item registration skipped.")
            return
        comp = serverApi.CreateComponent(level_id, "Minecraft", "Item")
        if comp is None:
            _logger.warning("[Verity] Failed to get Item component, item registration skipped.")
            return

        comp.RegisterItem(
            VerityItems.VERITY_BOX,
            {
                "item_name": "Verity 生物蛋",
                "category": "items",
                "max_stack_count": 64,
                "creative_category": "items",
                "creative_group": "itemGroup.name.items",
            }
        )

        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "ServerItemUseOnEvent", self, self._on_item_use
        )
        _logger.info("[Verity] Item %s registered.", VerityItems.VERITY_BOX)

    def _on_item_use(self, args):
        """玩家使用物品时触发。"""
        player_id = args.get("playerId", "")
        item_name = args.get("itemName", "")
        if item_name != VerityItems.VERITY_BOX:
            return
        if not self._world_ready:
            self._send_message(player_id, "[Verity] World not ready yet.")
            return

        dimension = args.get("dimensionId", 0)
        result = VerityBoxItem.use(player_id, dimension)
        if result:
            inv_comp = serverApi.CreateComponent(player_id, "Minecraft", "Inventory")
            if inv_comp:
                try:
                    inv_comp.DecreaseItemCount(VerityItems.VERITY_BOX, 1, 0, True)
                except Exception:
                    pass

    # -----------------------------------------------------------------------
    # 对话池加载
    # -----------------------------------------------------------------------

    def _load_dialogue_pools(self):
        """从 data/dialogue/*.json 加载对话池。"""
        base = os.path.join(os.path.dirname(__file__), "data", "dialogue")
        pools = ["friendly", "unsettling", "psychological", "hostile", "final"]
        for name in pools:
            path = os.path.join(base, name + ".json")
            try:
                with open(path, "r") as f:
                    self._dialogue_pools[name] = json.load(f)
            except (IOError, ValueError):
                self._dialogue_pools[name] = {"entries": []}
                _logger.warning("[Verity] Failed to load dialogue pool: %s", path)

    # -----------------------------------------------------------------------
    # 事件注册
    # -----------------------------------------------------------------------

    def _register_events(self):
        """注册网易引擎事件监听（仅注册回调，不执行业务逻辑）。"""
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "OnServerTick", self, self._on_tick
        )
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "AddServerPlayerEvent", self, self._on_player_join
        )
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "DelServerPlayerEvent", self, self._on_player_leave
        )
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "ServerChatEvent", self, self._on_chat
        )
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "EntityDieEvent", self, self._on_entity_die
        )
        # 监听世界就绪事件
        self.ListenForEvent(
            serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
            "OnWorldReady", self, self.OnWorldReady
        )

    # -----------------------------------------------------------------------
    # 引擎事件 → 业务逻辑桥接
    # -----------------------------------------------------------------------

    def _on_tick(self, args):
        """每 tick 调用，每秒（20 tick）执行一次业务逻辑。"""
        if not self._world_ready:
            return
        self._tick_counter += 1
        if self._tick_counter < 20:
            return
        self._tick_counter = 0

        # 推进腐化值
        self._corruption.tick_playtime()

        # 广播腐化值变化
        level = self._corruption.get_level()
        stage = self._corruption.get_stage()
        stage_idx = self._stage_to_index(stage)
        self._network.to_all(None, {
            "event_name": "verity.corruption_sync",
            "level": level,
            "stage": stage_idx
        })

        # 惊吓导演 tick
        players = serverApi.GetPlayerList()
        if players:
            self._scare.tick(players, self._corruption, self._network)

    def _on_player_join(self, args):
        """玩家加入服务器。"""
        if not self._world_ready:
            return
        player_id = args.get("id", args.get("playerId", ""))
        if not player_id:
            return

        # 同步当前腐化值
        level = self._corruption.get_level()
        stage_idx = self._stage_to_index(self._corruption.get_stage())
        self._network.to_player(player_id, {
            "event_name": "verity.corruption_sync",
            "level": level,
            "stage": stage_idx
        })

        # 首次登录发盒子
        self._give_box_if_first_time(player_id)

    def _on_player_leave(self, args):
        """玩家离开服务器。"""
        if not self._world_ready:
            return
        player_id = args.get("id", args.get("playerId", ""))
        if player_id in self._companions:
            entity_id = self._companions.pop(player_id)
            serverApi.DestroyEntity(entity_id)

    def _on_chat(self, args):
        """聊天消息处理：/verity 命令 + @Verity 对话。"""
        if not self._world_ready:
            return
        player_id = args.get("playerId", args.get("player_id", ""))
        message = args.get("message", "")

        if message.startswith("/verity"):
            self._handle_verity_command(player_id, message)
        elif message.startswith("@Verity") or message.startswith("@verity"):
            question = message[7:].strip()
            self._handle_verity_dialogue(player_id, question)

    def _on_entity_die(self, args):
        """实体死亡事件。"""
        if not self._world_ready:
            return
        entity_id = args.get("entityId", "")
        # 如果是 Boss 死亡，可以触发胜利逻辑
        for pid, eid in list(self._companions.items()):
            if eid == entity_id:
                del self._companions[pid]
                break

    # -----------------------------------------------------------------------
    # /verity 命令处理
    # -----------------------------------------------------------------------

    def _handle_verity_command(self, player_id, message):
        parts = message.split()
        if len(parts) < 2:
            self._send_message(player_id, "Usage: /verity <summon|dismiss|status|ask|corruption|reset|event>")
            return

        cmd = parts[1].lower()

        if cmd == "summon":
            self._cmd_summon(player_id)
        elif cmd == "dismiss":
            self._cmd_dismiss(player_id)
        elif cmd == "status":
            self._cmd_status(player_id)
        elif cmd == "ask":
            question = " ".join(parts[2:]) if len(parts) > 2 else ""
            self._cmd_ask(player_id, question)
        elif cmd == "corruption":
            self._cmd_corruption(player_id, parts)
        elif cmd == "reset":
            self._cmd_reset(player_id)
        elif cmd == "event":
            self._cmd_event(player_id, parts)
        else:
            self._send_message(player_id, "Unknown command: " + cmd)

    def _cmd_summon(self, player_id):
        """召唤 Verity 伙伴。"""
        if player_id in self._companions:
            self._send_message(player_id, "Verity is already with you.")
            return
        pos = serverApi.GetPlayerPosition(player_id)
        if pos is None:
            return
        # 玩家面前 2 格
        rot = serverApi.GetPlayerRotation(player_id)
        yaw = rot[1] if rot else 0
        dx = -math.sin(yaw * 3.14159 / 180.0) * 2.0
        dz = math.cos(yaw * 3.14159 / 180.0) * 2.0
        spawn_pos = (pos[0] + dx, pos[1] + 1.5, pos[2] + dz)
        entity_id = serverApi.CreateEntity("verity:companion", spawn_pos, (0, yaw))
        if entity_id:
            self._companions[player_id] = entity_id
            self._send_message(player_id, "Verity has appeared.")

    def _cmd_dismiss(self, player_id):
        """让 Verity 离开。"""
        if player_id in self._companions:
            entity_id = self._companions.pop(player_id)
            serverApi.DestroyEntity(entity_id)
            self._send_message(player_id, "Verity has departed.")
        else:
            self._send_message(player_id, "Verity is not here.")

    def _cmd_status(self, player_id):
        """显示腐化值和阶段。"""
        level = self._corruption.get_level()
        stage = self._corruption.get_stage()
        stage_name = self._stage_name(stage)
        self._send_message(player_id, "Corruption: %d/100 - Stage: %s" % (level, stage_name))

    def _cmd_ask(self, player_id, question):
        """向 Verity 提问。"""
        if not question:
            self._send_message(player_id, "Usage: /verity ask <question>")
            return
        self._handle_verity_dialogue(player_id, question)

    def _cmd_corruption(self, player_id, parts):
        """设置腐化值（OP only）。"""
        perm = serverApi.GetPlayerPermission(player_id)
        if perm < 2:
            self._send_message(player_id, "You don't have permission.")
            return
        if len(parts) < 3:
            self._send_message(player_id, "Usage: /verity corruption <0-100>")
            return
        try:
            value = int(parts[2])
        except ValueError:
            self._send_message(player_id, "Invalid number.")
            return
        self._corruption.set_level(value)
        self._send_message(player_id, "Corruption set to %d." % value)

    def _cmd_reset(self, player_id):
        """重置所有进度（OP only）。"""
        perm = serverApi.GetPlayerPermission(player_id)
        if perm < 2:
            self._send_message(player_id, "You don't have permission.")
            return
        self._corruption.set_level(0)
        self._corruption.set_boss_triggered(False)
        self._corruption.reset_rate()
        # 解散所有伙伴
        for pid, eid in list(self._companions.items()):
            serverApi.DestroyEntity(eid)
        self._companions.clear()
        self._send_message(player_id, "Verity progress reset.")

    def _cmd_event(self, player_id, parts):
        """强制触发事件（OP only）。"""
        perm = serverApi.GetPlayerPermission(player_id)
        if perm < 2:
            self._send_message(player_id, "You don't have permission.")
            return
        if len(parts) < 3:
            self._send_message(player_id, "Usage: /verity event <scare|boss>")
            return
        evt = parts[2].lower()
        if evt == "scare":
            players = serverApi.GetPlayerList()
            if players:
                self._scare._fire_scare(players, self._corruption,
                                        self._corruption.get_stage(), players[0])
        elif evt == "boss":
            self._spawn_boss(player_id)
        else:
            self._send_message(player_id, "Unknown event: " + evt)

    # -----------------------------------------------------------------------
    # @Verity 对话处理
    # -----------------------------------------------------------------------

    def _handle_verity_dialogue(self, player_id, question):
        """处理玩家提问，返回对话回复。"""
        # 增加交互腐化值
        self._corruption.add_interaction(1.0)

        # 获取阶段对应的对话池
        stage = self._corruption.get_stage()
        pool_name = self._stage_to_pool(stage)
        pool = self._dialogue_pools.get(pool_name, {})
        entries = pool.get("entries", [])

        if not entries:
            self._send_message(player_id, "Verity looks at you silently.")
            return

        # 加权随机选择
        total_weight = sum(e.get("weight", 1) for e in entries)
        roll = random.random() * total_weight
        cumulative = 0
        reply = entries[0].get("text", "...")
        for entry in entries:
            cumulative += entry.get("weight", 1)
            if roll <= cumulative:
                reply = entry.get("text", "...")
                break

        # 替换 {player} 令牌
        player_name = serverApi.GetPlayerName(player_id) or "Player"
        reply = reply.replace("{player}", player_name)

        # 发送回复
        self._send_message(player_id, "[Verity] " + reply)

    # -----------------------------------------------------------------------
    # Boss 生成
    # -----------------------------------------------------------------------

    def _spawn_boss(self, player_id):
        """在玩家附近生成 Boss。"""
        pos = serverApi.GetPlayerPosition(player_id)
        if pos is None:
            return
        # 玩家前方 8 格
        rot = serverApi.GetPlayerRotation(player_id)
        yaw = rot[1] if rot else 0
        dx = -math.sin(yaw * 3.14159 / 180.0) * 8.0
        dz = math.cos(yaw * 3.14159 / 180.0) * 8.0
        spawn_pos = (pos[0] + dx, pos[1] + 1.0, pos[2] + dz)
        entity_id = serverApi.CreateEntity("verity:boss", spawn_pos, (0, yaw + 180))
        if entity_id:
            self._corruption.set_boss_triggered(True)
            self._send_message(player_id, "Verity is here.")

    # -----------------------------------------------------------------------
    # 首次盒子发放
    # -----------------------------------------------------------------------

    def _give_box_if_first_time(self, player_id):
        """首次登录给玩家发 Verity Box。"""
        # 网易 SDK: 通过玩家背包组件添加物品
        comp = serverApi.CreateComponent(player_id, "Minecraft", "Inventory")
        if comp is None:
            return
        # TODO: 检查是否已发过（需要持久化存储）
        # comp.AddItemToInventory("verity:box", 1)
        self._send_message(player_id, "You received a Verity Box.")

    # -----------------------------------------------------------------------
    # 辅助方法
    # -----------------------------------------------------------------------

    def _send_message(self, player_id, text):
        """发送系统消息给玩家。"""
        serverApi.NotifyToClient(player_id, "verity.system_message", {"msg": text})

    def _stage_to_index(self, stage):
        """CorruptionStage 实例 → 索引。"""
        stages = [CorruptionStage.FRIENDLY, CorruptionStage.UNSETTLING,
                  CorruptionStage.PSYCHOLOGICAL, CorruptionStage.HOSTILE,
                  CorruptionStage.FINAL]
        try:
            return stages.index(stage)
        except ValueError:
            return 0

    def _stage_name(self, stage):
        """获取阶段显示名。"""
        if hasattr(stage, "_name"):
            return stage._name
        return str(stage)

    def _stage_to_pool(self, stage):
        """阶段 → 对话池名。"""
        name = self._stage_name(stage).lower()
        mapping = {
            "friendly": "friendly",
            "unsettling": "unsettling",
            "psychological": "psychological",
            "hostile": "hostile",
            "final": "final"
        }
        return mapping.get(name, "friendly")

    def Destroy(self):
        """系统销毁时清理。"""
        for pid, eid in list(self._companions.items()):
            serverApi.DestroyEntity(eid)
        self._companions.clear()
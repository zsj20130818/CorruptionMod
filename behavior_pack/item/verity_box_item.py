# -*- coding: utf-8 -*-
"""VerityBoxItem - 网易基岩版"""

from __future__ import print_function, division, absolute_import, unicode_literals

import math

import mod.server.extraServerApi as serverApi

from registry.verity_sounds import VeritySounds
from progression.corruption_data import CorruptionData
from progression.corruption_stage import CorruptionStage
from dialogue.dialogue_manager import DialogueManager


class VerityBoxItem(object):
    """Verity 生物蛋 / Verity Box 物品使用逻辑。"""

    ITEM_ID = "verity:box"

    @staticmethod
    def use(player_id, level):
        """右键使用盒子：在玩家面前 2 格生成 verity:companion 实体。"""
        pos = serverApi.GetPlayerPosition(player_id)
        if pos is None:
            VerityBoxItem._send_message(player_id, "[Verity] Failed to spawn: cannot get player position.")
            return False

        rot = serverApi.GetPlayerRotation(player_id)
        yaw = rot[1] if rot else 0
        dx = -math.sin(yaw * math.pi / 180.0) * 2.0
        dz = math.cos(yaw * math.pi / 180.0) * 2.0
        spawn_pos = (pos[0] + dx, pos[1] + 1.5, pos[2] + dz)

        entity_id = serverApi.CreateEntity("verity:placeholder", spawn_pos, (0, yaw))
        if not entity_id:
            VerityBoxItem._send_message(player_id, "[Verity] Failed to summon Verity.")
            return False

        # 增加腐化交互值
        data = CorruptionData.get()
        data.add_interaction(2.0)
        data.record_encounter(player_id, serverApi.GetPlayerName(player_id))

        # 问候对话
        dm = DialogueManager()
        stage = data.get_stage()
        player_name = serverApi.GetPlayerName(player_id) or "Player"
        mem = data.get_memory(player_id)
        encounters = mem.encounters if mem else 0
        reply = dm.pick_for_stage(stage, player_name, encounters)

        VerityBoxItem._send_message(player_id, "[Verity] " + reply)

        # 播放 letmeout 音效
        serverApi.PlayLocalSound(
            player_id,
            VeritySounds.VOICE_LETMEOUT,
            (spawn_pos[0], spawn_pos[1], spawn_pos[2]),
            1.0,
            1.0
        )

        return True

    @staticmethod
    def _send_message(player_id, text):
        serverApi.NotifyToClient(player_id, "verity.system_message", {"msg": text})

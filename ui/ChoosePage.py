from models.Roles import (
    Prophet,
    Witch,
    Hunter,
    Idiot,
    Villager,
    Wolf,
    WildChild,
    MaskWolf,
    Dancer,
    Warden,
    DreamCatcher,
    GhostBride,
    Guard,
    Psyquic,
    MechanicalWolf,
)
import random
from models.Player import Player


# 选择板子并返还板子名字，角色列表以及随机玩家列表
def choose_board(boardNumber: int):
    if boardNumber == 1:
        board_name = "预女猎白混"
        roles = [
            Prophet(),
            Witch(),
            Hunter(),
            Idiot(),
            WildChild(),
            Villager(),
            Villager(),
            Villager(),
            Wolf(),
            Wolf(),
            Wolf(),
            Wolf(),
        ]
    elif boardNumber == 2:
        board_name = "假面舞会"
        roles = [
            Prophet(),
            Witch(),
            Idiot(),
            Dancer(),
            Villager(),
            Villager(),
            Villager(),
            Villager(),
            MaskWolf(),
            Wolf(),
            Wolf(),
            Wolf(),
        ]
    elif boardNumber == 3:
        board_name = "孤注一掷"
        roles = [
            Prophet(),
            Witch(),
            Hunter(),
            DreamCatcher(),
            Villager(),
            Villager(),
            Villager(),
            Villager(),
            Wolf(),
            Wolf(),
            Wolf(),
            Warden(),
        ]
    elif boardNumber == 4:
        board_name = "鬼魂新娘"
        roles = [
            Prophet(),
            Witch(),
            Hunter(),
            Guard(),
            Villager(),
            Villager(),
            Villager(),
            Villager(),
            Wolf(),
            Wolf(),
            Wolf(),
            GhostBride(),
        ]
    elif boardNumber == 5:
        board_name = "机械狼通灵师"
        roles = [
            Psyquic(),
            Witch(),
            Hunter(),
            Guard(),
            Villager(),
            Villager(),
            Villager(),
            Villager(),
            MechanicalWolf(),
            Wolf(),
            Wolf(),
            Wolf(),
        ]
    else:
        board_name = "未知"
        roles = []

    # 打乱角色顺序
    roles_shuffled = roles[:]
    random.shuffle(roles_shuffled)
    players = [Player(i + 1, roles_shuffled[i]) for i in range(len(roles_shuffled))]
    return board_name, roles, players

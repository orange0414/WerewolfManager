class Role:
    def __init__(
        self,
        name: str,
        group: str,
        skill_1: str,
        skill_2: str,
        passive: str,
        description: str,
    ):
        self.name = name
        self.group = group
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.passive = passive
        self.description = description


# 女巫
class Witch(Role):
    def __init__(self):
        super().__init__(
            name="女巫",
            group="神职",
            skill_1="解药",
            skill_2="毒药",
            passive=None,
            description="女巫使用解药前，可以在晚上得知当晚被狼队杀害的对象，并决定是否使用解药将其救活，但女巫不可以自救；女巫也可以利用白天所得资讯，将怀疑的对象毒杀，该对象若为猎人或狼王死后不能发动技能。解药和毒药不可以在同一夜使用。",
        )


# 猎人
class Hunter(Role):
    def __init__(self):
        super().__init__(
            name="猎人",
            group="神职",
            skill_1=None,
            skill_2=None,
            passive="开枪",
            description="猎人死后可以选择开枪带走一名玩家，若猎人被女巫毒杀，则不能开枪。",
        )


# 白痴
class Idiot(Role):
    def __init__(self):
        super().__init__(
            name="白痴",
            group="神职",
            skill_1=None,
            skill_2=None,
            passive="翻牌",
            description="白痴在被投票出局时，可以发动技能翻牌，告诉所有人自己的身份。",
        )


# 村民
class Villager(Role):
    def __init__(self):
        super().__init__(
            name="村民",
            group="村民",
            skill_1=None,
            skill_2=None,
            passive=None,
            description="村民没有技能，白天可以参与投票放逐。",
        )


# 狼人
class Wolf(Role):
    def __init__(self):
        super().__init__(
            name="狼人",
            group="狼人",
            skill_1="杀人",
            skill_2="自爆",
            passive=None,
            description="狼人每晚可以选择击杀一名玩家。白天发言环节可以选择自爆，迅速进入黑夜阶段，自爆狼可以在夜间参与刀人，随后死亡出局。",
        )


# 混子
class WildChild(Role):
    def __init__(self):
        super().__init__(
            name="混子",
            group="村民",
            skill_1="选择榜样",
            skill_2=None,
            passive=None,
            description="混子在第一夜睁眼选择一名玩家作为榜样，混子不知道其具体身份，但是胜利条件与选择对象一致。",
        )


# 预言家
class Prophet(Role):
    def __init__(self):
        super().__init__(
            name="预言家",
            group="神职",
            skill_1="查验",
            skill_2=None,
            passive=None,
            description="预言家每晚可以选择一名玩家进行验人，并且得知其身份为好人阵营或狼人阵营。",
        )


#  舞者
class Dancer(Role):
    def __init__(self):
        super().__init__(
            name="舞者",
            group="神职",
            skill_1="共舞",
            skill_2=None,
            passive="抗毒",
            description="""
                从第二个夜间开始，每个夜间选三位玩家进入舞池跳舞。舞者只能选择未进入过舞池的玩家跳舞:
                \n1.三人阵营相同，无事发生。
                \n2.三人阵营不同，则阵营人数少的那位玩家出局。	
                \n3.若舞者自己进入舞池，则舞池中的三位玩家当晚免疫狼刀。
                \n舞者可以免疫女巫的毒药。""",
        )


#   假面
class MaskWolf(Role):
    def __init__(self):
        super().__init__(
            name="假面",
            group="狼人",
            skill_1="假面",
            skill_2=None,
            passive="抗毒",
            description="""
                假面可以免疫女巫的毒药。
                \n可以选择一位玩家查看其是否在舞池中。可以选择一位玩家赐予假面面具，被赐予面具的玩家在【共舞】技能结算时的阵营反转。
                3个狼人全部出局后继承狼刀。\n补充说明：夜间假面不与狼队友同时睁眼。假面无【自爆】技能""",
        )


#   典狱长
class Warden(Role):
    def __init__(self):
        super().__init__(
            name="典狱长",
            group="狼人",
            skill_1="交易",
            skill_2=None,
            passive=None,
            description="""
                第二夜起，典狱长可选择两名未进行过交易的玩家进行【交易】，随后与狼人一起睁眼。
                技能【交易】：在交易环节，两名玩家会被唤醒，可确认交易玩家，但不知晓其身份。随后各自闭眼选择大拇指向上向下，【交易】或【背叛】。
                技能效果：
                \n1. 同时交易，两人都免于夜间伤害。
                \n2. 同时背叛，双方夜间各自的技能都会释放到对方身上。
                \n3. 一交易一背叛，交易方出局。
                \n额外效果【决斗】：若典狱长选择自己进入交易环节，则双方选择一致典狱长出局，不一致另一方出局。""",
        )


#  摄梦人
class DreamCatcher(Role):
    def __init__(self):
        super().__init__(
            name="摄梦人",
            group="神职",
            skill_1="梦游",
            skill_2=None,
            passive=None,
            description="""
                每晚起身选择一名玩家进行梦游，被梦游的玩家不可得知自己被梦游，技能效果如下：
                \n1. 若连续两晚梦游同一人，则被梦游玩家出局，女巫无法救活。
                \n2. 被梦游者免疫夜间技能（狼刀 解药 毒药 均视为技能已使用但落空）
                \n3. 摄梦人受到的技能效果，梦游者也能受到。如狼刀，女巫毒药，用于摄梦人，则梦游者一同出局。
                \n4. 被梦游出局的猎人无法开枪。
                \n5. 摄梦人无法选择不发动技能。""",
        )


# 鬼魂新娘
class GhostBride(Role):
    def __init__(self):
        super().__init__(
            name="鬼魂新娘",
            group="第三方",
            skill_1="新婚",
            skill_2="证婚",
            passive=None,
            description="""
                查验为好人。第一晚选择一位新郎，新郎睁眼，共同商讨战术并选择一名证婚人，
                证婚人单独睁眼知晓新娘新郎号码。新郎新娘可夜晚睁眼商讨战术，证婚人仅得知号码牌不可得知身份，
                属第三方。新郎新娘任何一张牌倒牌，另一张随之一起。单身狼人全部出局以后，新娘新郎带刀。
                单身狼人新娘新郎均出局，则证婚人带刀。若证婚人为狼，则优先于情侣带刀。猎人殉情而死无法开枪。
                \n单身狼人全死 则单身狼人判负
                \n第三阵营全死 则第三阵营判负
                \n第三阵营 单身狼人全负 则好人获胜""",
        )


# 守卫
class Guard(Role):
    def __init__(self):
        super().__init__(
            name="守卫",
            group="神职",
            skill_1="守护",
            skill_2=None,
            passive=None,
            description="""
                每晚可以选择一名玩家进行守护，守护的玩家在当晚免疫狼刀。
                \n1. 守卫的盾无法抵挡毒药。
                \n2. 守卫可以守护自己。
                \n3. 守卫不能连续两晚守护同一人。
                \n4. 守卫的盾和女巫的解药同时对一人生效则此人身亡。""",
        )


# 机械狼
class MechanicalWolf(Role):
    def __init__(self):
        super().__init__(
            name="机械狼",
            group="狼人",
            skill_1="模仿",
            skill_2=None,
            passive=None,
            description="""
                夜晚不与小狼见面，不可自爆。 可在任意夜晚模仿一位存活的玩家的身份和技能。
                当所有小狼出局后，机械狼才可入夜刀人。若模仿对象是女巫，从模仿的下一个夜间开始，可以使用一瓶毒药；
                若模仿的对象是猎人，可以开枪，开枪规则同猎人；若模仿的对象是守卫，从模仿的下一个夜间开始，
                可以守护一位玩家不被狼人刀死、并且反弹女巫毒药，可以和女巫的解药同时生效奶死某位玩家；
                若模仿的对象是通灵师，从模仿的下一个夜间开始，可以每晚查验一位玩家的具体身份；
                若模仿的对象是狼人，在所有小狼出局后可多刀一人，且额外刀的人无法被女巫的解药、守卫的盾牌解救；
                若模仿的对象是平民，无特殊技能，被查验时显示平民身份。""",
        )


# 通灵师
class Psyquic(Role):
    def __init__(self):
        super().__init__(
            name="通灵师",
            group="神职",
            skill_1="查验",
            skill_2=None,
            passive=None,
            description="""
                每晚查验场上一名存活玩家的具体身份。
                如果查验对象是机械狼：若机械狼已经进行模仿，
                则查验结果为机械狼模仿的玩家身份；若机械狼尚未模仿，则查验结果为机械狼。""",
        )

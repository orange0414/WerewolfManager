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


class Wolf(Role):
    def __init__(self):
        super().__init__(
            name="狼人",
            group="狼人",
            skill_1="杀人",
            skill_2=None,
            passive=None,
            description="狼人每晚可以选择击杀一名玩家",
        )


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

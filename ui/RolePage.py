from PyQt6.QtWidgets import QScrollArea, QFrame, QVBoxLayout, QLabel, QWidget


class RolePage(QWidget):
    def __init__(self, roles, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("本局角色列表", self))

        # 用集合去重，只显示每种角色一次
        unique_roles = {}
        for role in roles:
            key = role.name
            if key not in unique_roles:
                unique_roles[key] = role

        # 可滚动区
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 每个角色一张卡片，所有QLabel自动换行
        for role in unique_roles.values():
            role_card = QFrame()
            role_card.setFrameShape(QFrame.Shape.Box)
            role_card.setLineWidth(1)
            card_layout = QVBoxLayout(role_card)

            name_label = QLabel(f"<b>角色名：</b>{role.name}")
            name_label.setWordWrap(True)
            card_layout.addWidget(name_label)

            group_label = QLabel(f"<b>阵营：</b>{role.group}")
            group_label.setWordWrap(True)
            card_layout.addWidget(group_label)

            if role.skill_1:
                skill1_label = QLabel(f"<b>技能1：</b>{role.skill_1 or '无'}")
                skill1_label.setWordWrap(True)
                card_layout.addWidget(skill1_label)

            if role.skill_2:
                skill2_label = QLabel(f"<b>技能2：</b>{role.skill_2 or '无'}")
                skill2_label.setWordWrap(True)
                card_layout.addWidget(skill2_label)

            if role.passive:
                passive_label = QLabel(f"<b>被动技能：</b>{role.passive}")
                passive_label.setWordWrap(True)
                card_layout.addWidget(passive_label)

            desc_label = QLabel(f"<b>角色介绍：</b>{role.description}")
            desc_label.setWordWrap(True)
            card_layout.addWidget(desc_label)

            scroll_layout.addWidget(role_card)
        scroll_layout.addStretch(1)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

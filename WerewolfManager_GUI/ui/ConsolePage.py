from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QListWidget,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
)
import random


class ConsolePage(QWidget):
    def __init__(self, status_bar, board_name, players):
        super().__init__()
        self.status_bar = status_bar
        self.players = players
        layout = QHBoxLayout(self)

        # 玩家信息表（只显示角色、状态、死亡方式/描述）
        self.player_table = QTableWidget(len(players), 3)
        self.player_table.setHorizontalHeaderLabels(["角色", "状态", "死亡方式"])
        for i, player in enumerate(self.players):
            self.player_table.setItem(i, 0, QTableWidgetItem(player.role.name))
            # 状态下拉框
            status_combo = QComboBox()
            status_combo.addItems(["存活", "死亡"])
            status_combo.setCurrentIndex(0 if player.alive else 1)
            status_combo.currentIndexChanged.connect(
                lambda idx, p=player: self.update_player_status(p, idx)
            )
            self.player_table.setCellWidget(i, 1, status_combo)
            from PyQt6.QtWidgets import QLineEdit

            # 死亡方式输入框
            desc_edit = QLineEdit()
            desc_edit.setPlaceholderText("请输入死亡方式")
            desc_edit.setToolTip("例如：被狼人杀死、被女巫毒死等")
            if player.death_type:
                desc_edit.setText(player.death_type)
            desc_edit.textChanged.connect(
                lambda text, p=player: self.update_death_type(p, text)
            )
            self.player_table.setCellWidget(i, 2, desc_edit)

        # 夜间行动
        night_layout = QVBoxLayout()
        night_layout.addWidget(QLabel("夜间行动"))
        self.night_action_edit = QTextEdit()
        self.night_action_edit.setPlaceholderText(
            "请按夜间顺序记录各角色行动，例如：\n狼人刀5号\n女巫救5号\n女巫毒2号\n..."
        )
        night_layout.addWidget(self.night_action_edit)
        self.night_action_btn = QPushButton("记录夜间行动到日志")
        self.night_action_btn.clicked.connect(self.add_night_action_log)
        night_layout.addWidget(self.night_action_btn)

        # 白天发言收集关键词
        day_layout = QVBoxLayout()
        day_layout.addWidget(QLabel("白天发言关键词"))
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("输入白天发言关键词，回车添加")
        self.keyword_input.returnPressed.connect(self.add_keyword)
        day_layout.addWidget(self.keyword_input)
        self.keyword_list = QListWidget()
        day_layout.addWidget(self.keyword_list)
        self.add_keyword_btn = QPushButton("记录所有关键词到日志")
        self.add_keyword_btn.clicked.connect(self.add_keywords_log)
        day_layout.addWidget(self.add_keyword_btn)

        # 日志区
        log_layout = QVBoxLayout()
        log_layout.addWidget(QLabel("日志"))
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        log_layout.addWidget(self.log_edit)
        self.clear_log_btn = QPushButton("清空日志")
        self.clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(self.clear_log_btn)

        # 发言顺序按钮
        self.random_speech_order_btn = QPushButton("随机顺序发言")
        self.random_speech_order_btn.clicked.connect(
            lambda: self.random_speech_order(reverse=False)
        )
        log_layout.addWidget(self.random_speech_order_btn)

        self.random_reverse_order_btn = QPushButton("随机逆序发言")
        self.random_reverse_order_btn.clicked.connect(
            lambda: self.random_speech_order(reverse=True)
        )
        log_layout.addWidget(self.random_reverse_order_btn)

        # 布局
        layout.addWidget(self.player_table)
        self.player_table.setMinimumWidth(450)
        self.player_table.setMinimumHeight(300)
        self.player_table.horizontalHeader().setStretchLastSection(True)
        layout.addLayout(night_layout)
        layout.addLayout(day_layout)
        layout.addLayout(log_layout)

        self.status_bar.showMessage(
            f"欢迎使用狼人杀主控台：{board_name}！所有报错会在此状态栏显现！请注意观察。"
        )

    # 添加夜间行动日志
    def add_night_action_log(self):
        text = self.night_action_edit.toPlainText().strip()
        if not text:
            self.status_bar.showMessage(f"【系统提示】: 夜间行动不能为空!!!")
            return
        self.log_edit.append(f"<b>【夜间行动】</b>\n{text}\n")
        self.night_action_edit.clear()

    # 添加白天关键词
    def add_keyword(self):
        keyword = self.keyword_input.text().strip()
        if keyword:
            self.keyword_list.addItem(keyword)
            self.keyword_input.clear()

    # 添加白天关键词日志
    def add_keywords_log(self):
        if self.keyword_list.count() == 0:
            self.status_bar.showMessage(f"【系统提示】: 请至少添加一个关键词!!!")
            return
        keywords = [
            self.keyword_list.item(i).text() for i in range(self.keyword_list.count())
        ]
        self.log_edit.append(f"<b>【白天关键词】</b>\n{'、'.join(keywords)}\n")
        self.keyword_list.clear()

    # 清空日志
    def clear_log(self):
        self.log_edit.clear()

    # 更新玩家状态
    def update_player_status(self, player, idx):
        player.alive = idx == 0

    # 更新死亡方式
    def update_death_type(self, player, text):
        player.death_type = text

    def random_speech_order(self, reverse=False):
        alive = [p.number for p in self.players if p.alive]
        if not alive:
            self.log_edit.append("<b>当前没有存活玩家！</b>")
            return
        alive.sort(reverse=reverse)
        start = random.choice(alive)
        idx = alive.index(start)
        # 以start为起点循环
        order = alive[idx:] + alive[:idx]
        self.log_edit.append(
            f"<b>随机起点{'（逆序）' if reverse else ''}发言顺序：</b>{' '.join(map(str, order))}（起点：{start}号）"
        )

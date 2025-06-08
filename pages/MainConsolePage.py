from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QListWidget,
    QHBoxLayout,
)


class MainConsolePage(QWidget):  # <== 注意这里变为 QWidget
    def __init__(self, status_bar, board_name):
        super().__init__()
        self.status_bar = status_bar
        layout = QHBoxLayout(self)

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

        layout.addLayout(night_layout, 2)
        layout.addLayout(day_layout, 2)
        layout.addLayout(log_layout, 3)

        self.status_bar.showMessage(
            f"欢迎使用狼人杀主控台：{board_name}！所有报错会在此状态栏显现！请注意观察。"
        )

    def add_night_action_log(self):
        text = self.night_action_edit.toPlainText().strip()
        if not text:
            self.status_bar.showMessage(f"【系统提示】: 夜间行动不能为空!!!")
            return
        self.log_edit.append(f"<b>【夜间行动】</b>\n{text}\n")
        self.night_action_edit.clear()

    def add_keyword(self):
        keyword = self.keyword_input.text().strip()
        if keyword:
            self.keyword_list.addItem(keyword)
            self.keyword_input.clear()

    def add_keywords_log(self):
        if self.keyword_list.count() == 0:
            self.status_bar.showMessage(f"【系统提示】: 请至少添加一个关键词!!!")
            return
        keywords = [
            self.keyword_list.item(i).text() for i in range(self.keyword_list.count())
        ]
        self.log_edit.append(f"<b>【白天关键词】</b>\n{'、'.join(keywords)}\n")
        self.keyword_list.clear()

    def clear_log(self):
        self.log_edit.clear()

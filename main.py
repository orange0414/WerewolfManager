from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QMainWindow,
    QStatusBar,
    QStackedWidget,
    QApplication,
)
from models.LogPage import LogPage
from models.MainConsolePage import MainConsolePage
from models.RolePage import RolePage
from Roles import Witch, Hunter, Idiot, Villager, Wolf, WildChild, Prophet
from models.Player import Player
import random

available_boards = [1, 2, 3, 4]


class BoardSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择板子")
        self.selected = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("请选择板子："))
        names = ["1. 预女猎白混", "2. 假面舞会", "3. 孤注一掷", "4. 鬼魂新娘"]
        for i, name in enumerate(names, 1):
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, x=i: self.select_board(x))
            layout.addWidget(btn)

    def select_board(self, number):
        self.selected = number
        self.accept()


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
        roles = []
    elif boardNumber == 3:
        board_name = "孤注一掷"
        roles = []
    elif boardNumber == 4:
        board_name = "鬼魂新娘"
        roles = []
    else:
        board_name = "未知"
        roles = []
    return board_name, roles


class MainWindow(QMainWindow):
    def __init__(self, board_name, roles, players):
        super().__init__()
        self.setWindowTitle("狼人杀管理器")
        self.resize(1100, 700)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("QStatusBar{font-weight:bold;}")

        self.role_page = RolePage(roles)
        self.console_page = MainConsolePage(self.status_bar, board_name, players)
        self.log_page = LogPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.role_page)  # index 0
        self.stack.addWidget(self.console_page)  # index 1
        self.stack.addWidget(self.log_page)  # index 2

        # 顶部导航栏
        btn_role = QPushButton("角色管理")
        btn_console = QPushButton("主控台")
        btn_log = QPushButton("日志/设置")
        btn_role.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_console.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_log.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        nav_bar = QHBoxLayout()
        nav_bar.addWidget(btn_role)
        nav_bar.addWidget(btn_console)
        nav_bar.addWidget(btn_log)

        layout = QVBoxLayout()
        layout.addLayout(nav_bar)
        layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


def create_randomized_players(roles):
    roles_shuffled = roles[:]
    random.shuffle(roles_shuffled)
    players = [Player(i + 1, roles_shuffled[i]) for i in range(len(roles_shuffled))]
    return players


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    select_dialog = BoardSelectDialog()
    if select_dialog.exec() == QDialog.DialogCode.Accepted:
        boardNumber = select_dialog.selected
        board_name, roles = choose_board(boardNumber)
        players = create_randomized_players(roles)  # 随机分配角色
        window = MainWindow(board_name, roles, players)
        window.show()
        sys.exit(app.exec())

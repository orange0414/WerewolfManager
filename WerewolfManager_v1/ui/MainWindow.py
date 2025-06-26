from PyQt6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)
from ui.RolePage import RolePage
from ui.ConsolePage import ConsolePage
from ui.LogPage import LogPage


class MainWindow(QMainWindow):
    def __init__(self, board_name, roles, players):
        super().__init__()
        self.setWindowTitle("狼人杀管理器")
        self.resize(1100, 700)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("QStatusBar{font-weight:bold;}")

        self.role_page = RolePage(roles)
        self.console_page = ConsolePage(self.status_bar, board_name, players)
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

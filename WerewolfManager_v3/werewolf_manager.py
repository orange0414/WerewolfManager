import sys
import json
import random
from copy import deepcopy
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QMessageBox, QLabel,
    QScrollArea, QFrame, QListWidget
)
from PyQt6.QtCore import Qt

# Mapping team to colors
TEAM_COLORS = {
    '狼人': "#FF1313",      # red
    '神职': "#F6DA39",      # gold
    '村民': "#50E650",      # green
    '第三方': "#E793E7",    # purple
}

class Role:
    def __init__(self, name: str, team: str, description: str):
        self.name = name
        self.team = team
        self.description = description

class RoleManager:
    def __init__(self, roles_file: str):
        self.roles = {}
        self.load_roles(roles_file)

    def load_roles(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for r in data:
            role = Role(r['name'], r['team'], r['description'])
            self.roles[role.name] = role

class BoardManager:
    def __init__(self, role_manager: RoleManager):
        self.boards = {
            "预女猎白混": {"预言家":1, "女巫":1, "猎人":1, "白痴":1, "混子":1, "村民":3, "狼人":4},
            "假面舞会": {"预言家":1, "女巫":1, "舞者":1, "白痴":1, "村民":4, "狼人":3, "假面":1},
            "孤注一掷": {"预言家":1, "女巫":1, "猎人":1, "摄梦人":1, "村民":4, "狼人":3, "典狱长":1},
            "机械狼通灵师": {"通灵师":1, "女巫":1, "守卫":1, "猎人":1, "村民":4, "狼人":3, "机械狼":1},
            "盗宝通灵": {"通灵师":1, "毒师":1, "猎人":1, "摄梦人":1, "蒙面人":1, "村民":5, "狼人":4, "盗宝大师":1},
            "鬼魂新娘": {"预言家":1, "女巫":1, "猎人":1, "守卫":1, "村民":4, "狼人":3, "鬼魂新娘":1},
            "骑士狼美": {"预言家":1, "女巫":1, "守卫":1, "骑士":1, "村民":4, "狼人":3, "狼美人":1},
        }
        self.role_manager = role_manager
        self.current_board = None
        self.current_roles = []

    def select_board(self, board_name: str) -> bool:
        config = self.boards.get(board_name)
        if not config:
            return False
        self.current_board = board_name
        self.current_roles.clear()
        for role_name, count in config.items():
            template = self.role_manager.roles.get(role_name)
            if not template:
                continue
            for _ in range(count):
                self.current_roles.append(deepcopy(template))
        random.shuffle(self.current_roles)
        return True

class MainWindow(QMainWindow):
    def __init__(self, role_mgr: RoleManager, board_mgr: BoardManager):
        super().__init__()
        self.setWindowTitle("狼人杀管理器")
        self.resize(800, 600)
        self.role_mgr = role_mgr
        self.board_mgr = board_mgr
        self.players = []
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 版型选择页
        self.tab_boards = QWidget()
        self.tabs.addTab(self.tab_boards, "版型选择")
        self._init_boards_tab()

        # 角色介绍页
        self.tab_roles = QWidget()
        self.tabs.addTab(self.tab_roles, "角色介绍")
        self._init_roles_tab()

        # 玩家管理页
        self.tab_players = QWidget()
        self.tabs.addTab(self.tab_players, "玩家管理")
        self._init_players_tab()

        # 游戏流程页（占位）
        self.tab_flow = QWidget()
        flow_layout = QVBoxLayout(self.tab_flow)
        flow_label = QLabel("游戏流程模块，后续实现具体逻辑")
        flow_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        flow_layout.addWidget(flow_label)
        self.tabs.addTab(self.tab_flow, "游戏流程")

    def _init_boards_tab(self):
        layout = QHBoxLayout(self.tab_boards)
        btn_widget = QWidget()
        blayout = QVBoxLayout(btn_widget)
        for name in self.board_mgr.boards:
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, n=name: self._on_board_click(n))
            blayout.addWidget(btn)
        layout.addWidget(btn_widget, 1)

        info_widget = QWidget()
        ilayout = QVBoxLayout(info_widget)
        self.lbl_board = QLabel("当前版型：无")
        self.lbl_config = QLabel("配置：")
        self.lbl_config.setWordWrap(True)
        ilayout.addWidget(self.lbl_board)
        ilayout.addWidget(self.lbl_config)
        layout.addWidget(info_widget, 2)

    def _on_board_click(self, name: str):
        if self.board_mgr.select_board(name):
            self.lbl_board.setText(f"当前版型：{name}")
            cfg = self.board_mgr.boards[name]
            parts = [f"{r}×{c}" for r, c in cfg.items()]
            self.lbl_config.setText("配置：" + ", ".join(parts))
            QMessageBox.information(self, "版型已选", f"已选择版型：{name}")
            self.update_roles_tab()
            # 自动创建玩家
            self.players = [str(i+1) for i in range(len(self.board_mgr.current_roles))]
            self.update_players_tab()
        else:
            QMessageBox.warning(self, "错误", "无法选择该版型")

    def _init_roles_tab(self):
        layout = QVBoxLayout(self.tab_roles)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        container = QWidget()
        self.roles_layout = QVBoxLayout(container)
        self.scroll_area.setWidget(container)
        layout.addWidget(self.scroll_area)
        lbl = QLabel("请先在‘版型选择’页选择版型")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.roles_layout.addWidget(lbl)

    def update_roles_tab(self):
        # clear
        for i in reversed(range(self.roles_layout.count())):
            w = self.roles_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        if not self.board_mgr.current_roles:
            lbl = QLabel("请先在‘版型选择’页选择版型")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.roles_layout.addWidget(lbl)
            return
        unique = {r.name: r for r in self.board_mgr.current_roles}
        for role in unique.values():
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.Box)
            vbox = QVBoxLayout(frame)
            lbl_name = QLabel(f"名称：{role.name}")
            lbl_team = QLabel(f"阵营：{role.team}")
            color = TEAM_COLORS.get(role.team, '#000000')
            lbl_team.setStyleSheet(f"color: {color}; font-weight: bold;")
            lbl_desc = QLabel(f"描述：{role.description}")
            lbl_desc.setWordWrap(True)
            vbox.addWidget(lbl_name)
            vbox.addWidget(lbl_team)
            vbox.addWidget(lbl_desc)
            vbox.setSpacing(5)
            self.roles_layout.addWidget(frame)
        self.roles_layout.addStretch()

    def _init_players_tab(self):
        layout = QVBoxLayout(self.tab_players)
        self.player_list = QListWidget()
        layout.addWidget(self.player_list)
        btn_assign = QPushButton("分配角色")
        btn_assign.clicked.connect(self.assign_roles)
        layout.addWidget(btn_assign)

    def update_players_tab(self):
        self.player_list.clear()
        for name in self.players:
            self.player_list.addItem(name)

    def assign_roles(self):
        if not self.board_mgr.current_roles:
            QMessageBox.warning(self, "未选版型", "请先选择版型")
            return
        if len(self.players) > len(self.board_mgr.current_roles):
            QMessageBox.warning(self, "角色不足", "玩家超过角色数量")
            return
        roles = deepcopy(self.board_mgr.current_roles)
        random.shuffle(roles)
        self.player_list.clear()
        for i, name in enumerate(self.players):
            self.player_list.addItem(f"{name} → {roles[i].name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rm = RoleManager('data/roles.json')
    bm = BoardManager(rm)
    win = MainWindow(rm, bm)
    win.show()
    sys.exit(app.exec())

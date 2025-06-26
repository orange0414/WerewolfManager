from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QDialog,
    QPushButton,
    QApplication,
)
from ui import ChoosePage
from ui.MainWindow import MainWindow

available_boards = [1, 2, 3, 4, 5]  # 可用的板子编号列表


class BoardSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择板子")
        self.selected = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("请选择板子："))
        names = [
            "1. 预女猎白混",
            "2. 假面舞会",
            "3. 孤注一掷",
            "4. 鬼魂新娘",
            "5. 机械狼通灵师",
        ]
        for i, name in enumerate(names, 1):
            btn = QPushButton(name)
            btn.clicked.connect(lambda _, x=i: self.select_board(x))
            layout.addWidget(btn)

    def select_board(self, number):
        self.selected = number
        self.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    select_dialog = BoardSelectDialog()
    if select_dialog.exec() == QDialog.DialogCode.Accepted:
        boardNumber = select_dialog.selected
        board_name, roles, players = ChoosePage.choose_board(
            boardNumber
        )  # 随机分配角色
        window = MainWindow(board_name, roles, players)
        window.show()
        sys.exit(app.exec())

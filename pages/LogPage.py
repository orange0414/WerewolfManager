from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class LogPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这里是日志/设置页"))
        self.setLayout(layout)

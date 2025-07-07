from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class MenuScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Logo
        logo = QLabel()
        pixmap = QPixmap("app/assets/icons/code_craft_vAlfa.webp").scaledToWidth(300)
        logo.setPixmap(pixmap)
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        # Przycisk start
        layout.addWidget(QLabel("Witaj w CODECRAFT!"))

        # NOWY PRZYCISK – wybór modułu
        for i in range(1, 6):
            module_button = QPushButton(f"Moduł {i}")
            module_button.clicked.connect(lambda _, index=i: self.main_window.select_lesson(index))
            layout.addWidget(module_button)

        self.setLayout(layout)

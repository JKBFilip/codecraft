from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ModuleSelectScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📚 Wybierz moduł"))
        for i in range(1, 4):
            btn = QPushButton(f"Lekcja {i}")
            btn.clicked.connect(lambda checked, index=i: self.load_lesson(index))
            layout.addWidget(btn)

        back_btn = QPushButton("🔙 Powrót do menu")
        back_btn.clicked.connect(self.main_window.show_menu)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_lesson(self, index):
        self.main_window.set_lesson_index(index)
        self.main_window.show_lesson()

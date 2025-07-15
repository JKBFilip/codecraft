from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QFrame
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from app.views.achievements_screen import AchievementsScreen

class MenuScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.module_widgets = []
        self.init_ui()
        self.update_module_widgets()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)  # ✅ tylko raz

        # ===== Przycisk osiągnięć =====
        self.achievements_button = QPushButton("🏆 Osiągnięcia")
        self.achievements_button.clicked.connect(self.main_window.show_achievements)
        self.layout.addWidget(self.achievements_button)

        # ===== Logo =====
        logo = QLabel()
        pixmap = QPixmap("app/assets/icons/code_craft_vAlfa.webp").scaledToWidth(300)
        logo.setPixmap(pixmap)
        self.layout.addWidget(logo, alignment=Qt.AlignCenter)

        # ===== Nagłówek powitalny =====
        welcome_label = QLabel("Witaj w CODECRAFT!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; margin: 16px 0;")
        self.layout.addWidget(welcome_label)

        # ===== Lista modułów =====
        for i in range(1, 6):
            module_frame = QFrame()
            module_frame.setFrameShape(QFrame.StyledPanel)
            module_frame.setLineWidth(1)

            frame_layout = QHBoxLayout()

            # Przycisk modułu
            btn = QPushButton(f"Moduł {i} (0/16)")
            btn.setStyleSheet("text-align: left; padding-left: 10px;")
            btn.clicked.connect(lambda _, index=i: self.main_window.select_lesson(index))

            # Ikona testu
            test_icon = QLabel()
            test_icon.setPixmap(QPixmap("app/assets/icons/test_icon.png").scaled(24, 24))
            test_icon.setToolTip("Test niezaliczony")
            test_icon.hide()  # domyślnie ukryta

            frame_layout.addWidget(btn, stretch=4)
            frame_layout.addWidget(test_icon, stretch=1, alignment=Qt.AlignRight)
            module_frame.setLayout(frame_layout)

            self.module_widgets.append({
                'frame': module_frame,
                'button': btn,
                'test_icon': test_icon
            })

            self.layout.addWidget(module_frame)  # ✅ tu używamy self.layout
        self.final_exam_button = QPushButton("🎓 Egzamin Końcowy")
        self.final_exam_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.final_exam_button.clicked.connect(self.main_window.show_final_exam)
        self.layout.addWidget(self.final_exam_button)


    def show_achievements(self):
        self.achievements_screen = AchievementsScreen(self.user_account, self)
        self.setCentralWidget(self.achievements_screen)

    def update_module_widgets(self):  # Upewnij się, że nazwa jest taka sama jak w wywołaniu
        """Aktualizuje widgety modułów na podstawie postępu"""
        if not hasattr(self.main_window, 'user_progress'):
            return

        for i, widget in enumerate(self.module_widgets, start=1):
            module_key = str(i)
            tasks_completed = self.main_window.user_progress.module_scores.get(module_key, 0)
            test_passed = f"final_test_{i}" in self.main_window.user_progress.completed_tasks

            # Aktualizacja przycisku
            widget['button'].setText(f"Moduł {i} ({tasks_completed}/16)")

            # Ikona testu
            if test_passed:
                widget['test_icon'].setPixmap(QPixmap("app/assets/icons/test_passed.png").scaled(24, 24))
                widget['test_icon'].setToolTip("Test zaliczony!")
                widget['test_icon'].show()
            else:
                widget['test_icon'].hide()

            # Kolorowanie ramki
            if tasks_completed >= 16 and test_passed:
                widget['frame'].setStyleSheet("""
                    QFrame {
                        background-color: #E8F5E9;
                        border: 2px solid #4CAF50;
                        border-radius: 5px;
                    }
                """)
            else:
                widget['frame'].setStyleSheet("QFrame { background-color: none; border: 1px solid #ddd; }")
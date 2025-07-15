# app/views/achievements_screen.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton
from PySide6.QtCore import Qt

from app.features.achievements import AchievementSystem


class AchievementsScreen(QWidget):
    def __init__(self, user_account, main_window):
        super().__init__()
        self.user_account = user_account
        self.main_window = main_window
        self.init_ui()
        self.refresh_achievements()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Nagłówek
        self.title_label = QLabel("Twoje Osiągnięcia")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin: 10px;
        """)
        self.layout.addWidget(self.title_label)

        # Obszar przewijania z osiągnięciami
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_content.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Przycisk powrotu do menu
        self.back_button = QPushButton("🔙 Powrót do Menu")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.back_button.clicked.connect(self.main_window.show_menu)
        self.layout.addWidget(self.back_button)

    def refresh_achievements(self):
        """Odświeża widok osiągnięć i sprawdza nowe"""
        # Usuń wszystkie istniejące widgety
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Upewnij się, że system osiągnięć istnieje i jest poprawny
        if not hasattr(self.user_account, 'achievement_system') or not self.user_account.achievement_system:
            self.user_account.achievement_system = AchievementSystem(self.user_account)

        # Sprawdź i odblokuj nowe osiągnięcia
        new_achievements = self.user_account.check_achievements()
        if new_achievements:
            self.user_account.save_achievements()

        # Pobierz aktualną listę odblokowanych osiągnięć
        unlocked_ids = set(self.user_account._unlocked_achievements)  # Użyj bezpośrednio zbioru

        # Wyświetl wszystkie osiągnięcia
        for achievement in self.user_account.achievement_system.get_all_achievements():
            is_unlocked = achievement.id in unlocked_ids
            self._add_achievement_widget(achievement, is_unlocked)

    def _add_achievement_widget(self, achievement, is_unlocked):
        """Dodaje widget pojedynczego osiągnięcia
        Args:
            achievement: Obiekt Achievement
            is_unlocked: bool - czy osiągnięcie jest odblokowane
        """
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {'#71ea13' if is_unlocked else '#a197a4'};
                border: 2px solid {'#4caf50' if is_unlocked else '#f44336'};
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
            }}
        """)

        layout = QVBoxLayout(frame)

        # Nagłówek osiągnięcia
        title = QLabel(f"{achievement.icon} {achievement.name}")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
        """)
        layout.addWidget(title)

        # Opis
        desc = QLabel(achievement.description)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Status
        status = QLabel(f"Status: {'✅ Odblokowane' if is_unlocked else '❌ Zablokowane'}")
        status.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)
        layout.addWidget(status)

        # Punkty (jeśli odblokowane)
        if is_unlocked:
            points = QLabel(f"Punkty: {achievement.points} XP")
            points.setStyleSheet("""
                font-size: 14px;
                color: #2196f3;
            """)
            layout.addWidget(points)

        self.scroll_layout.addWidget(frame)
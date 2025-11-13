from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PySide6.QtCore import Qt

class AchievementsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user_account = self.main_window.user_account
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        title = QLabel("🏆 Twoje Osiągnięcia")
        title.setObjectName("welcomeHeader")
        title.setAlignment(Qt.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.achievements_layout = QVBoxLayout(self.content_widget)
        self.achievements_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.content_widget)

        back_button = QPushButton("🔙 Powrót do menu")
        back_button.clicked.connect(self.main_window.show_menu)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(scroll)
        self.main_layout.addWidget(back_button)

    def refresh_achievements(self):
        while self.achievements_layout.count():
            child = self.achievements_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.user_account = self.main_window.user_account
        if not self.user_account:
            self.achievements_layout.addWidget(QLabel("Błąd: Brak danych użytkownika."))
            return

        all_achievements = self.user_account.achievement_system.get_all_achievements()
        unlocked_ids = self.user_account.unlocked_achievements
        username = self.user_account.username

        achievements_displayed = 0
        for ach in all_achievements:
            is_unlocked = (ach.id in unlocked_ids) or (f"{username}_{ach.id}" in unlocked_ids)

            if is_unlocked or not ach.hidden:
                widget = self.create_achievement_widget(ach, is_unlocked)
                self.achievements_layout.addWidget(widget)
                achievements_displayed += 1

        if achievements_displayed == 0:
            self.achievements_layout.addWidget(QLabel("Jeszcze nie zdobyłeś żadnych osiągnięć. Do dzieła!"))

    def create_achievement_widget(self, achievement, is_unlocked):
        if is_unlocked:
            text = f"{achievement.icon} <b>{achievement.name}</b><br><small>{achievement.description}</small>"
            style = "background-color: #283636; border: 1px solid #50fa7b; border-radius: 5px; padding: 10px;"
        else:
            text = f"🔒 <b>{achievement.name}</b><br><small>{achievement.description}</small>"
            style = "background-color: #2a2a40; border-radius: 5px; padding: 10px; color: #888;"

        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(style)
        return label
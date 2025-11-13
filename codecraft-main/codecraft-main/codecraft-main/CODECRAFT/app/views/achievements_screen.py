from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PySide6.QtCore import Qt


class AchievementsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        # Na starcie user_account jest None, to jest w porządku.
        self.user_account = self.main_window.user_account
        self._setup_ui()

    def _setup_ui(self):
        """Tworzy statyczne elementy UI, które nie zależą od danych."""
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

    # W pliku: app/views/achievements_screen.py

    def refresh_achievements(self):

        # KROK 1: Wyczyść starą listę
        while self.achievements_layout.count():
            child = self.achievements_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # KROK 2: Pobierz najświeższe dane użytkownika
        self.user_account = self.main_window.user_account
        if not self.user_account:
            self.achievements_layout.addWidget(QLabel("Błąd: Brak danych użytkownika."))
            return

        # KROK 3: Pobierz dane o osiągnięciach
        all_achievements = self.user_account.achievement_system.get_all_achievements()
        unlocked_ids = self.user_account.unlocked_achievements
        username = self.user_account.username

        # DEBUG, który wciąż jest przydatny
        print(f"\n--- DEBUG: Odświeżanie Osiągnięć dla '{username}' ---")
        print(f"ID w pliku: {unlocked_ids}")
        print("--------------------------------------------------\n")

        # KROK 4: Zbuduj listę na nowo
        achievements_displayed = 0
        for ach in all_achievements:
            # ✅ KLUCZOWA POPRAWKA: Sprawdzamy oba formaty ID!
            # Czy prosty ID jest w zbiorze? LUB czy ID z nazwą użytkownika jest w zbiorze?
            is_unlocked = (ach.id in unlocked_ids) or (f"{username}_{ach.id}" in unlocked_ids)

            if is_unlocked or not ach.hidden:
                widget = self.create_achievement_widget(ach, is_unlocked)
                self.achievements_layout.addWidget(widget)
                achievements_displayed += 1

        if achievements_displayed == 0:
            self.achievements_layout.addWidget(QLabel("Jeszcze nie zdobyłeś żadnych osiągnięć. Do dzieła!"))

    def create_achievement_widget(self, achievement, is_unlocked):
        """Tworzy pojedynczy, estetyczny widget reprezentujący osiągnięcie."""
        if is_unlocked:
            text = f"{achievement.icon} <b>{achievement.name}</b><br><small>{achievement.description}</small>"
            style = "background-color: #283636; border: 1px solid #50fa7b; border-radius: 5px; padding: 10px;"
        else:  # Zablokowane, ale widoczne
            text = f"🔒 <b>{achievement.name}</b><br><small>{achievement.description}</small>"
            style = "background-color: #2a2a40; border-radius: 5px; padding: 10px; color: #888;"

        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(style)
        return label
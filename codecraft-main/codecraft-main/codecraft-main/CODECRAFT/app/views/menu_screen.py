from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame,
    QProgressBar
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class MenuScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setObjectName("menuScreen")

        self.module_widgets = {}
        self.module_definitions = {
            1: {"title": "Podstawy: Zmienne i Typy Danych", "icon": "📦"},
            2: {"title": "Decyzje: Instrukcje Warunkowe", "icon": "🚦"},
            3: {"title": "Powtórzenia: Pętle", "icon": "🔁"},
            4: {"title": "Organizacja: Funkcje", "icon": "🔧"},
            5: {"title": "Kolekcje: Listy", "icon": "📚"},
        }

        self.init_ui()


    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        header_layout = self._create_header()
        main_layout.addLayout(header_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("separator")
        main_layout.addWidget(separator)

        # Dodajemy nagłówek dla sekcji modułów
        modules_header = QLabel("Wybierz moduł, aby rozpocząć naukę")
        modules_header.setObjectName("modulesHeader")
        modules_header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(modules_header)

        modules_grid = QGridLayout()
        modules_grid.setSpacing(20)

        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        for i in range(1, 6):
            module_info = self.module_definitions[i]
            card = self._create_module_card(i, module_info["title"], module_info["icon"])
            row, col = positions[i - 1]
            modules_grid.addWidget(card, row, col)

        main_layout.addLayout(modules_grid)
        main_layout.addStretch()

        self.final_exam_button = QPushButton("🎓 Egzamin Końcowy")
        self.final_exam_button.setObjectName("finalExamButton")
        self.final_exam_button.setMinimumHeight(50)
        self.final_exam_button.setCursor(Qt.PointingHandCursor)
        self.final_exam_button.clicked.connect(self.main_window.show_final_exam)
        main_layout.addWidget(self.final_exam_button)

    def _create_header(self):
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        pixmap = QPixmap("app/assets/icons/code_craft_vAlfa.webp").scaledToWidth(60)
        logo_label.setPixmap(pixmap)

        welcome_layout = QVBoxLayout()
        self.welcome_label = QLabel("Witaj w CODECRAFT!")
        self.welcome_label.setObjectName("welcomeHeader")
        self.xp_label = QLabel("Zaloguj się, aby zobaczyć postępy.")
        self.xp_label.setObjectName("xpLabel")
        welcome_layout.addWidget(self.welcome_label)
        welcome_layout.addWidget(self.xp_label)

        header_layout.addWidget(logo_label)
        header_layout.addLayout(welcome_layout)
        header_layout.addStretch()

        self.cheats_button = QPushButton("🎁")  # Prosta ikona prezentu
        self.cheats_button.setToolTip("Wprowadź kod")
        self.cheats_button.setObjectName("achievementsButton")  # Użyje tego samego stylu co przycisk osiągnięć
        self.cheats_button.setFixedSize(60, 45)  # Mały, kwadratowy przycisk
        self.cheats_button.clicked.connect(self.main_window.show_cheat_code_prompt)
        header_layout.addWidget(self.cheats_button)

        self.achievements_button = QPushButton("🏆 Osiągnięcia")
        self.achievements_button.setObjectName("achievementsButton")
        self.achievements_button.setMinimumSize(150, 45)
        self.achievements_button.setCursor(Qt.PointingHandCursor)
        self.achievements_button.clicked.connect(self.main_window.show_achievements)
        header_layout.addWidget(self.achievements_button)
        return header_layout

    def _create_module_card(self, index, title, icon):
        """Tworzy klikalną kartę dla jednego modułu."""
        card = QPushButton()  # Użycie QPushButton jako klikalnego kontenera
        card.setObjectName("moduleCard")
        card.setCursor(Qt.PointingHandCursor)
        card.clicked.connect(lambda: self.main_window.select_lesson(index))

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Górna część karty: Ikona i tytuł
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setObjectName("moduleIcon")

        title_label = QLabel(title)
        title_label.setObjectName("moduleTitle")
        title_label.setWordWrap(True)

        # --- KLUCZOWA POPRAWKA JEST TUTAJ ---
        # 1. NAJPIERW tworzymy etykietę (pudełko)
        test_status_icon = QLabel()
        # 2. DOPIERO TERAZ nadajemy jej nazwę (naklejamy etykietkę)
        test_status_icon.setObjectName("testStatusIcon")
        # ------------------------------------

        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label, stretch=1)
        top_layout.addWidget(test_status_icon)

        # Dolna część karty: Pasek postępu i tekst
        bottom_layout = QVBoxLayout()
        progress_bar = QProgressBar()
        progress_bar.setObjectName("moduleProgressBar")
        progress_bar.setMaximum(16)  # Maksymalna liczba zadań
        progress_bar.setTextVisible(False)

        progress_label = QLabel("0/16 ukończonych zadań")
        progress_label.setObjectName("moduleProgressLabel")

        bottom_layout.addWidget(progress_bar)
        bottom_layout.addWidget(progress_label)

        layout.addLayout(top_layout)
        layout.addStretch()
        layout.addLayout(bottom_layout)

        # Zapisujemy widgety do słownika, aby móc je aktualizować
        self.module_widgets[index] = {
            'card': card,
            'progress_bar': progress_bar,
            'progress_label': progress_label,
            'test_icon': test_status_icon
        }
        return card

    # --- GŁÓWNA FUNKCJA AKTUALIZUJĄCA ---
    def update_module_widgets(self):
        if not self.main_window.user_account:
            return

        self._update_header()
        self._update_module_cards()
        self._update_final_exam_button_state()

    def _update_header(self):
        user = self.main_window.user_account
        self.welcome_label.setText(f"Witaj z powrotem, {user.username}!")
        self.xp_label.setText(f"Poziom: {user.level}  |  XP: {user.experience}/{user.get_xp_for_next_level()}")

    def _update_module_cards(self):
        progress = self.main_window.user_progress
        for i in range(1, 6):
            widgets = self.module_widgets[i]
            tasks_completed = progress.module_scores.get(str(i), 0)
            test_passed = f"final_test_{i}" in progress.completed_tasks

            widgets['progress_bar'].setValue(tasks_completed)
            widgets['progress_label'].setText(f"{tasks_completed}/16 ukończonych zadań")

            is_completed = tasks_completed >= 16 and test_passed
            widgets['card'].setProperty("completed", is_completed)

            # --- NOWA, PROSTSZA LOGIKA BEZ OBRAZKÓW ---
            if test_passed:
                # Ustawiamy zielony "ptaszek" jako tekst
                widgets['test_icon'].setText("✔️")
                widgets['test_icon'].setToolTip("Test zaliczony!")
            else:
                # Czyścimy tekst, jeśli test nie jest zaliczony
                widgets['test_icon'].setText("")
            # ----------------------------------------------

            # Odświeżamy style, aby QSS zaaplikował zmiany
            widgets['card'].style().unpolish(widgets['card'])
            widgets['card'].style().polish(widgets['card'])

    def _update_final_exam_button_state(self):
        all_modules_completed = self._check_if_all_modules_completed()
        self.final_exam_button.setEnabled(all_modules_completed)

        if not all_modules_completed:
            self.final_exam_button.setToolTip("Ukończ wszystkie moduły (zadania + testy), aby odblokować egzamin.")
        else:
            self.final_exam_button.setToolTip("Gratulacje! Możesz teraz podejść do egzaminu końcowego.")

    def _check_if_all_modules_completed(self) -> bool:
        progress = self.main_window.user_progress
        for i in range(1, 6):
            tasks_completed = progress.module_scores.get(str(i), 0)
            test_passed = f"final_test_{i}" in progress.completed_tasks
            if not (tasks_completed >= 16 and test_passed):
                return False
        return True
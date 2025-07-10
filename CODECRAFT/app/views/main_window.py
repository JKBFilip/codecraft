from PySide6.QtCore import Qt  # This is the correct import
from PySide6.QtWidgets import (QMainWindow, QStackedLayout, QWidget,
                              QMessageBox, QVBoxLayout, QHBoxLayout,
                              QPushButton)

from app.models.auth.password_reset_screen import PasswordResetScreen
from app.views.menu_screen import MenuScreen
from app.views.lesson_screen import LessonScreen
from app.views.task_screen import TaskScreen
from app.views.final_test_screen import FinalTestScreen
from app.views.auth.login_screen import LoginScreen
from app.views.auth.register_screen import RegisterScreen
from app.models.auth.user_account import UserAccount
from app.features.achievements import AchievementSystem
from app.views.achievements_screen import AchievementsScreen



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODECRAFT")
        self.setMinimumSize(800, 600)

        # 1. Najpierw inicjalizujemy podstawowe widgety
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 2. Główny layout z paskiem narzędziowym
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)

        # 3. Tworzymy i konfigurujemy przycisk wylogowania
        self.logout_button = QPushButton("Wyloguj")
        self._setup_logout_button()

        # 4. Górny pasek z przyciskiem
        self.top_bar = QWidget()
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.logout_button)
        self.top_bar.setLayout(self.top_bar_layout)
        self.main_layout.addWidget(self.top_bar)

        # 5. Kontener dla stack layout
        self.stack_container = QWidget()
        self.stack = QStackedLayout()
        self.stack_container.setLayout(self.stack)
        self.main_layout.addWidget(self.stack_container)

        # 6. Inicjalizacja stanu aplikacji
        self.user_account = None
        self.achievement_system = None
        self.lesson_index = 1
        self.current_task_index = 0

        # 7. Inicjalizacja ekranów
        self._init_screens()
        self._setup_ui()
        self.password_reset_screen = PasswordResetScreen(self)
        self.stack.addWidget(self.password_reset_screen)
        # 8. Domyślnie pokazujemy ekran logowania
        self.show_login_screen()

    def _setup_logout_button(self):
        """Konfiguruje przycisk wylogowania"""
        self.logout_button.setStyleSheet("""
            QPushButton {
                padding: 5px;
                background-color: #f44336;
                color: white;
                border-radius: 4px;
                max-width: 100px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.hide()

    def show_password_reset_screen(self):
        self.stack.setCurrentWidget(self.password_reset_screen)
    def _init_screens(self):
        """Inicjalizuje wszystkie ekrany aplikacji"""
        # Ekrany autentykacji
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)

        # Główne ekrany aplikacji
        self.menu_screen = MenuScreen(self)
        self.lesson_screen = None  # Będzie tworzony dynamicznie
        self.task_screen = None  # Będzie tworzony dynamicznie
        self.final_test_screen = None  # Będzie tworzony dynamicznie
        self.achievements_screen = None  # Będzie tworzony dynamicznie

    def _setup_ui(self):
        """Konfiguruje główny interfejs użytkownika"""
        # Dodajemy tylko podstawowe ekrany do stacku
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.register_screen)
        self.stack.addWidget(self.menu_screen)

    def show_login_screen(self):
        """Pokazuje ekran logowania"""
        self.stack.setCurrentWidget(self.login_screen)
        self.logout_button.hide()

    def show_register_screen(self):
        """Pokazuje ekran rejestracji"""
        self.stack.setCurrentWidget(self.register_screen)
        self.logout_button.hide()

    def show_menu(self):
        """Pokazuje główne menu aplikacji"""
        if self.user_account:
            new_achievements = self.user_account.check_achievements()
            for achievement in new_achievements:
                print(f"Nowe osiągnięcie: {achievement.name}")
            if self.achievements_screen:
                self.achievements_screen.refresh_achievements()

        self.stack.setCurrentWidget(self.menu_screen)
        self.logout_button.show()
        self.menu_screen.update_module_widgets()

    # W klasie MainWindow zmodyfikuj metodę show_achievements:
    def show_achievements(self):
        """Pokazuje ekran osiągnięć"""
        if not self.user_account:
            return

        # Zawsze tworzymy nową instancję ekranu osiągnięć
        self.achievements_screen = AchievementsScreen(self.user_account, self)

        # Usuń starą instancję jeśli istnieje
        old_widget = self.stack.indexOf(self.achievements_screen)
        if old_widget >= 0:
            widget_to_remove = self.stack.widget(old_widget)
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        # Dodaj nową instancję
        self.stack.addWidget(self.achievements_screen)
        self.stack.setCurrentWidget(self.achievements_screen)
        self.logout_button.show()

    def _check_user_achievements(self):
        """Sprawdza osiągnięcia tylko dla aktualnego użytkownika"""
        if not hasattr(self, '_achievement_system'):
            self._achievement_system = AchievementSystem(self.user_account)

        # Sprawdź tylko nieodblokowane osiągnięcia
        unlocked = []
        for achievement in self._achievement_system.achievements:
            if achievement.id not in self.user_account.unlocked_achievements:
                if achievement.condition_fn(self.user_account):
                    self.user_account.unlocked_achievements.add(achievement.id)
                    unlocked.append(achievement)
                    self.user_account.save_progress()
        return unlocked

    def show_achievement_notification(self, achievements):
        """Pokazuje powiadomienie o nowym osiągnięciu (może przyjąć pojedyncze osiągnięcie lub listę)"""
        if not isinstance(achievements, list):
            achievements = [achievements]  # Zamień pojedyncze osiągnięcie na listę

        for achievement in achievements:
            print(f"Nowe osiągnięcie: {achievement.name}")

            # Tutaj możesz dodać wyświetlanie powiadomień w GUI jeśli chcesz
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Nowe osiągnięcie!")
            msg.setText(f"Odblokowano: {achievement.name}\n{achievement.description}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    def select_lesson(self, index):
        """Wybier lekcję o podanym indeksie"""
        print(f"\nWybrałeś lekcję {index}")
        self.lesson_index = index
        self.current_task_index = 0
        self.show_lesson()

    def show_lesson(self):
        """Pokazuje ekran lekcji"""
        if self.lesson_screen:
            self.stack.removeWidget(self.lesson_screen)
            self.lesson_screen.deleteLater()

        self.lesson_screen = LessonScreen(self, self.lesson_index)
        self.stack.addWidget(self.lesson_screen)
        self.stack.setCurrentWidget(self.lesson_screen)
        self.logout_button.show()

    def init_task_screen(self):
        """Inicjalizuje ekran zadań jeśli nie istnieje"""
        if not self.task_screen:
            self.task_screen = TaskScreen(self)
            self.stack.addWidget(self.task_screen)

    def show_task(self):
        """Pokazuje ekran zadań"""
        self.init_task_screen()
        self.task_screen.update_task()
        self.stack.setCurrentWidget(self.task_screen)
        self.logout_button.show()

    def previous_task(self):
        """Przechodzi do poprzedniego zadania"""
        if hasattr(self, 'current_task_index') and self.current_task_index > 0:
            self.current_task_index -= 1
            self.task_screen.update_task()

    def next_task(self):
        """Przechodzi do następnego zadania"""
        if (hasattr(self, 'current_task_index') and
                hasattr(self, 'task_screen') and
                self.current_task_index < len(self.task_screen.filtered_tasks) - 1):
            self.current_task_index += 1
            self.task_screen.update_task()

    def start_final_test(self):
        """Rozpoczyna test końcowy"""
        if self.final_test_screen:
            self.stack.removeWidget(self.final_test_screen)
            self.final_test_screen.deleteLater()

        self.final_test_screen = FinalTestScreen(self, self.lesson_index)
        self.stack.addWidget(self.final_test_screen)
        self.stack.setCurrentWidget(self.final_test_screen)
        self.logout_button.show()

    def _load_user_data(self):
        """Ładuje dane użytkownika"""
        print("Ładowanie danych użytkownika...")
        if hasattr(self, 'user_account') and self.user_account:
            try:
                print(f"Ścieżka pliku: {self.user_account.progress_file}")
                self.user_account.load_progress()
                print(f"Załadowane zadania: {len(self.user_account.completed_tasks)}")
            except Exception as e:
                print(f"Błąd ładowania: {e}")
                QMessageBox.warning(self, "Błąd", "Nie udało się załadować postępu")

    @property
    def user_progress(self):
        """Zwraca obiekt śledzący postęp użytkownika"""
        if hasattr(self, 'user_account') and self.user_account:
            return self.user_account
        return self._get_guest_account()

    def _get_guest_account(self):
        """Zwraca tymczasowe konto gościa"""
        if not hasattr(self, '_guest_account'):
            self._guest_account = UserAccount("guest")
        return self._guest_account

    def logout(self):
        """Wylogowuje użytkownika"""
        self.user_account = None
        self.achievement_system = None
        self.show_login_screen()
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany")

    def closeEvent(self, event):
        """Zapisuje postęp przed zamknięciem"""
        if hasattr(self, 'user_account') and self.user_account:
            self.user_account.save_progress()
        super().closeEvent(event)
from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget, QMessageBox
from app.views.menu_screen import MenuScreen
from app.views.lesson_screen import LessonScreen
from app.views.task_screen import TaskScreen
from app.views.final_test_screen import FinalTestScreen
from app.views.auth.login_screen import LoginScreen
from app.views.auth.register_screen import RegisterScreen
from app.models.auth.user_account import UserAccount
from app.features.achievements import AchievementSystem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODECRAFT")
        self.setMinimumSize(800, 600)

        # Inicjalizacja stanu aplikacji
        self.user_account = None
        self.achievement_system = None
        self.lesson_index = 1
        self.current_task_index = 0
        self._load_user_data()
        # Inicjalizacja ekranów
        self._init_screens()
        self._setup_ui()

        # Domyślnie pokazujemy ekran logowania
        self.show_login_screen()

    def _init_screens(self):
        """Inicjalizuje wszystkie ekrany aplikacji"""
        # Ekrany autentykacji
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)

        # Główne ekrany aplikacji
        self.menu_screen = MenuScreen(self)
        self.lesson_screen = None  # Będzie tworzony dynamicznie
        self.task_screen = TaskScreen(self)
        self.final_test_screen = None  # Będzie tworzony dynamicznie

    def _setup_ui(self):
        """Konfiguruje główny interfejs użytkownika"""
        central_widget = QWidget()
        self.stack = QStackedLayout()

        # Dodajemy wszystkie ekrany do stosu
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.register_screen)
        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.task_screen)

        central_widget.setLayout(self.stack)
        self.setCentralWidget(central_widget)

    def show_login_screen(self):
        """Pokazuje ekran logowania"""
        self.stack.setCurrentWidget(self.login_screen)

    def show_register_screen(self):
        """Pokazuje ekran rejestracji"""
        self.stack.setCurrentWidget(self.register_screen)

    def show_menu(self):
        """Pokazuje główne menu aplikacji"""
        # Inicjalizujemy system osiągnięć jeśli użytkownik jest zalogowany
        if self.user_account and not self.achievement_system:
            self.achievement_system = AchievementSystem(self.user_account.username)

        self.stack.setCurrentWidget(self.menu_screen)
        self.menu_screen.update_module_widgets()
        # Odświeżamy menu (np. stan przycisków)
        if hasattr(self.menu_screen, 'update_ui'):
            self.menu_screen.update_ui()

    def select_lesson(self, index):
        """Wybierz lekcję i przejdź do jej ekranu"""
        self.lesson_index = index
        self.current_task_index = 0
        self.show_lesson()

    def show_lesson(self):
        """Pokazuje ekran lekcji dla aktualnie wybranego modułu"""
        # Usuwamy poprzedni ekran lekcji jeśli istniał
        if self.lesson_screen:
            self.stack.removeWidget(self.lesson_screen)
            self.lesson_screen.deleteLater()

        # Tworzymy nowy ekran lekcji
        self.lesson_screen = LessonScreen(self, self.lesson_index)
        self.stack.addWidget(self.lesson_screen)
        self.stack.setCurrentWidget(self.lesson_screen)

    def show_task(self):
        """Pokazuje ekran zadania"""
        self.current_task_index = 0
        self.task_screen.update_task()
        self.stack.setCurrentWidget(self.task_screen)

    def previous_task(self):
        """Przechodzi do poprzedniego zadania"""
        if self.current_task_index > 0:
            self.current_task_index -= 1
            self.task_screen.update_task()

    def next_task(self):
        """Przechodzi do następnego zadania"""
        if self.current_task_index < len(self.task_screen.filtered_tasks) - 1:
            self.current_task_index += 1
            self.task_screen.update_task()

    def start_final_test(self):
        """Rozpoczyna test końcowy dla aktualnego modułu"""
        # Usuwamy poprzedni ekran testu jeśli istniał
        if self.final_test_screen:
            self.stack.removeWidget(self.final_test_screen)
            self.final_test_screen.deleteLater()

        # Tworzymy nowy ekran testu
        self.final_test_screen = FinalTestScreen(self, self.lesson_index)
        self.stack.addWidget(self.final_test_screen)
        self.stack.setCurrentWidget(self.final_test_screen)

    def _load_user_data(self):
        """Ładuje dane z dodatkowym loggingiem"""
        print("Ładowanie danych użytkownika...")  # Debug
        if hasattr(self, 'user_account') and self.user_account:
            try:
                print(f"Ścieżka pliku: {self.user_account.progress_file}")  # Debug
                self.user_account.load_progress()
                print(f"Zaladowane zadania: {len(self.user_account.completed_tasks)}")  # Debug
            except Exception as e:
                print(f"Krytyczny błąd ładowania: {e}")
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
        """Wylogowuje bieżącego użytkownika"""
        self.user_account = None
        self.achievement_system = None
        self.show_login_screen()
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany")

    def closeEvent(self, event):
        """Zapisuje postęp przed zamknięciem aplikacji"""
        if hasattr(self, 'user_account') and self.user_account:
            self.user_account.save_progress()
        super().closeEvent(event)
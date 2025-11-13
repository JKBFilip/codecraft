import traceback
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QWidget,
                               QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog)

# Importy widoków
from app.views.auth.login_screen import LoginScreen
from app.views.auth.register_screen import RegisterScreen
from app.models.auth.password_reset_screen import PasswordResetScreen
from app.views.menu_screen import MenuScreen
from app.views.lesson_screen import LessonScreen
from app.views.task_screen import TaskScreen
from app.views.final_test_screen import FinalTestScreen
from app.views.achievements_screen import AchievementsScreen
from app.views.final_exam_screen import FinalExamScreen

# Importy logiki
from app.models.auth.user_account import UserAccount


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODECRAFT")
        self.setMinimumSize(800, 600)

        # Inicjalizacja kluczowych atrybutów
        self.user_account = None
        self.lesson_index = 1
        self.current_task_index = 0

        # Ustawienie głównego layoutu i ekranów
        self._setup_layout_and_screens()

        # Ustawienie stanu początkowego
        self.show_login_screen()

    def _setup_layout_and_screens(self):
        # --- Główny kontener ---
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        # --- Górny pasek z przyciskiem wylogowania ---
        self.logout_button = QPushButton("Wyloguj")
        self._setup_logout_button()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.logout_button)
        self.main_layout.addLayout(top_bar_layout)

        # --- Kontener na przełączane ekrany (QStackedWidget) ---
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # --- INICJALIZACJA EKRANÓW (tworzone tylko raz!) ---
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.password_reset_screen = PasswordResetScreen(self)
        self.menu_screen = MenuScreen(self)
        self.task_screen = TaskScreen(self)  # TaskScreen jest generyczny, tworzymy go raz
        self.final_exam_screen = FinalExamScreen(self)  # Egzamin też tworzymy raz

        # Ekran osiągnięć jest tworzony raz, ale na początku może nie mieć użytkownika
        self.achievements_screen = AchievementsScreen(self)

        # Ekrany, które zależą od dynamicznych danych (jak lesson_index), zostawiamy jako None
        self.lesson_screen = None
        self.final_test_screen = None

        # --- Dodanie ekranów do "stosu" ---
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.register_screen)
        self.stack.addWidget(self.password_reset_screen)
        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.task_screen)
        self.stack.addWidget(self.achievements_screen)
        self.stack.addWidget(self.final_exam_screen)

    def _setup_logout_button(self):
        """Konfiguruje wygląd i działanie przycisku wylogowania."""
        self.logout_button.setStyleSheet("""
            QPushButton { padding: 5px; background-color: #f44336; color: white;
                          border-radius: 4px; max-width: 100px; }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.logout_button.clicked.connect(self.logout)

    # --- METODY DO NAWIGACJI I ZARZĄDZANIA WIDOKAMI ---

    def show_login_screen(self):
        self.stack.setCurrentWidget(self.login_screen)
        self.logout_button.hide()

    def show_register_screen(self):
        self.stack.setCurrentWidget(self.register_screen)
        self.logout_button.hide()

    def show_password_reset_screen(self):
        self.stack.setCurrentWidget(self.password_reset_screen)
        self.logout_button.hide()

    def show_menu(self):
        if self.user_account:
            # Zawsze odświeżaj dane w menu przed jego pokazaniem
            self.menu_screen.update_module_widgets()
            self.achievements_screen.user_account = self.user_account
        self.stack.setCurrentWidget(self.menu_screen)
        self.logout_button.show()

    def show_achievements(self):
        if self.user_account and self.achievements_screen:
            # Mówimy ekranowi, aby sam odświeżył swój wygląd
            self.achievements_screen.refresh_achievements()
            self.stack.setCurrentWidget(self.achievements_screen)
            self.logout_button.show()

    def select_lesson(self, index):
        """Ustawia wybrany moduł i przechodzi do ekranu lekcji."""
        self.lesson_index = index
        self.current_task_index = 0
        self.show_lesson()

    def show_lesson(self):
        """Tworzy i pokazuje ekran lekcji dla aktualnie wybranego modułu."""
        # Ten ekran, zależny od `lesson_index`, tworzymy dynamicznie
        if self.lesson_screen:
            self.stack.removeWidget(self.lesson_screen)
            self.lesson_screen.deleteLater()

        self.lesson_screen = LessonScreen(self, self.lesson_index)
        self.stack.addWidget(self.lesson_screen)
        self.stack.setCurrentWidget(self.lesson_screen)
        self.logout_button.show()

    def show_task(self):
        """Pokazuje ekran zadań i aktualizuje go do bieżącego zadania."""
        self.task_screen.update_task()
        self.stack.setCurrentWidget(self.task_screen)
        self.logout_button.show()

    def start_final_test(self):
        """Tworzy i pokazuje ekran testu dla aktualnie wybranego modułu."""
        if self.final_test_screen:
            self.stack.removeWidget(self.final_test_screen)
            self.final_test_screen.deleteLater()

        self.final_test_screen = FinalTestScreen(self, self.lesson_index)
        self.stack.addWidget(self.final_test_screen)
        self.stack.setCurrentWidget(self.final_test_screen)
        self.logout_button.show()

    def show_final_exam(self):
        """Sprawdza warunki i pokazuje ekran egzaminu końcowego."""
        if not self.user_account:
            QMessageBox.warning(self, "Błąd", "Musisz być zalogowany, aby przystąpić do egzaminu.")
            return

        if not self.user_account.are_all_modules_completed():
            QMessageBox.warning(self, "Nieukończone moduły",
                                "Musisz ukończyć wszystkie moduły (zadania + testy) przed przystąpieniem do egzaminu!")
            return

        # Po prostu pokazujemy ekran, który już istnieje
        self.stack.setCurrentWidget(self.final_exam_screen)
        self.logout_button.show()
        self.final_exam_screen.prepare_and_display()
        self.stack.setCurrentWidget(self.final_exam_screen)

    def show_cheat_code_prompt(self):
        """Wyświetla okienko do wpisania kodu."""
        if not self.user_account:
            QMessageBox.warning(self, "Błąd", "Musisz być zalogowany, aby używać kodów.")
            return

        # Wyświetlamy proste okienko dialogowe
        code, ok = QInputDialog.getText(self, "Kody", "Wprowadź kod:")

        if ok and code:
            # Jeśli użytkownik coś wpisał i kliknął OK, przekazujemy kod do UserAccount
            result_message = self.user_account.apply_cheat_code(code)

            # Pokazujemy wynik operacji
            QMessageBox.information(self, "Wynik kodu", result_message)

            # Odświeżamy widok menu, aby pokazać zmiany (np. odblokowane moduły)
            self.show_menu()

    # --- METODY POMOCNICZE I ZARZĄDZANIE DANYMI ---

    @property
    def user_progress(self):
        """Zapewnia dostęp do postępu zalogowanego użytkownika lub gościa."""
        return self.user_account if self.user_account else self._get_guest_account()

    def _get_guest_account(self):
        """Tworzy tymczasowe konto gościa, jeśli nie jest zalogowany żaden użytkownik."""
        if not hasattr(self, '_guest_account'):
            self._guest_account = UserAccount("guest")
        return self._guest_account

    def logout(self):
        """Wylogowuje użytkownika i wraca do ekranu logowania."""
        if self.user_account:
            self.user_account.save_progress()  # Zapisz postęp przed wylogowaniem
        self.user_account = None
        self.show_login_screen()
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany.")

    def closeEvent(self, event):
        """Zapisuje postęp przy zamykaniu aplikacji."""
        if self.user_account:
            self.user_account.save_progress()
        super().closeEvent(event)

    def previous_task(self):
        """Przełącza na poprzednie zadanie w bieżącym module."""
        if self.current_task_index > 0:
            self.current_task_index -= 1
            self.task_screen.update_task()

    def next_task(self):
        """Przełącza na następne zadanie w bieżącym module."""
        # Upewniamy się, że mamy dostęp do listy zadań, aby uniknąć błędu
        if hasattr(self.task_screen, 'filtered_tasks'):
            if self.current_task_index < len(self.task_screen.filtered_tasks) - 1:
                self.current_task_index += 1
                self.task_screen.update_task()
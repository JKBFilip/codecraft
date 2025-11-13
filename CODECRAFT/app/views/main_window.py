import traceback
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QWidget,
                               QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog)

from app.views.auth.login_screen import LoginScreen
from app.views.auth.register_screen import RegisterScreen
from app.models.auth.password_reset_screen import PasswordResetScreen
from app.views.menu_screen import MenuScreen
from app.views.lesson_screen import LessonScreen
from app.views.task_screen import TaskScreen
from app.views.final_test_screen import FinalTestScreen
from app.views.achievements_screen import AchievementsScreen
from app.views.final_exam_screen import FinalExamScreen
from app.models.auth.user_account import UserAccount

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODECRAFT")
        self.setMinimumSize(800, 600)

        self.user_account = None
        self.lesson_index = 1
        self.current_task_index = 0

        self._setup_layout_and_screens()
        self.show_login_screen()

    def _setup_layout_and_screens(self):
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        self.logout_button = QPushButton("Wyloguj")
        self._setup_logout_button()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.logout_button)
        self.main_layout.addLayout(top_bar_layout)

        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.password_reset_screen = PasswordResetScreen(self)
        self.menu_screen = MenuScreen(self)
        self.task_screen = TaskScreen(self)
        self.final_exam_screen = FinalExamScreen(self)
        self.achievements_screen = AchievementsScreen(self)

        self.lesson_screen = None
        self.final_test_screen = None

        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.register_screen)
        self.stack.addWidget(self.password_reset_screen)
        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.task_screen)
        self.stack.addWidget(self.achievements_screen)
        self.stack.addWidget(self.final_exam_screen)

    def _setup_logout_button(self):
        self.logout_button.setStyleSheet("""
            QPushButton { padding: 5px; background-color: #f44336; color: white;
                          border-radius: 4px; max-width: 100px; }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.logout_button.clicked.connect(self.logout)

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
            self.menu_screen.update_module_widgets()
            self.achievements_screen.user_account = self.user_account
        self.stack.setCurrentWidget(self.menu_screen)
        self.logout_button.show()

    def show_achievements(self):
        if self.user_account and self.achievements_screen:
            self.achievements_screen.refresh_achievements()
            self.stack.setCurrentWidget(self.achievements_screen)
            self.logout_button.show()

    def select_lesson(self, index):
        self.lesson_index = index
        self.current_task_index = 0
        self.show_lesson()

    def show_lesson(self):
        if self.lesson_screen:
            self.stack.removeWidget(self.lesson_screen)
            self.lesson_screen.deleteLater()

        self.lesson_screen = LessonScreen(self, self.lesson_index)
        self.stack.addWidget(self.lesson_screen)
        self.stack.setCurrentWidget(self.lesson_screen)
        self.logout_button.show()

    def show_task(self):
        self.task_screen.update_task()
        self.stack.setCurrentWidget(self.task_screen)
        self.logout_button.show()

    def start_final_test(self):
        if self.final_test_screen:
            self.stack.removeWidget(self.final_test_screen)
            self.final_test_screen.deleteLater()

        self.final_test_screen = FinalTestScreen(self, self.lesson_index)
        self.stack.addWidget(self.final_test_screen)
        self.stack.setCurrentWidget(self.final_test_screen)
        self.logout_button.show()

    def show_final_exam(self):
        if not self.user_account:
            QMessageBox.warning(self, "Błąd", "Musisz być zalogowany, aby przystąpić do egzaminu.")
            return

        if not self.user_account.are_all_modules_completed():
            QMessageBox.warning(self, "Nieukończone moduły",
                                "Musisz ukończyć wszystkie moduły (zadania + testy) przed przystąpieniem do egzaminu!")
            return

        self.final_exam_screen.prepare_and_display()
        self.stack.setCurrentWidget(self.final_exam_screen)
        self.logout_button.show()

    def show_cheat_code_prompt(self):
        if not self.user_account:
            QMessageBox.warning(self, "Błąd", "Musisz być zalogowany, aby używać kodów.")
            return

        code, ok = QInputDialog.getText(self, "Kody", "Wprowadź kod:")

        if ok and code:
            result_message = self.user_account.apply_cheat_code(code)
            QMessageBox.information(self, "Wynik kodu", result_message)
            self.show_menu()

    @property
    def user_progress(self):
        return self.user_account if self.user_account else self._get_guest_account()

    def _get_guest_account(self):
        if not hasattr(self, '_guest_account'):
            self._guest_account = UserAccount("guest")
        return self._guest_account

    def logout(self):
        if self.user_account:
            self.user_account.save_progress()
        self.user_account = None
        self.show_login_screen()
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany.")

    def closeEvent(self, event):
        if self.user_account:
            self.user_account.save_progress()
        super().closeEvent(event)

    def previous_task(self):
        if self.current_task_index > 0:
            self.current_task_index -= 1
            self.task_screen.update_task()

    def next_task(self):
        if hasattr(self.task_screen, 'filtered_tasks'):
            if self.current_task_index < len(self.task_screen.filtered_tasks) - 1:
                self.current_task_index += 1
                self.task_screen.update_task()
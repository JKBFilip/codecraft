import traceback
from PySide6.QtWidgets import (QMainWindow, QStackedLayout, QWidget,
                              QMessageBox, QVBoxLayout, QHBoxLayout,
                              QPushButton)
from app.models.auth.password_reset_screen import PasswordResetScreen
from app.views.final_exam_screen import FinalExamScreen
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
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)
        self.logout_button = QPushButton("Wyloguj")
        self._setup_logout_button()
        self.top_bar = QWidget()
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.logout_button)
        self.top_bar.setLayout(self.top_bar_layout)
        self.main_layout.addWidget(self.top_bar)
        self.stack_container = QWidget()
        self.stack = QStackedLayout()
        self.stack_container.setLayout(self.stack)
        self.main_layout.addWidget(self.stack_container)
        self.user_account = None
        self.achievement_system = None
        self.lesson_index = 1
        self.current_task_index = 0
        self._init_screens()
        self._setup_ui()
        self.password_reset_screen = PasswordResetScreen(self)
        self.stack.addWidget(self.password_reset_screen)
        self.show_login_screen()

    def _setup_logout_button(self):
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
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.menu_screen = MenuScreen(self)
        self.lesson_screen = None
        self.task_screen = None
        self.final_test_screen = None
        self.achievements_screen = None

    def _setup_ui(self):
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.register_screen)
        self.stack.addWidget(self.menu_screen)

    def show_login_screen(self):
        self.stack.setCurrentWidget(self.login_screen)
        self.logout_button.hide()

    def show_register_screen(self):
        self.stack.setCurrentWidget(self.register_screen)
        self.logout_button.hide()

    def show_menu(self):
        if self.user_account:
            new_achievements = self.user_account.check_achievements()
            for achievement in new_achievements:
                print(f"Nowe osiągnięcie: {achievement.name}")
            if self.achievements_screen:
                self.achievements_screen.refresh_achievements()

        self.stack.setCurrentWidget(self.menu_screen)
        self.logout_button.show()
        self.menu_screen.update_module_widgets()

    def show_achievements(self):
        if not self.user_account:
            return

        self.achievements_screen = AchievementsScreen(self.user_account, self)
        old_widget = self.stack.indexOf(self.achievements_screen)
        if old_widget >= 0:
            widget_to_remove = self.stack.widget(old_widget)
            self.stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        self.stack.addWidget(self.achievements_screen)
        self.stack.setCurrentWidget(self.achievements_screen)
        self.logout_button.show()

    def _check_user_achievements(self):
        if not hasattr(self, '_achievement_system'):
            self._achievement_system = AchievementSystem(self.user_account)

        unlocked = []
        for achievement in self._achievement_system.achievements:
            if achievement.id not in self.user_account.unlocked_achievements:
                if achievement.condition_fn(self.user_account):
                    self.user_account.unlocked_achievements.add(achievement.id)
                    unlocked.append(achievement)
                    self.user_account.save_progress()
        return unlocked

    def show_achievement_notification(self, achievements):
        if not isinstance(achievements, list):
            achievements = [achievements]

        for achievement in achievements:
            print(f"Nowe osiągnięcie: {achievement.name}")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Nowe osiągnięcie!")
            msg.setText(f"Odblokowano: {achievement.name}\n{achievement.description}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    def select_lesson(self, index):
        print(f"\nWybrałeś lekcję {index}")
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

    def init_task_screen(self):
        if not self.task_screen:
            self.task_screen = TaskScreen(self)
            self.stack.addWidget(self.task_screen)

    def show_task(self):
        self.init_task_screen()
        self.task_screen.update_task()
        self.stack.setCurrentWidget(self.task_screen)
        self.logout_button.show()

    def previous_task(self):
        if hasattr(self, 'current_task_index') and self.current_task_index > 0:
            self.current_task_index -= 1
            self.task_screen.update_task()

    def next_task(self):
        if (hasattr(self, 'current_task_index') and
                hasattr(self, 'task_screen') and
                self.current_task_index < len(self.task_screen.filtered_tasks) - 1):
            self.current_task_index += 1
            self.task_screen.update_task()

    def start_final_test(self):
        if self.final_test_screen:
            self.stack.removeWidget(self.final_test_screen)
            self.final_test_screen.deleteLater()
        self.final_test_screen = FinalTestScreen(self, self.lesson_index)
        self.stack.addWidget(self.final_test_screen)
        self.stack.setCurrentWidget(self.final_test_screen)
        self.logout_button.show()

    def _load_user_data(self):
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
        if hasattr(self, 'user_account') and self.user_account:
            return self.user_account
        return self._get_guest_account()

    def _get_guest_account(self):
        if not hasattr(self, '_guest_account'):
            self._guest_account = UserAccount("guest")
        return self._guest_account

    def logout(self):
        self.user_account = None
        self.achievement_system = None
        self.show_login_screen()
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany")

    def closeEvent(self, event):
        if hasattr(self, 'user_account') and self.user_account:
            self.user_account.save_progress()
        super().closeEvent(event)

    def show_final_exam(self):
        try:
            if not hasattr(self, 'user_account') or not self.user_account:
                QMessageBox.warning(self, "Błąd", "Musisz być zalogowany, aby przystąpić do egzaminu")
                return

            if not self.user_account.are_all_modules_completed():
                QMessageBox.warning(self, "Nieukończone moduły",
                                    "Musisz ukończyć wszystkie moduły (zadania + testy) przed przystąpieniem do egzaminu końcowego!")
                return

            if hasattr(self, 'final_exam_screen'):
                self.stack.removeWidget(self.final_exam_screen)
                self.final_exam_screen.deleteLater()

            self.final_exam_screen = FinalExamScreen(self)
            self.stack.addWidget(self.final_exam_screen)
            self.stack.setCurrentWidget(self.final_exam_screen)
            self.logout_button.show()

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się rozpocząć egzaminu:\n{str(e)}")
            print(f"Błąd podczas tworzenia egzaminu: {traceback.format_exc()}")
import traceback
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QWidget,
                               QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog, QApplication)
from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtCore import Qt

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

# --- NOWE IMPORTY DLA GIER I PLAYGROUND ---
from app.views.retro_console_screen import RetroConsoleScreen
from app.views.retrogames_splash.pong_info_screen import PongInfoScreen
from app.views.retrogames_splash.space_invaders_info_screen import SpaceInvadersInfoScreen
from app.views.retrogames_splash.snake_info_screen import SnakeInfoScreen  # <-- DODANO
from app.views.playground_screen import PlaygroundScreen  # <-- DODANO


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODECRAFT")
        self.setMinimumSize(800, 600)

        # Inicjalizacja TTS
        self.tts = None
        self._init_tts()

        self.user_account = None
        self.lesson_index = 1
        self.current_task_index = 0
        self.is_dark_mode = True

        # WAŻNE: Najpierw setup layoutu (tworzy self.stack), potem reszta
        self._setup_layout_and_screens()
        self._apply_theme()
        self.show_login_screen()

    def _init_tts(self):
        """Inicjalizuje silnik mowy w bezpieczny sposób."""
        try:
            engines = QTextToSpeech.availableEngines()
            print(f"TTS GLOBAL: Dostępne silniki: {engines}")

            if 'sapi' in engines:
                self.tts = QTextToSpeech("sapi", self)
            elif 'winrt' in engines:
                self.tts = QTextToSpeech("winrt", self)
            else:
                self.tts = QTextToSpeech(self)

            if self.tts:
                self.tts.setVolume(1.0)
                # Próba ustawienia polskiego głosu
                for voice in self.tts.availableVoices():
                    name = voice.name().lower()
                    if "pl" in voice.locale().name().lower() or "pol" in name or "paulina" in name:
                        self.tts.setVoice(voice)
                        print(f"TTS GLOBAL: Wybrano głos: {voice.name()}")
                        break
        except Exception as e:
            print(f"TTS INIT ERROR: {e}")

    def read_text(self, text):
        if not self.tts: return
        if self.tts.state() == QTextToSpeech.State.Speaking:
            self.tts.stop()
        clean_text = self._clean_text_for_tts(text)
        try:
            print(f"DEBUG TTS: Czytam: '{clean_text[:30]}...'")
            self.tts.say(clean_text)
        except Exception as e:
            print(f"TTS READ ERROR: {e}")

    def stop_reading(self):
        if self.tts and self.tts.state() == QTextToSpeech.State.Speaking:
            try:
                self.tts.stop()
            except Exception:
                pass

    def _clean_text_for_tts(self, text):
        text = text.replace("<br>", ". ").replace("<b>", "").replace("</b>", "").replace("<h2>", "").replace("</h2>",
                                                                                                             "")
        text = text.replace("<ul>", "").replace("</ul>", "").replace("<li>", "").replace("</li>", ". ")
        text = text.replace("<pre><code>", "").replace("</code></pre>", "")
        emojis = ["📦", "✅", "❌", "🤔", "🤷", "🚦", "⚖️", "🔁", "♾️", "🔧", "📚", "✏️", "🤝", "🗣️", "⚙️", "➡️", "🔢", "`", "🚀",
                  "💻", "🏠", "🔙", "📄", "🕹️", "👾", "🏓", "🐍"]
        for e in emojis: text = text.replace(e, "")
        return text

    def _setup_layout_and_screens(self):
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        # Górny pasek
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 10, 10, 0)

        # Przycisk Motywu
        self.theme_button = QPushButton("🌓")
        self.theme_button.setFixedSize(60, 60)
        self.theme_button.setToolTip("Zmień motyw")
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setObjectName("secondaryButton")
        self.theme_button.setStyleSheet("font-size: 32px; border-radius: 10px; border: 2px solid #6200ea;")

        top_bar_layout.addWidget(self.theme_button)
        top_bar_layout.addStretch()

        self.logout_button = QPushButton("Wyloguj")
        self._setup_logout_button()
        top_bar_layout.addWidget(self.logout_button)

        self.main_layout.addLayout(top_bar_layout)

        # Stack ekranów - TWORZONY TUTAJ
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Inicjalizacja ekranów
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.password_reset_screen = PasswordResetScreen(self)
        self.menu_screen = MenuScreen(self)
        self.task_screen = TaskScreen(self)
        self.final_exam_screen = FinalExamScreen(self)
        self.achievements_screen = AchievementsScreen(self)

        # --- EKRANY GIER I PLAYGROUND ---
        self.retro_console_screen = RetroConsoleScreen(self)
        self.pong_info_screen = PongInfoScreen(self)
        self.space_invaders_info_screen = SpaceInvadersInfoScreen(self)
        self.snake_info_screen = SnakeInfoScreen(self)  # <-- DODANO
        self.playground_screen = PlaygroundScreen(self)  # <-- Inicjalizacja Playground
        # --------------------------------

        self.lesson_screen = None
        self.final_test_screen = None

        # Dodawanie do stacka
        self.stack.addWidget(self.login_screen)
        self.stack.addWidget(self.register_screen)
        self.stack.addWidget(self.password_reset_screen)
        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.task_screen)
        self.stack.addWidget(self.achievements_screen)
        self.stack.addWidget(self.final_exam_screen)
        self.stack.addWidget(self.retro_console_screen)
        self.stack.addWidget(self.pong_info_screen)
        self.stack.addWidget(self.space_invaders_info_screen)
        self.stack.addWidget(self.snake_info_screen)  # <-- DODANO DO STACKA
        self.stack.addWidget(self.playground_screen)  # <-- Dodanie do stacka

    def _setup_logout_button(self):
        self.logout_button.setStyleSheet("""
            QPushButton { padding: 5px; background-color: #f44336; color: white;
                          border-radius: 4px; max-width: 100px; font-weight: bold; }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        self.logout_button.clicked.connect(self.logout)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self._apply_theme()

    def _apply_theme(self):
        style_path = "app/assets/style.qss" if self.is_dark_mode else "app/assets/style_light.qss"
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku stylu {style_path}")

    # --- NAWIGACJA ---

    def show_login_screen(self):
        self.stack.setCurrentWidget(self.login_screen)
        self.logout_button.hide()
        self.theme_button.setVisible(True)

    def show_register_screen(self):
        self.stack.setCurrentWidget(self.register_screen)
        self.logout_button.hide()

    def show_password_reset_screen(self):
        self.stack.setCurrentWidget(self.password_reset_screen)
        self.logout_button.hide()

    def show_menu(self):
        self.stop_reading()
        if self.user_account:
            self.menu_screen.update_module_widgets()
            self.achievements_screen.user_account = self.user_account
        self.stack.setCurrentWidget(self.menu_screen)
        self.logout_button.show()

    def show_achievements(self):
        self.stop_reading()
        if self.user_account and self.achievements_screen:
            self.achievements_screen.refresh_achievements()
            self.stack.setCurrentWidget(self.achievements_screen)
            self.logout_button.show()

    def show_retro_console(self):
        self.stop_reading()
        if self.retro_console_screen:
            self.retro_console_screen.refresh_state()
            self.stack.setCurrentWidget(self.retro_console_screen)
            self.logout_button.show()

    def show_pong_info(self):
        self.stop_reading()
        self.stack.setCurrentWidget(self.pong_info_screen)
        self.logout_button.show()

    def show_space_invaders_info(self):
        self.stop_reading()
        self.stack.setCurrentWidget(self.space_invaders_info_screen)
        self.logout_button.show()

    def show_snake_info(self):  # <-- DODANO METODĘ NAWIGACJI
        self.stop_reading()
        self.stack.setCurrentWidget(self.snake_info_screen)
        self.logout_button.show()

    def show_playground(self):  # <-- Metoda do pokazywania Playground
        self.stop_reading()
        self.stack.setCurrentWidget(self.playground_screen)
        self.logout_button.show()

    def select_lesson(self, index):
        self.lesson_index = index;
        self.current_task_index = 0;
        self.show_lesson()

    def show_lesson(self):
        self.stop_reading()
        if self.lesson_screen: self.stack.removeWidget(self.lesson_screen); self.lesson_screen.deleteLater()
        self.lesson_screen = LessonScreen(self, self.lesson_index)
        self.stack.addWidget(self.lesson_screen);
        self.stack.setCurrentWidget(self.lesson_screen);
        self.logout_button.show()

    def show_task(self):
        self.stop_reading()
        self.task_screen.update_task()
        self.stack.setCurrentWidget(self.task_screen);
        self.logout_button.show()

    def start_final_test(self):
        self.stop_reading()
        if self.final_test_screen: self.stack.removeWidget(self.final_test_screen); self.final_test_screen.deleteLater()
        self.final_test_screen = FinalTestScreen(self, self.lesson_index)
        self.stack.addWidget(self.final_test_screen);
        self.stack.setCurrentWidget(self.final_test_screen);
        self.logout_button.show()

    def show_final_exam(self):
        self.stop_reading()
        if not self.user_account: QMessageBox.warning(self, "Błąd", "Zaloguj się."); return
        if not self.user_account.are_all_modules_completed(): QMessageBox.warning(self, "Błąd",
                                                                                  "Ukończ moduły."); return
        self.final_exam_screen.prepare_and_display()
        self.stack.setCurrentWidget(self.final_exam_screen);
        self.logout_button.show()

    def show_cheat_code_prompt(self):
        if not self.user_account: QMessageBox.warning(self, "Błąd", "Zaloguj się."); return
        code, ok = QInputDialog.getText(self, "Kody", "Wprowadź kod:")
        if ok and code:
            msg = self.user_account.apply_cheat_code(code)
            QMessageBox.information(self, "Wynik", msg);
            self.show_menu()

    @property
    def user_progress(self):
        return self.user_account if self.user_account else self._get_guest_account()

    def _get_guest_account(self):
        if not hasattr(self, '_guest_account'): self._guest_account = UserAccount("guest")
        return self._guest_account

    def logout(self):
        self.stop_reading()
        if self.user_account: self.user_account.save_progress()
        self.user_account = None;
        self.show_login_screen()
        QMessageBox.information(self, "Wylogowano", "Zostałeś pomyślnie wylogowany.")

    def closeEvent(self, event):
        self.stop_reading()
        if self.user_account: self.user_account.save_progress()
        super().closeEvent(event)

    def previous_task(self):
        if self.current_task_index > 0: self.current_task_index -= 1; self.task_screen.update_task()

    def next_task(self):
        if hasattr(self.task_screen, 'filtered_tasks'):
            if self.current_task_index < len(
                self.task_screen.filtered_tasks) - 1: self.current_task_index += 1; self.task_screen.update_task()
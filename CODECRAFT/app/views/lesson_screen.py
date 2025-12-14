import webbrowser
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QTextEdit, QSizePolicy, QDialog, QTextBrowser, QMessageBox, QStackedWidget, QScrollArea,
                               QFrame)
from PySide6.QtGui import QFont, QTextDocument
from PySide6.QtCore import Qt, QTimer
from PySide6.QtTextToSpeech import QTextToSpeech

# Importujemy dane i helpery z nowego modułu
from app.data.lesson_content import get_lesson_data, get_programmer_task

# --- ZMIENNA GLOBALNA DLA TTS (Singleton) ---
_global_tts_engine = None


def get_tts_engine():
    global _global_tts_engine
    if _global_tts_engine is None:
        try:
            engines = QTextToSpeech.availableEngines()
            print(f"TTS GLOBAL: Dostępne silniki: {engines}")
            if 'sapi' in engines:
                _global_tts_engine = QTextToSpeech("sapi", None)
            elif 'winrt' in engines:
                _global_tts_engine = QTextToSpeech("winrt", None)
            else:
                _global_tts_engine = QTextToSpeech(None)

            if _global_tts_engine:
                _global_tts_engine.setVolume(1.0)
                for voice in _global_tts_engine.availableVoices():
                    if any(x in voice.name().lower() for x in ['pl', 'pol', 'paulina']):
                        _global_tts_engine.setVoice(voice)
                        break
        except Exception as e:
            print(f"TTS INIT ERROR: {e}")
    return _global_tts_engine


# --------------------------------------------

# Klasy pomocnicze UI (Dialogi)
class CodeViewerDialog(QDialog):
    def __init__(self, code_string, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rozwiązanie Zadania")
        self.setMinimumSize(600, 400)
        layout = QVBoxLayout(self)
        code_edit = QTextEdit()
        code_edit.setReadOnly(True)
        code_edit.setPlainText(code_string.strip())
        code_edit.setFont(QFont("Consolas", 11))
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.accept)
        layout.addWidget(code_edit)
        layout.addWidget(close_button)


class ProgrammerTaskDialog(QDialog):
    def __init__(self, instruction, solution, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zadanie Programisty")
        self.setMinimumSize(700, 500)
        self.solution = solution
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        self.instruction_browser = QTextBrowser()
        self.instruction_browser.setOpenExternalLinks(True)
        self.instruction_browser.setHtml(
            instruction + '<br><p>Przetestuj swój kod w <a href="https://www.online-python.com" target="_blank">Edytorze Online</a>.</p>')
        layout.addWidget(self.instruction_browser)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.solution_button = QPushButton("💡 Pokaż rozwiązanie")
        self.solution_button.setObjectName("secondaryButton")
        self.solution_button.clicked.connect(self.show_solution)
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.solution_button)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def show_solution(self):
        dialog = CodeViewerDialog(self.solution, self)
        dialog.exec()


# --- GŁÓWNA KLASA EKRANU LEKCJI ---

class LessonScreen(QWidget):
    def __init__(self, main_window, lesson_index):
        super().__init__()
        self.main_window = main_window
        self.lesson_index = lesson_index
        self.page = 0

        # Pobieramy dane z nowego modułu
        self.theory_pages = get_lesson_data(lesson_index)

        self.tts = get_tts_engine()
        self.init_ui()

    def closeEvent(self, event):
        self.stop_tts_safe()
        super().closeEvent(event)

    def hideEvent(self, event):
        self.stop_tts_safe()
        super().hideEvent(event)

    def init_ui(self):
        # Główny layout (zewnętrzny) - nie przewijany
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. NAGŁÓWEK (Stały, zawsze widoczny)
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)

        self.title_label = QLabel(f"📖 Lekcja {self.lesson_index}: Teoria")
        self.title_label.setObjectName("lessonTitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.title_label)

        self.tts_button = QPushButton("🔊")
        self.tts_button.setFixedSize(60, 60)
        self.tts_button.setToolTip("Odsłuchaj stronę")
        self.tts_button.setObjectName("secondaryButton")
        self.tts_button.clicked.connect(self.toggle_speech)
        self.tts_button.setStyleSheet("font-size: 32px; border-radius: 10px; border: 2px solid #6200ea;")
        header_layout.addWidget(self.tts_button)

        main_layout.addWidget(header_widget)

        # 2. SCROLL AREA (Przewijana treść)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 10, 20, 20)
        self.scroll_layout.setSpacing(20)

        # --- A. STACK Z TREŚCIĄ (Tekst lub Gra) ---
        self.content_stack = QStackedWidget()
        self.content_stack.setMinimumHeight(400)
        self.content_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.scroll_layout.addWidget(self.content_stack)

        # --- B. NAWIGACJA (Dalej/Wstecz) ---
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Poprzednie")
        self.prev_button.clicked.connect(self.prev_page)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Następna ➡️")
        self.next_button.clicked.connect(self.next_page)
        nav_layout.addWidget(self.next_button)

        self.scroll_layout.addLayout(nav_layout)

        # --- C. PRZYCISKI AKCJI (Pojawiają się na dole) ---
        self.actions_layout = QVBoxLayout()
        self.actions_layout.setSpacing(10)

        self.task_button = QPushButton("✍️ Przejdź do zadań")
        self.task_button.setObjectName("taskButton")
        self.task_button.setMinimumHeight(50)
        self.task_button.clicked.connect(lambda: self.main_window.show_task())
        self.actions_layout.addWidget(self.task_button)

        self.programmer_task_button = QPushButton("💻 Zadanie Programisty (Opcjonalne)")
        self.programmer_task_button.setObjectName("secondaryButton")
        self.programmer_task_button.setMinimumHeight(50)
        self.programmer_task_button.clicked.connect(self.show_programmer_task)
        self.actions_layout.addWidget(self.programmer_task_button)

        self.test_button = QPushButton("🚀 Rozpocznij test modułu")
        self.test_button.setObjectName("finalTestButton")
        self.test_button.setMinimumHeight(50)
        self.test_button.clicked.connect(lambda: self.main_window.start_final_test())
        self.actions_layout.addWidget(self.test_button)

        self.scroll_layout.addLayout(self.actions_layout)
        self.scroll_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # 3. STOPKA
        footer_widget = QWidget()
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setContentsMargins(20, 10, 20, 20)

        self.menu_button = QPushButton("🏠 Powrót do menu")
        self.menu_button.clicked.connect(self.back_to_menu)
        footer_layout.addWidget(self.menu_button)

        main_layout.addWidget(footer_widget)

        self.update_page()

    def toggle_speech(self):
        if not self.tts: return
        if self.tts.state() == QTextToSpeech.State.Speaking:
            self.stop_tts_safe()
        else:
            self.read_current_page()

    def clean_text_for_tts(self, text):
        emojis = ["📦", "✅", "❌", "🤔", "🤷", "🚦", "⚖️", "🔁", "♾️", "🔧", "📚", "✏️", "🤝", "🗣️", "⚙️", "➡️", "🔢", "`"]
        for e in emojis: text = text.replace(e, "")
        return text

    def read_current_page(self):
        if not self.tts or self.page >= len(self.theory_pages): return
        page_data = self.theory_pages[self.page]

        if page_data.get("type") == "html":
            try:
                doc = QTextDocument()
                doc.setHtml(page_data["content"])
                plain_text = doc.toPlainText()

                safe_text = self.clean_text_for_tts(plain_text)

                print(f"DEBUG TTS: Czytam (bezpieczny tekst): '{safe_text[:50]}...'")
                self.tts.say(safe_text)
            except Exception as e:
                print(f"TTS ERROR: {e}")
        else:
            print("DEBUG TTS: Strona zawiera grę, pomijam czytanie.")

    def stop_tts_safe(self):
        if self.tts:
            try:
                if self.tts.state() == QTextToSpeech.State.Speaking:
                    self.tts.stop()
            except Exception:
                pass

    def update_page(self):
        self.stop_tts_safe()
        QTimer.singleShot(100, self._perform_page_update)

    def _perform_page_update(self):
        if self.page < 0 or self.page >= len(self.theory_pages): return

        current = self.content_stack.currentWidget()
        if current:
            self.content_stack.removeWidget(current)
            current.deleteLater()

        page_data = self.theory_pages[self.page]
        page_type = page_data.get("type", "html")

        if page_type == "html":
            text_viewer = QTextBrowser()
            text_viewer.setReadOnly(True)
            text_viewer.setOpenExternalLinks(True)
            text_viewer.setHtml(page_data["content"])
            font = text_viewer.font()
            font.setPointSize(12)
            text_viewer.setFont(font)
            text_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

            self.content_stack.addWidget(text_viewer)
            self.content_stack.setCurrentWidget(text_viewer)
            self.tts_button.setEnabled(True)

        elif page_type == "widget":
            # --- POPRAWKA CRASH ---
            # Pobieramy obiekt content (może być instancją lub klasą)
            content_obj = page_data.get("content")
            game_widget = None

            # Jeśli w danych jest przekazana KLASA (type), tworzymy instancję
            if isinstance(content_obj, type):
                game_widget = content_obj(self)

            # Jeśli w danych jest przekazana INSTANCJA (QWidget), która mogła zostać usunięta
            elif isinstance(content_obj, QWidget):
                # Bierzemy jej klasę i tworzymy NOWĄ, świeżą instancję
                GameClass = content_obj.__class__
                game_widget = GameClass(self)

            if game_widget:
                self.content_stack.addWidget(game_widget)
                self.content_stack.setCurrentWidget(game_widget)
                self.tts_button.setEnabled(False)

        self.prev_button.setEnabled(self.page > 0)
        self.next_button.setEnabled(self.page < len(self.theory_pages) - 1)

        is_last_page = self.page == len(self.theory_pages) - 1

        self.task_button.setVisible(is_last_page)
        self.test_button.setVisible(is_last_page)
        self.programmer_task_button.setVisible(is_last_page)

        self.scroll_area.verticalScrollBar().setValue(0)

    def prev_page(self):
        self.stop_tts_safe()
        if self.page > 0: self.page -= 1; self.update_page()

    def next_page(self):
        self.stop_tts_safe()
        if self.page < len(self.theory_pages) - 1: self.page += 1; self.update_page()

    def back_to_menu(self):
        self.stop_tts_safe()
        self.main_window.show_menu()

    def show_programmer_task(self):
        task_data = get_programmer_task(self.lesson_index)
        if not task_data["solution"]:
            QMessageBox.information(self, "Informacja", "Brak dodatkowego zadania.")
            return
        dialog = ProgrammerTaskDialog(task_data["instruction"], task_data["solution"], self)
        dialog.exec()
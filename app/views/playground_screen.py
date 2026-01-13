import sys
import traceback
from io import StringIO
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QFrame, QSplitter, QSizePolicy, QFileDialog, QMessageBox)
from PySide6.QtGui import QFont, QColor, QTextCursor
from PySide6.QtCore import Qt


class PlaygroundScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Nagłówek ---
        header_layout = QHBoxLayout()
        title = QLabel("🐍 Interaktywny Plac Zabaw")
        title.setObjectName("welcomeHeader")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)

        main_layout.addLayout(header_layout)

        description = QLabel(
            "Tu możesz eksperymentować! Wpisz kod po lewej, kliknij 'Uruchom' i zobacz wynik po prawej.")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #aaa; font-size: 14px; margin-bottom: 5px;")
        description.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        main_layout.addWidget(description)

        # --- Obszar Roboczy (Splitter) ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Rozciągaj się na maxa

        # Lewy panel (Input)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 5, 0)

        code_label = QLabel("Twój Kod (Input):")
        code_label.setStyleSheet("font-weight: bold; color: #50fa7b;")
        left_layout.addWidget(code_label)

        self.code_editor = QTextEdit()
        # Ustawiamy czcionkę bezpośrednio w CSS, żeby mieć pewność, że zadziała
        self.code_editor.setPlaceholderText("print('Witaj w CodeCraft!')\n\nx = 10\ny = 20\nprint(x + y)")
        self.code_editor.setStyleSheet("""
            QTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                border: 2px solid #6272a4;
                border-radius: 5px;
                font-family: 'Consolas';
                font-size: 24px;
            }
        """)
        # Ustawiamy politykę rozmiaru na Expanding
        self.code_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.code_editor)

        # Prawy panel (Output)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 0, 0)

        output_label = QLabel("Wynik (Output):")
        output_label.setStyleSheet("font-weight: bold; color: #ff79c6;")
        right_layout.addWidget(output_label)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        # Tutaj również wymuszamy rozmiar w CSS
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e2e;
                color: #8be9fd;
                border: 2px solid #44475a;
                border-radius: 5px;
                font-family: 'Consolas';
                font-size: 24px;
            }
        """)
        self.console_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.console_output)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([500, 500])

        # ✅ KLUCZOWA ZMIANA: stretch=1 sprawi, że splitter zajmie całe dostępne miejsce w pionie
        main_layout.addWidget(splitter, 1)

        # --- Przyciski ---
        buttons_layout = QHBoxLayout()

        self.back_btn = QPushButton("🔙 Powrót do menu")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.setMinimumHeight(50)
        self.back_btn.clicked.connect(self.main_window.show_menu)

        self.clear_btn = QPushButton("🗑️ Wyczyść")
        self.clear_btn.setObjectName("secondaryButton")
        self.clear_btn.setMinimumHeight(50)
        self.clear_btn.clicked.connect(self.clear_all)

        self.save_btn = QPushButton("💾 Zapisz Plik")
        self.save_btn.setObjectName("secondaryButton")
        self.save_btn.setMinimumHeight(50)
        self.save_btn.clicked.connect(self.save_file)

        self.run_btn = QPushButton("▶ URUCHOM KOD")
        self.run_btn.setObjectName("taskButton")
        self.run_btn.setMinimumHeight(50)
        self.run_btn.clicked.connect(self.run_code)

        buttons_layout.addWidget(self.back_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.run_btn)

        main_layout.addLayout(buttons_layout)

    def run_code(self):
        code = self.code_editor.toPlainText()
        if not code.strip():
            self.console_output.setPlainText("--- Pusty kod ---")
            return

        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

        self.console_output.clear()

        try:
            # Uruchamiamy kod użytkownika w bezpiecznym środowisku (lokalnym scope)
            exec(code, {})
            result = redirected_output.getvalue()
            if not result:
                result = "[Program wykonany pomyślnie, brak outputu]"
            self.append_output(result, is_error=False)

        except Exception:
            error_msg = traceback.format_exc()
            self.append_output(error_msg, is_error=True)
        finally:
            sys.stdout = old_stdout

    def append_output(self, text, is_error=False):
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)

        format = cursor.charFormat()
        if is_error:
            format.setForeground(QColor("#ff5555"))
        else:
            format.setForeground(QColor("#8be9fd"))

            # Ważne: Musimy ustawić font ponownie dla nowego tekstu, bo formatowanie może się zresetować
        font = QFont("Consolas", 24)
        format.setFont(font)

        cursor.setCharFormat(format)
        cursor.insertText(text + "\n")
        self.console_output.setTextCursor(cursor)
        self.console_output.ensureCursorVisible()

    def clear_all(self):
        self.code_editor.clear()
        self.console_output.clear()

    def save_file(self):
        code = self.code_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "Błąd", "Nie można zapisać pustego pliku!")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz Plik Python", "", "Python Files (*.py);;All Files (*)")

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                QMessageBox.information(self, "Sukces", f"Plik zapisany pomyślnie:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać pliku:\n{str(e)}")
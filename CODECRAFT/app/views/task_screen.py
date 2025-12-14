import ast
import textwrap
import traceback
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextEdit, QHBoxLayout, QComboBox, QMessageBox, QListWidget, QDialog, QScrollArea,
                               QFrame)
from PySide6.QtCore import Qt
from app.models.task import Task
from app.widgets.reorder_list import ReorderList


class HintDialog(QDialog):
    def __init__(self, hint_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Podpowiedź")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QLabel(hint_text)
        content.setWordWrap(True)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        self.setLayout(layout)


def codes_match_ast(code1: str, code2: str) -> bool:
    try:
        if not code1 or not code2: return False
        tree1 = ast.parse(textwrap.dedent(code1.strip()))
        tree2 = ast.parse(textwrap.dedent(code2.strip()))
        return ast.dump(tree1) == ast.dump(tree2)
    except (SyntaxError, ValueError, Exception):
        return False


class TaskScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_task_index = 0
        self.filtered_tasks = []
        self.current_task = None
        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # --- GÓRNY PASEK ---
        top_layout = QHBoxLayout()
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)

        # --- ZMIANA: Duży przycisk TTS ---
        self.tts_button = QPushButton("🔊")
        self.tts_button.setFixedSize(60, 60)
        self.tts_button.setToolTip("Odsłuchaj treść zadania")
        self.tts_button.setObjectName("secondaryButton")
        self.tts_button.clicked.connect(self.read_task_content)
        # Styl dla dużej ikony
        self.tts_button.setStyleSheet("font-size: 32px; border-radius: 10px; border: 2px solid #6200ea;")

        top_layout.addWidget(self.progress_label)
        top_layout.addStretch()
        top_layout.addWidget(self.tts_button)
        self.layout.addLayout(top_layout)

        self.title_label = QLabel("🧪 Zadanie")
        self.title_label.setObjectName("welcomeHeader")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        # ... (reszta kodu bez zmian: status_label, scroll_area, itd.)
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        question_frame = QFrame()
        question_frame.setObjectName("formFrame")
        q_layout = QVBoxLayout(question_frame)
        q_layout.setSpacing(15)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setObjectName("questionLabel")
        self.question_label.setStyleSheet("font-size: 16px;")
        q_layout.addWidget(self.question_label)

        self.code_input = QTextEdit()
        self.code_input.setMinimumHeight(150)
        self.option_select = QComboBox()
        self.option_select.setMinimumHeight(40)
        self.reorder_list = ReorderList()
        self.reorder_list.setMinimumHeight(150)

        q_layout.addWidget(self.code_input)
        q_layout.addWidget(self.option_select)
        q_layout.addWidget(self.reorder_list)

        self.scroll_layout.addWidget(question_frame)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        button_layout = QHBoxLayout()
        self.check_button = QPushButton("Sprawdź")
        self.check_button.setObjectName("primaryButton")
        self.check_button.setMinimumHeight(45)
        self.check_button.setCursor(Qt.PointingHandCursor)
        self.check_button.clicked.connect(self.check_answer)
        button_layout.addWidget(self.check_button)

        self.hint_button = QPushButton("Podpowiedź")
        self.hint_button.setMinimumHeight(45)
        self.hint_button.setCursor(Qt.PointingHandCursor)
        self.hint_button.clicked.connect(self.show_hint)
        self.hint_button.setStyleSheet("background-color: #FFC107; color: #333; font-weight: bold; border-radius: 8px;")
        button_layout.addWidget(self.hint_button)
        self.layout.addLayout(button_layout)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 5px;")
        self.layout.addWidget(self.result_label)

        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Poprzednie")
        self.prev_button.setObjectName("secondaryButton")
        self.prev_button.clicked.connect(self.main_window.previous_task)

        self.next_button = QPushButton("Następne ➡️")
        self.next_button.setObjectName("secondaryButton")
        self.next_button.clicked.connect(self.main_window.next_task)

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

        self.back_button = QPushButton("📘 Powrót do lekcji")
        self.back_button.setObjectName("secondaryButton")
        self.back_button.clicked.connect(self.main_window.show_lesson)
        self.layout.addWidget(self.back_button)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_tasks()
        self.update_task()

    def read_task_content(self):
        if hasattr(self, 'current_task') and self.current_task:
            self.main_window.read_text(self.current_task.question)

    def load_tasks(self):
        lesson_index = self.main_window.lesson_index
        all_tasks = Task.load_all()
        self.filtered_tasks = [t for t in all_tasks if t.lesson_index == lesson_index]
        if not self.filtered_tasks:
            self.filtered_tasks = [Task(lesson_index, "Debug", "ok", "code_input")]

    def update_task(self):
        if not self.filtered_tasks: return
        if hasattr(self.main_window, 'tts'): self.main_window.tts.stop()

        self.result_label.clear()
        self.result_label.setStyleSheet("")
        self.status_label.clear()
        self.status_label.setStyleSheet("")
        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()
        self.code_input.setReadOnly(False)
        self.option_select.setEnabled(True)
        self.reorder_list.setDragDropMode(QListWidget.InternalMove)

        self.current_task = self.filtered_tasks[self.main_window.current_task_index]
        task_id = self.current_task.get_id()
        progress = self.main_window.user_progress

        self.question_label.setText(self.current_task.question)
        self.title_label.setText(f"🧪 Zadanie {self.main_window.current_task_index + 1}/{len(self.filtered_tasks)}")
        lesson_key = str(self.current_task.lesson_index)
        completed = progress.module_scores.get(lesson_key, 0)
        total = len(self.filtered_tasks)
        self.progress_label.setText(f"Postęp: {completed}/{total} zadań ukończonych")
        if task_id in progress.completed_tasks:
            self._mark_task_completed()
            if task_id in progress.task_solutions:
                self._load_saved_answer(self.current_task, progress.task_solutions[task_id]["answer"])
        self._setup_answer_widget()

    def show_hint(self):
        if not self.current_task: return
        hint_text = "Brak podpowiedzi"
        if self.current_task.type == "code_input": hint_text = f"Rozwiązanie:\n{self.current_task.solution}"
        dialog = HintDialog(hint_text, self)
        dialog.exec()

    def _prepare_hint(self):
        if not self.current_task: return "Brak dostępnych podpowiedzi"
        if self.current_task.type == "multiple_choice":
            for opt in self.current_task.options:
                if opt.startswith(self.current_task.solution): return f"Poprawna odpowiedź: {opt}"
            return "Brak podpowiedzi"
        elif self.current_task.type in ("code_input", "code_output"):
            return f"Rozwiązanie:\n{self.current_task.solution}"
        elif self.current_task.type == "reorder":
            lines = self.current_task.solution.split('\n')
            return "Poprawna kolejność:\n" + "\n".join(f"{i + 1}. {line}" for i, line in enumerate(lines))
        return "Brak dostępnej podpowiedzi"

    def _setup_answer_widget(self):
        self.code_input.hide();
        self.option_select.hide();
        self.reorder_list.hide()
        if self.current_task.type in ("code_input", "code_output"):
            self.code_input.show()
            self.code_input.setPlaceholderText(
                "Wpisz wynik..." if self.current_task.type == "code_output" else "Twój kod...")
        elif self.current_task.type == "multiple_choice":
            self.option_select.show();
            self.option_select.clear()
            for option in self.current_task.options: self.option_select.addItem(option)
        elif self.current_task.type == "reorder":
            self.reorder_list.show();
            self.reorder_list.clear()
            for block in self.current_task.options: self.reorder_list.addItem(block)

    def _mark_task_completed(self):
        self.status_label.setText("✓ Zadanie ukończone")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 14px;")

    def _load_saved_answer(self, task, answer):
        try:
            if task.type in ("code_input", "code_output"):
                self.code_input.setPlainText(answer)
                self.code_input.setReadOnly(True)
            elif task.type == "multiple_choice":
                index = self.option_select.findText(answer, Qt.MatchContains)
                if index >= 0: self.option_select.setCurrentIndex(index)
                self.option_select.setEnabled(False)
            elif task.type == "reorder":
                self.reorder_list.load_from_code(answer)
                self.reorder_list.setDragDropMode(QListWidget.NoDragDrop)
        except Exception as e:
            print(f"Błąd ładowania odpowiedzi: {e}")

    def check_answer(self):
        print("DEBUG: Rozpoczęcie sprawdzania odpowiedzi...")
        if not self.current_task:
            print("DEBUG: Brak bieżącego zadania!")
            return

        try:
            task_id = self.current_task.get_id()
            progress = self.main_window.user_progress

            if task_id in progress.completed_tasks:
                QMessageBox.information(self, "Info", "To zadanie zostało już poprawnie rozwiązane!")
                return

            user_answer = self._get_user_answer()
            print(f"DEBUG: Odpowiedź użytkownika: '{user_answer}'")

            is_correct = self._validate_answer(user_answer)
            print(f"DEBUG: Wynik walidacji: {is_correct}")

            if is_correct:
                progress.complete_task(task_id, self.current_task.lesson_index)
                progress.save_task_answer(task_id, user_answer)

                if hasattr(self.main_window.user_progress, 'check_achievements'):
                    new_achievements = self.main_window.user_progress.check_achievements()
                    if new_achievements:
                        self.main_window.show_achievement_notification(new_achievements)

                self._mark_task_completed()

            self._update_ui_feedback(is_correct)

        except Exception as e:
            error_msg = f"Wystąpił błąd podczas sprawdzania:\n{str(e)}\n{traceback.format_exc()}"
            print(f"CRITICAL ERROR: {error_msg}")
            QMessageBox.critical(self, "Błąd Krytyczny", error_msg)

    def save_task(self):
        if not self.current_task: return
        task_id = self.current_task.get_id()
        user_answer = self._get_user_answer()
        self.main_window.user_progress.save_task_answer(task_id, user_answer)

    def _get_user_answer(self):
        if self.current_task.type == "code_input":
            return self.code_input.toPlainText()
        elif self.current_task.type == "code_output":
            return self.code_input.toPlainText().strip()
        elif self.current_task.type == "multiple_choice":
            return self.option_select.currentText().strip()
        elif self.current_task.type == "reorder":
            return self.reorder_list.get_code_string().strip()
        return ""

    def _validate_answer(self, user_answer):
        if self.current_task.type == "code_input":
            return codes_match_ast(user_answer, self.current_task.solution)
        elif self.current_task.type == "code_output":
            return user_answer == self.current_task.solution.strip()
        elif self.current_task.type == "multiple_choice":
            return user_answer.startswith(self.current_task.solution)
        elif self.current_task.type == "reorder":
            user_lines = [line.strip() for line in user_answer.splitlines() if line.strip()]
            correct_lines = [line.strip() for line in self.current_task.solution.strip().splitlines() if line.strip()]
            return user_lines == correct_lines
        return False

    def _update_ui_feedback(self, is_correct):
        if is_correct:
            self.result_label.setText("✓ Poprawna odpowiedź!")
            self.result_label.setStyleSheet("color: #4CAF50; font-weight: bold")
            lesson_key = str(self.current_task.lesson_index)
            completed = self.main_window.user_progress.module_scores.get(lesson_key, 0)
            total = len(self.filtered_tasks)
            self.progress_label.setText(f"Postęp: {completed}/{total} zadań ukończonych")
        else:
            self.result_label.setText("✗ Spróbuj jeszcze raz")
            self.result_label.setStyleSheet("color: #F44336; font-weight: bold")
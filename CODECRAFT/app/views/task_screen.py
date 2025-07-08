import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextEdit, QHBoxLayout, QComboBox, QMessageBox, QListWidget)
from PySide6.QtCore import Qt
from app.models.task import Task
from app.widgets.reorder_list import ReorderList
import ast
import textwrap


def codes_match_ast(code1: str, code2: str) -> bool:
    try:
        tree1 = ast.parse(textwrap.dedent(code1.strip()))
        tree2 = ast.parse(textwrap.dedent(code2.strip()))
        return ast.dump(tree1) == ast.dump(tree2)
    except SyntaxError:
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
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Progress label
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress_label)

        # Title label
        self.title_label = QLabel("🧪 Zadanie")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # Question label
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        # Answer widgets
        self.code_input = QTextEdit()
        self.option_select = QComboBox()
        self.reorder_list = ReorderList()

        self.layout.addWidget(self.code_input)
        self.layout.addWidget(self.option_select)
        self.layout.addWidget(self.reorder_list)

        # Check button
        self.check_button = QPushButton("Sprawdź")
        self.check_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_button)

        # Result label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        # Navigation
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Poprzednie")
        self.prev_button.clicked.connect(self.main_window.previous_task)
        self.next_button = QPushButton("Następne ➡️")
        self.next_button.clicked.connect(self.main_window.next_task)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

        # Back button
        self.back_button = QPushButton("📘 Powrót do lekcji")
        self.back_button.clicked.connect(self.main_window.show_lesson)
        self.layout.addWidget(self.back_button)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_tasks()
        self.update_task()

    def load_tasks(self):
        """Load tasks for current lesson"""
        print("\n=== DEBUG: Ładowanie zadań ===")
        lesson_index = self.main_window.lesson_index
        print(f"Aktualna lekcja: {lesson_index}")

        all_tasks = Task.load_all()
        print(f"Łączna liczba zadań: {len(all_tasks)}")

        self.filtered_tasks = [t for t in all_tasks if t.lesson_index == lesson_index]
        print(f"Znaleziono zadań dla lekcji {lesson_index}: {len(self.filtered_tasks)}")

        if not self.filtered_tasks:
            print("UWAGA: Brak zadań dla tej lekcji!")
            self.filtered_tasks = [
                Task(lesson_index, "Debug: Wpisz 'print(5)'", "print(5)", "code_input")
            ]

        for i, task in enumerate(self.filtered_tasks[:3]):
            print(f"Zadanie {i + 1}: {task.question[:50]}...")

    def update_task(self):
        """Update UI for current task"""
        if not self.filtered_tasks:
            print("Brak zadań do wyświetlenia!")
            return

        # Reset UI elements
        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()
        self.code_input.setReadOnly(False)
        self.option_select.setEnabled(True)
        self.reorder_list.setDragDropMode(QListWidget.InternalMove)

        # Get current task
        self.current_task = self.filtered_tasks[self.main_window.current_task_index]
        task_id = self.current_task.get_id()
        progress = self.main_window.user_progress

        # Update task info
        self.question_label.setText(self.current_task.question)
        self.title_label.setText(f"🧪 Zadanie {self.main_window.current_task_index + 1}/{len(self.filtered_tasks)}")

        # Update progress
        lesson_key = str(self.current_task.lesson_index)
        completed = progress.module_scores.get(lesson_key, 0)
        total = len(self.filtered_tasks)
        self.progress_label.setText(f"Postęp: {completed}/{total} zadań ukończonych")

        # Check if task is completed
        if task_id in progress.completed_tasks:
            self._mark_task_completed()
            if task_id in progress.task_solutions:
                self._load_saved_answer(self.current_task, progress.task_solutions[task_id]["answer"])

        # Setup answer widget based on task type
        self._setup_answer_widget()

    def _setup_answer_widget(self):
        """Configure appropriate answer widget based on task type"""
        self.code_input.hide()
        self.option_select.hide()
        self.reorder_list.hide()

        if self.current_task.type in ("code_input", "code_output"):
            self.code_input.show()
            if self.current_task.type == "code_output":
                self.code_input.setPlaceholderText("Wpisz oczekiwany wynik...")
        elif self.current_task.type == "multiple_choice":
            self.option_select.show()
            for option in self.current_task.options:
                self.option_select.addItem(option)
        elif self.current_task.type == "reorder":
            self.reorder_list.show()
            for block in self.current_task.options:
                self.reorder_list.addItem(block)

    def _mark_task_completed(self):
        """Mark task as completed in UI"""
        self.status_label.setText("✓ Zadanie ukończone")
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold")

    def _load_saved_answer(self, task, answer):
        """Load saved answer into appropriate widget"""
        if task.type in ("code_input", "code_output"):
            self.code_input.setPlainText(answer)
            self.code_input.setReadOnly(True)
        elif task.type == "multiple_choice":
            index = self.option_select.findText(answer, Qt.MatchContains)
            if index >= 0:
                self.option_select.setCurrentIndex(index)
            self.option_select.setEnabled(False)
        elif task.type == "reorder":
            self.reorder_list.load_from_code(answer)
            self.reorder_list.setDragDropMode(QListWidget.NoDragDrop)

    def check_answer(self):
        """Check user's answer and update progress"""
        if not self.current_task:
            return

        task_id = self.current_task.get_id()
        progress = self.main_window.user_progress

        # Check if task already completed
        if task_id in progress.completed_tasks:
            QMessageBox.information(self, "Info", "To zadanie zostało już rozwiązane!")
            return

        # Get user answer
        user_answer = self._get_user_answer()
        is_correct = self._validate_answer(user_answer)

        # Update progress if correct
        if is_correct:
            progress.complete_task(task_id, self.current_task.lesson_index)
            progress.save_task_answer(task_id, user_answer)
            self._mark_task_completed()

        # Update UI feedback
        self._update_ui_feedback(is_correct)

    def _get_user_answer(self):
        """Get answer from appropriate widget"""
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
        """Validate user's answer"""
        if self.current_task.type == "code_input":
            return codes_match_ast(user_answer, self.current_task.solution)
        elif self.current_task.type == "code_output":
            return user_answer == self.current_task.solution.strip()
        elif self.current_task.type == "multiple_choice":
            return user_answer.startswith(self.current_task.solution)
        elif self.current_task.type == "reorder":
            user_lines = [line.strip() for line in user_answer.splitlines()]
            correct_lines = [line.strip() for line in self.current_task.solution.strip().splitlines()]
            return user_lines == correct_lines
        return False

    def _update_ui_feedback(self, is_correct):
        """Update UI based on answer correctness"""
        if is_correct:
            self.result_label.setText("✓ Poprawna odpowiedź!")
            self.result_label.setStyleSheet("color: #4CAF50; font-weight: bold")

            # Update progress counter
            lesson_key = str(self.current_task.lesson_index)
            completed = self.main_window.user_progress.module_scores.get(lesson_key, 0)
            total = len(self.filtered_tasks)
            self.progress_label.setText(f"Postęp: {completed}/{total} zadań ukończonych")
        else:
            self.result_label.setText("✗ Spróbuj jeszcze raz")
            self.result_label.setStyleSheet("color: #F44336; font-weight: bold")
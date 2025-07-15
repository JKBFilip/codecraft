from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextEdit, QComboBox, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QElapsedTimer
from app.models.task import Task
import random
import ast
import textwrap
from app.widgets.reorder_list import ReorderList
from app.assets.test_summary_styles import generate_summary_html


def codes_match_ast(code1: str, code2: str) -> bool:
    try:
        tree1 = ast.parse(textwrap.dedent(code1.strip()))
        tree2 = ast.parse(textwrap.dedent(code2.strip()))
        return ast.dump(tree1) == ast.dump(tree2)
    except SyntaxError:
        return False


class FinalTestScreen(QWidget):
    def __init__(self, main_window, lesson_index):
        super().__init__()
        self.main_window = main_window
        self.lesson_index = lesson_index
        self.tasks = [t for t in Task.load_all() if t.lesson_index == lesson_index]
        self.test_tasks = random.sample(self.tasks, 10) if len(self.tasks) >= 10 else self.tasks.copy()
        self.current_index = 0
        self.correct_answers = 0
        self.remaining_time = 300
        self.user_answers = []

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_timer)
        self.elapsed_timer = QElapsedTimer()

        self.init_ui()
        self.load_task()
        self.start_test()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.timer_label = QLabel("Czas: 05:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.timer_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        scroll.setWidget(self.content_widget)
        self.layout.addWidget(scroll)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 20px;")
        self.content_layout.addWidget(self.question_label)

        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Wpisz tutaj swój kod...")
        self.content_layout.addWidget(self.code_input)

        self.option_select = QComboBox()
        self.content_layout.addWidget(self.option_select)

        self.reorder_list = ReorderList()
        self.content_layout.addWidget(self.reorder_list)

        self.check_button = QPushButton("Zatwierdź odpowiedź")
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.check_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_button)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.hide()
        self.layout.addWidget(self.summary_text)

        self.final_result_label = QLabel()
        self.final_result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            text-align: center;
        """)
        self.final_result_label.hide()
        self.layout.addWidget(self.final_result_label)

        self.back_button = QPushButton("🔙 Powrót do menu")
        self.back_button.setStyleSheet("padding: 10px;")
        self.back_button.clicked.connect(self.main_window.show_menu)
        self.back_button.hide()
        self.layout.addWidget(self.back_button)

    def start_test(self):
        self.elapsed_timer.start()
        self.countdown_timer.start(1000)
        self.remaining_time = 300

    def update_timer(self):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Czas: {minutes:02d}:{seconds:02d}")

        if self.remaining_time <= 0:
            self.countdown_timer.stop()
            self.end_test(timeout=True)

    def load_task(self):
        if self.current_index >= len(self.test_tasks):
            self.end_test()
            return

        task = self.test_tasks[self.current_index]
        self.current_task = task

        self.code_input.hide()
        self.option_select.hide()
        self.reorder_list.hide()

        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()

        self.question_label.setText(f"Pytanie {self.current_index + 1}/{len(self.test_tasks)}:\n\n{task.question}")

        if task.type in ("code_input", "code_output"):
            self.code_input.show()
            if task.type == "code_output":
                self.code_input.setPlaceholderText("Wpisz oczekiwany wynik...")
        elif task.type == "multiple_choice":
            self.option_select.show()
            for opt in task.options:
                self.option_select.addItem(opt)
        elif task.type == "reorder":
            self.reorder_list.show()
            for block in task.options:
                self.reorder_list.addItem(block)

    def check_answer(self):
        if not hasattr(self, 'current_task'):
            return

        task = self.current_task
        user_answer = ""
        correct_answer = task.solution
        is_correct = False

        if task.type == "code_input":
            user_answer = self.code_input.toPlainText()
            is_correct = codes_match_ast(user_answer, correct_answer)
        elif task.type == "code_output":
            user_answer = self.code_input.toPlainText().strip()
            is_correct = (user_answer == correct_answer.strip())
        elif task.type == "multiple_choice":
            user_answer = self.option_select.currentText().strip()
            is_correct = user_answer.startswith(correct_answer)
        elif task.type == "reorder":
            user_answer = self.reorder_list.get_code_string().strip()
            correct_lines = [line.strip() for line in correct_answer.strip().splitlines()]
            user_lines = [line.strip() for line in user_answer.splitlines()]
            is_correct = user_lines == correct_lines

        self.user_answers.append({
            "question": task.question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "type": task.type
        })

        if is_correct:
            self.correct_answers += 1

        self.current_index += 1
        self.load_task()

    def end_test(self, timeout=False):
        self.countdown_timer.stop()
        elapsed_time = float(self.elapsed_timer.elapsed()) / 1000
        total_questions = len(self.test_tasks)
        score_percentage = (self.correct_answers / total_questions) * 100
        perfect_score = (self.correct_answers == total_questions)
        self.main_window.user_progress.test_completion_time = elapsed_time

        test_result = {
            "module": self.lesson_index,
            "score": float(score_percentage),
            "perfect": bool(perfect_score),
            "time": float(elapsed_time),
            "date": datetime.now().isoformat()
        }

        self.main_window.user_progress.add_test_result(
            module_index=self.lesson_index,
            score=(self.correct_answers / len(self.test_tasks)) * 100,
            perfect_score=(self.correct_answers == len(self.test_tasks)),
            time_taken=elapsed_time
        )
        self.main_window.user_progress.save_progress()

        self.layout.itemAt(1).widget().hide()
        self.timer_label.hide()
        self.check_button.hide()

        self.summary_text.setHtml(generate_summary_html(self.user_answers, self.correct_answers))
        self.summary_text.show()

        if timeout:
            result_msg = "Czas minął! Test niezaliczony."
            self.final_result_label.setStyleSheet("color: #D32F2F;")
        elif self.correct_answers >= 8:
            result_msg = "Test zdany! Moduł zaliczony."
            if perfect_score:
                result_msg += " Perfekcyjny wynik 100%!"
                self.final_result_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            else:
                self.final_result_label.setStyleSheet("color: #2E7D32;")

            try:
                task_id = f"final_test_{self.lesson_index}"
                self.main_window.user_progress.complete_task(task_id, self.lesson_index)
            except Exception as e:
                print(f"Błąd zapisu: {e}")
        else:
            result_msg = f"Test niezaliczony. Wynik: {self.correct_answers}/{total_questions}"
            self.final_result_label.setStyleSheet("color: #D32F2F;")

        self.final_result_label.setText(result_msg)
        self.final_result_label.show()
        self.back_button.show()

        if hasattr(self.main_window, 'check_achievements'):
            self.main_window.check_achievements()

        new_achievements = self.main_window.user_progress.check_achievements()
        if new_achievements:
            self.main_window.show_achievement_notification(new_achievements)

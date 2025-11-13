import random
import ast
import textwrap
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QElapsedTimer
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QTextEdit, QComboBox, QMessageBox, QStackedWidget, QFrame)

from app.models.task import Task
from app.widgets.reorder_list import ReorderList
from app.assets.test_summary_styles import generate_summary_html

def codes_match_ast(code1: str, code2: str) -> bool:
    try:
        tree1 = ast.parse(textwrap.dedent(code1.strip()))
        tree2 = ast.parse(textwrap.dedent(code2.strip()))
        return ast.dump(tree1) == ast.dump(tree2)
    except SyntaxError:
        return False
    except Exception:
        return False

class FinalTestScreen(QWidget):
    def __init__(self, main_window, lesson_index):
        super().__init__()
        self.main_window = main_window
        self.lesson_index = lesson_index

        self.test_tasks, self.user_answers = [], []
        self.current_index, self.correct_answers, self.remaining_time = 0, 0, 300
        self.countdown_timer, self.elapsed_timer = QTimer(self), QElapsedTimer()

        self._prepare_test_tasks()

        self.stack = QStackedWidget(self)
        self.test_page = self._create_test_page()
        self.summary_page = self._create_summary_page()
        self.stack.addWidget(self.test_page)
        self.stack.addWidget(self.summary_page)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)

        self.start_test()

    def _prepare_test_tasks(self):
        try:
            all_module_tasks = [t for t in Task.load_all() if t.lesson_index == self.lesson_index]
            if len(all_module_tasks) >= 10:
                self.test_tasks = random.sample(all_module_tasks, 10)
            else:
                self.test_tasks = all_module_tasks
                print(f"Warning: Module {self.lesson_index} has only {len(all_module_tasks)} tasks. Using all for the test.")
            if not self.test_tasks:
                 QMessageBox.warning(self, "Błąd", f"Nie znaleziono zadań dla modułu {self.lesson_index}!")
        except Exception as e:
            QMessageBox.critical(self, "Błąd ładowania zadań", f"Nie udało się wczytać zadań testowych: {e}")
            self.test_tasks = []

    def _create_test_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        self.timer_label = QLabel("Czas: 05:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffca8a; padding: 5px; background-color: #2a2a40; border-radius: 5px;")
        top_bar_layout.addWidget(self.timer_label)
        layout.addLayout(top_bar_layout)

        question_frame = QFrame()
        question_frame.setObjectName("formFrame")
        q_layout = QVBoxLayout(question_frame)
        q_layout.setSpacing(10)

        self.question_label = QLabel("Pytanie...")
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 18px; color: #f8f8f2; margin-bottom: 10px;")
        q_layout.addWidget(self.question_label)

        self.answer_stack = QStackedWidget()
        self.code_input = QTextEdit()
        self.option_select = QComboBox()
        self.reorder_list = ReorderList()
        self.answer_stack.addWidget(self.code_input)
        self.answer_stack.addWidget(self.option_select)
        self.answer_stack.addWidget(self.reorder_list)
        q_layout.addWidget(self.answer_stack)

        layout.addWidget(question_frame)

        self.submit_button = QPushButton("Zatwierdź odpowiedź")
        self.submit_button.setObjectName("primaryButton")
        self.submit_button.setMinimumHeight(45)
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)
        return page

    def _create_summary_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        self.summary_title = QLabel("Podsumowanie Testu")
        self.summary_title.setObjectName("welcomeHeader")
        self.summary_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_title)

        self.final_result_label = QLabel("Wynik...")
        self.final_result_label.setAlignment(Qt.AlignCenter)
        self.final_result_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(self.final_result_label)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setObjectName("summaryText")
        layout.addWidget(self.summary_text)

        back_button = QPushButton("🔙 Powrót do menu")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.main_window.show_menu)
        layout.addWidget(back_button)
        return page

    def start_test(self):
        if not self.test_tasks:
            self.main_window.show_menu()
            return
        self.remaining_time = 300
        self.elapsed_timer.start()
        self.countdown_timer.timeout.connect(self.update_timer)
        self.countdown_timer.start(1000)
        self.load_task()
        self.stack.setCurrentWidget(self.test_page)

    def update_timer(self):
        self.remaining_time -= 1
        minutes, seconds = self.remaining_time // 60, self.remaining_time % 60
        self.timer_label.setText(f"Czas: {minutes:02d}:{seconds:02d}")
        if self.remaining_time <= 60:
            self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f44336; padding: 5px; background-color: #2a2a40; border-radius: 5px;")
        if self.remaining_time <= 0:
            self.end_test(timeout=True)

    def load_task(self):
        if self.current_index >= len(self.test_tasks):
            self.end_test()
            return

        task = self.test_tasks[self.current_index]
        self.current_task = task
        self.question_label.setText(f"Pytanie {self.current_index + 1}/{len(self.test_tasks)}:\n\n{task.question}")
        task_type = task.type

        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()

        if task_type in ("code_input", "code_output"):
            self.code_input.setPlaceholderText("Wpisz odpowiedź...")
            self.answer_stack.setCurrentWidget(self.code_input)
        elif task_type == "multiple_choice":
            options_copy = task.options[:]
            random.shuffle(options_copy)
            self.option_select.addItems(options_copy)
            self.answer_stack.setCurrentWidget(self.option_select)
        elif task_type == "reorder":
            options_copy = task.options[:]
            random.shuffle(options_copy)
            self.reorder_list.addItems(options_copy)
            self.answer_stack.setCurrentWidget(self.reorder_list)

    def check_answer(self):
        if not hasattr(self, 'current_task'): return

        task = self.current_task
        user_answer, correct_answer, is_correct = "", task.solution, False

        try:
            if task.type == "code_input":
                user_answer = self.code_input.toPlainText()
                is_correct = codes_match_ast(user_answer, correct_answer)
            elif task.type == "code_output":
                user_answer = self.code_input.toPlainText().strip()
                is_correct = (user_answer == correct_answer.strip())
            elif task.type == "multiple_choice":
                user_answer = self.option_select.currentText().strip()
                is_correct = user_answer.startswith(correct_answer.strip())
            elif task.type == "reorder":
                user_answer = self.reorder_list.get_code_string()
                user_lines = [line.strip() for line in user_answer.strip().splitlines()]
                correct_lines = [line.strip() for line in correct_answer.strip().splitlines()]
                is_correct = user_lines == correct_lines

        except Exception as e:
            print(f"ERROR checking answer for task type {task.type}: {e}")
            is_correct = False

        self.user_answers.append({"question": task.question, "user_answer": user_answer, "correct_answer": correct_answer, "is_correct": is_correct, "type": task.type})

        if is_correct: self.correct_answers += 1

        self.current_index += 1
        self.load_task()

    def end_test(self, timeout=False):
        self.countdown_timer.stop()
        elapsed_time = float(self.elapsed_timer.elapsed()) / 1000.0
        total_questions = len(self.test_tasks)
        score_percentage = (self.correct_answers / total_questions) * 100 if total_questions > 0 else 0
        perfect_score = (self.correct_answers == total_questions) and total_questions > 0
        passed = self.correct_answers >= 8 and not timeout

        self.main_window.user_progress.add_test_result(
            module_index=self.lesson_index,
            score=score_percentage,
            perfect_score=perfect_score,
            time_taken=elapsed_time
        )

        self.summary_text.setHtml(generate_summary_html(self.user_answers, self.correct_answers, required_to_pass=8))

        if timeout:
            result_msg = "Czas minął! Test niezaliczony."
            self.final_result_label.setStyleSheet("color: #ff5555; font-size: 18px; font-weight: bold;")
        elif passed:
            result_msg = f"Test zdany! Wynik: {self.correct_answers}/{total_questions} ({score_percentage:.1f}%)"
            if perfect_score: result_msg += " Perfekcyjnie!"
            self.final_result_label.setStyleSheet("color: #50fa7b; font-size: 18px; font-weight: bold;")

            try:
                task_id = f"final_test_{self.lesson_index}"
                self.main_window.user_progress.complete_task(task_id, self.lesson_index)
            except Exception as e:
                print(f"Error marking test as completed: {e}")
        else:
            result_msg = f"Test niezaliczony. Wynik: {self.correct_answers}/{total_questions} ({score_percentage:.1f}%)"
            self.final_result_label.setStyleSheet("color: #ff5555; font-size: 18px; font-weight: bold;")

        self.final_result_label.setText(result_msg)

        self.stack.setCurrentWidget(self.summary_page)

        self.main_window.user_progress.check_achievements()
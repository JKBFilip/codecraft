from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout, QComboBox
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
        self.tasks = Task.load_all()
        self.filtered_tasks = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("🧪 Zadanie")
        self.layout.addWidget(self.title_label)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        # Dynamiczne widżety:
        self.code_input = QTextEdit()
        self.option_select = QComboBox()
        self.reorder_list = ReorderList()

        self.layout.addWidget(self.code_input)
        self.layout.addWidget(self.option_select)
        self.layout.addWidget(self.reorder_list)

        self.check_button = QPushButton("Sprawdź")
        self.check_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_button)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Poprzednie")
        self.prev_button.clicked.connect(self.main_window.previous_task)
        self.next_button = QPushButton("Następne ➡️")
        self.next_button.clicked.connect(self.main_window.next_task)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

        self.back_button = QPushButton("📘 Powrót do lekcji")
        self.back_button.clicked.connect(self.main_window.show_lesson)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def showEvent(self, event):
        super().showEvent(event)
        lesson_index = self.main_window.lesson_index
        self.filtered_tasks = [t for t in self.tasks if t.lesson_index == lesson_index]
        if self.main_window.current_task_index >= len(self.filtered_tasks):
            self.main_window.current_task_index = 0
        self.update_task()

    def update_task(self):
        if not self.filtered_tasks:
            self.question_label.setText("Brak zadań dla tego modułu.")
            self.code_input.hide()
            self.option_select.hide()
            self.reorder_list.hide()
            self.result_label.setText("")
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        index = self.main_window.current_task_index
        index = max(0, min(index, len(self.filtered_tasks) - 1))
        self.main_window.current_task_index = index

        task = self.filtered_tasks[index]
        self.current_task = task  # zapisz aktualne zadanie

        self.question_label.setText(task.question)
        self.title_label.setText(f"🧠 Zadanie {index + 1} z {len(self.filtered_tasks)}")
        self.result_label.setText("")

        # Ukryj wszystkie widżety na start
        self.code_input.hide()
        self.option_select.hide()
        self.reorder_list.hide()

        # Wyczyść dane wejściowe
        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()

        # Wybierz widżet zależnie od typu zadania
        if task.type == "code_input":
            self.code_input.show()

        elif task.type == "multiple_choice":
            self.option_select.show()
            for option in task.options:
                self.option_select.addItem(option)

        elif task.type == "reorder":
            self.reorder_list.show()
            for block in task.options:
                self.reorder_list.addItem(block)

        elif task.type == "code_output":
            self.code_input.show()

        # Blokowanie przycisków
        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.filtered_tasks) - 1)

    def check_answer(self):
        task = self.filtered_tasks[self.main_window.current_task_index]

        if task.type == "code_input":
            user_code = self.code_input.toPlainText()
            if codes_match_ast(user_code, task.solution):
                self.result_label.setText("✅ Poprawna odpowiedź!")
            else:
                print("USER:")
                print(user_code)
                print("EXPECTED:")
                print(task.solution)
                self.result_label.setText("❌ Spróbuj jeszcze raz.")

        elif task.type == "code_output":
            user_answer = self.code_input.toPlainText().strip()
            if user_answer == task.solution.strip():
                self.result_label.setText("✅ Poprawna odpowiedź!")
            else:
                self.result_label.setText("❌ Niepoprawny wynik.")

        elif task.type == "multiple_choice":
            selected_text = self.option_select.currentText().strip()
            if selected_text.startswith(task.solution):
                self.result_label.setText("✅ Poprawna odpowiedź!")
            else:
                self.result_label.setText("❌ To nie ta odpowiedź.")
        elif task.type == "reorder":
            user_code_lines = self.reorder_list.get_code_string().strip().splitlines()
            correct_code_lines = task.solution.strip().splitlines()

            # Usuń nadmiarowe spacje z początku i końca
            user_code_clean = [line.strip() for line in user_code_lines]
            correct_code_clean = [line.strip() for line in correct_code_lines]

            if user_code_clean == correct_code_clean:
                self.result_label.setText("✅ Dobrze!")
            else:
                self.result_label.setText("❌ Kolejność się nie zgadza.")
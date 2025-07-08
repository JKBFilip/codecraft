from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextEdit, QHBoxLayout, QComboBox)
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
        self.tasks = Task.load_all()  # Ładujemy wszystkie zadania raz
        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Nagłówek z postępem
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress_label)

        self.title_label = QLabel("🧪 Zadanie")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Status zadania
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.layout.addWidget(self.question_label)

        # Dynamiczne widżety odpowiedzi
        self.code_input = QTextEdit()
        self.option_select = QComboBox()
        self.reorder_list = ReorderList()

        self.layout.addWidget(self.code_input)
        self.layout.addWidget(self.option_select)
        self.layout.addWidget(self.reorder_list)

        # Przycisk sprawdzania
        self.check_button = QPushButton("Sprawdź")
        self.check_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.check_button)

        # Wynik
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)

        # Nawigacja
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("⬅️ Poprzednie")
        self.prev_button.clicked.connect(self.main_window.previous_task)
        self.next_button = QPushButton("Następne ➡️")
        self.next_button.clicked.connect(self.main_window.next_task)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        self.layout.addLayout(nav_layout)

        # Przycisk powrotu
        self.back_button = QPushButton("📘 Powrót do lekcji")
        self.back_button.clicked.connect(self.main_window.show_lesson)
        self.layout.addWidget(self.back_button)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_tasks()
        self.update_task()

    def load_tasks(self):
        lesson_index = self.main_window.lesson_index
        self.filtered_tasks = [t for t in self.tasks if t.lesson_index == lesson_index]

        # Reset indeksu jeśli wykracza poza zakres
        if self.main_window.current_task_index >= len(self.filtered_tasks):
            self.main_window.current_task_index = 0

    def update_task(self):
        # Aktualizacja paska postępu
        lesson_index = self.main_window.lesson_index
        done = self.main_window.user_progress.module_scores.get(str(lesson_index), 0)
        total = len(self.filtered_tasks)
        self.progress_label.setText(f"Postęp: {done}/{total} zadań ukończonych")

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
        task = self.filtered_tasks[index]
        self.current_task = task

        # Aktualizacja UI
        self.question_label.setText(task.question)
        task_id = task.get_id()
        completed = "✔️" if task_id in self.main_window.user_progress.completed_tasks else ""
        self.title_label.setText(f"🧠 Zadanie {index + 1} z {len(self.filtered_tasks)} {completed}")

        # Reset widżetów
        self.result_label.setText("")
        self.code_input.hide()
        self.option_select.hide()
        self.reorder_list.hide()
        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()

        # Konfiguracja widżetu odpowiedniego dla typu zadania
        if task.type in ("code_input", "code_output"):
            self.code_input.show()
            if task.type == "code_output":
                self.code_input.setPlaceholderText("Wpisz oczekiwany wynik...")

        elif task.type == "multiple_choice":
            self.option_select.show()
            for option in task.options:
                self.option_select.addItem(option)

        elif task.type == "reorder":
            self.reorder_list.show()
            for block in task.options:
                self.reorder_list.addItem(block)

        # Status zadania
        if task_id in self.main_window.user_progress.completed_tasks:
            self.status_label.setText("✔️ Zadanie ukończone")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold")
        else:
            self.status_label.setText("")
            self.status_label.setStyleSheet("")

        # Przyciski nawigacji
        self.prev_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < len(self.filtered_tasks) - 1)

        # Sprawdź czy cały moduł ukończony
        if self.main_window.user_progress.is_module_complete(lesson_index, len(self.filtered_tasks)):
            self.result_label.setText("🎉 Moduł ukończony!")
            self.result_label.setStyleSheet("color: #4CAF50; font-weight: bold")

    def check_answer(self):
        task = self.filtered_tasks[self.main_window.current_task_index]
        task_id = task.get_id()
        correct = False

        # Sprawdzenie odpowiedzi w zależności od typu zadania
        if task.type == "code_input":
            user_code = self.code_input.toPlainText()
            correct = codes_match_ast(user_code, task.solution)

        elif task.type == "code_output":
            user_answer = self.code_input.toPlainText().strip()
            correct = (user_answer == task.solution.strip())

        elif task.type == "multiple_choice":
            selected_text = self.option_select.currentText().strip()
            correct = selected_text.startswith(task.solution)

        elif task.type == "reorder":
            user_code_lines = self.reorder_list.get_code_string().strip().splitlines()
            correct_code_lines = task.solution.strip().splitlines()
            user_clean = [line.strip() for line in user_code_lines]
            correct_clean = [line.strip() for line in correct_code_lines]
            correct = (user_clean == correct_clean)

        # Obsługa wyniku
        if correct:
            # Sprawdź czy zadanie nie było już wcześniej ukończone
            if task_id not in self.main_window.user_progress.completed_tasks:
                try:
                    # Zapis do systemu progresu
                    self.main_window.user_progress.complete_task(task_id, task.lesson_index)

                    # Natychmiastowy zapis do pliku
                    self.main_window.user_progress.save_progress()
                    print(f"Zapisano ukończenie zadania: {task_id}")  # Log diagnostyczny

                except Exception as e:
                    print(f"Błąd podczas zapisywania postępu: {e}")
                    self.result_label.setText("✅ Poprawnie, ale błąd zapisu postępu!")
                    self.result_label.setStyleSheet("color: #FFC107; font-weight: bold")
                    return

            self.result_label.setText("✅ Poprawna odpowiedź!")
            self.result_label.setStyleSheet("color: #4CAF50; font-weight: bold")

            # Odśwież widok zadania
            self.update_task()

            # Aktualizacja menu (jeśli to ostatnie zadanie w module)
            if self.main_window.user_progress.is_module_complete(task.lesson_index, len(self.filtered_tasks)):
                self.main_window.menu_screen.update_module_widgets()

        else:
            self.result_label.setText("❌ Spróbuj jeszcze raz.")
            self.result_label.setStyleSheet("color: #F44336; font-weight: bold")
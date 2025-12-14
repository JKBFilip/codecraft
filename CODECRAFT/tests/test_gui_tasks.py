from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from app.views.task_screen import TaskScreen
from app.models.task import Task

# prosty mock uzytkownika
class UdawanyGracz:
    def __init__(self):
        self.module_scores = {}
        self.completed_tasks = set()
        self.task_solutions = {}

    def complete_task(self, task_id, lesson_index):
        self.completed_tasks.add(task_id)

    def save_task_answer(self, task_id, answer):
        self.task_solutions[task_id] = {"answer": answer}

    def check_achievements(self):
        return []

# mock glownego okna z podpietym graczem
class UdawaneOkno:
    def __init__(self):
        self.lesson_index = 1
        self.current_task_index = 0
        self.user_account = UdawanyGracz()
        self.user_progress = self.user_account

    def show_achievement_notification(self, a): pass
    def previous_task(self): pass
    def next_task(self): pass
    def show_lesson(self): pass

# sprawdzamy czy zaliczy dobre rozwiazanie
def test_task_check_correct(qtbot, setup_fake_dirs):
    okno = UdawaneOkno()

    zadanie = Task(1, "Pytanie", "print('ok')", "code_input")

    ekran = TaskScreen(okno)
    ekran.filtered_tasks = [zadanie]
    ekran.update_task()
    qtbot.addWidget(ekran)

    ekran.code_input.setPlainText("print('ok')")

    qtbot.mouseClick(ekran.check_button, Qt.MouseButton.LeftButton)

    assert "Poprawna" in ekran.result_label.text()

# testujemy czy podpowiedz dziala
def test_task_hint(qtbot, setup_fake_dirs, monkeypatch):
    okno = UdawaneOkno()
    zadanie = Task(1, "Pytanie", "A", "multiple_choice", ["A: opcja", "B: inna"])

    ekran = TaskScreen(okno)
    ekran.filtered_tasks = [zadanie]
    ekran.update_task()
    qtbot.addWidget(ekran)

    okienko_otwarte = False
    def zlap_dialog(self):
        nonlocal okienko_otwarte
        okienko_otwarte = True

    monkeypatch.setattr(QDialog, "exec", zlap_dialog)

    qtbot.mouseClick(ekran.hint_button, Qt.MouseButton.LeftButton)
    assert okienko_otwarte is True
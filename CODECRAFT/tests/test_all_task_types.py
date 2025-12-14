from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from app.views.task_screen import TaskScreen
from app.models.task import Task
from app.models.auth.user_account import UserAccount

class UdawaneOkno:
    def __init__(self):
        self.lesson_index = 1
        self.current_task_index = 0
        self.user_account = UserAccount("types_user")
        self.user_progress = self.user_account

    def show_achievement_notification(self, a): pass
    def previous_task(self): pass
    def next_task(self): pass
    def show_lesson(self): pass

# sprawdzamy czy kazdy rodzaj zadania da sie zaliczyc i oblac
def test_sprawdzania_zadan(qtbot, setup_fake_dirs, monkeypatch):
    okno = UdawaneOkno()
    ekran = TaskScreen(okno)
    qtbot.addWidget(ekran)

    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    zadanie_kod = Task(1, "Q", "x = 1", "code_input", task_index=100)
    ekran.filtered_tasks = [zadanie_kod]
    ekran.update_task()

    ekran.code_input.setPlainText("  x=1  ")
    qtbot.mouseClick(ekran.check_button, Qt.MouseButton.LeftButton)
    assert "Poprawna" in ekran.result_label.text()

    zadanie_wynik = Task(1, "Q", "5", "code_output", task_index=101)
    ekran.filtered_tasks = [zadanie_wynik]
    ekran.update_task()

    ekran.code_input.setPlainText("999")
    qtbot.mouseClick(ekran.check_button, Qt.MouseButton.LeftButton)

    assert "Spróbuj" in ekran.result_label.text()

    zadanie_wybor = Task(1, "Q", "A", "multiple_choice", ["A: Tak", "B: Nie"], task_index=102)
    ekran.filtered_tasks = [zadanie_wybor]
    ekran.update_task()

    ekran.option_select.setCurrentText("A: Tak")
    qtbot.mouseClick(ekran.check_button, Qt.MouseButton.LeftButton)
    assert "Poprawna" in ekran.result_label.text()

    zadanie_wybor_2 = Task(1, "Q2", "A", "multiple_choice", ["A: Tak", "B: Nie"], task_index=103)
    ekran.filtered_tasks = [zadanie_wybor_2]
    ekran.update_task()

    ekran.option_select.setCurrentText("B: Nie")
    qtbot.mouseClick(ekran.check_button, Qt.MouseButton.LeftButton)
    assert "Spróbuj" in ekran.result_label.text()

    zadanie_ukladanka = Task(1, "Q", "linia1\nlinia2", "reorder", ["linia2", "linia1"], task_index=104)
    ekran.current_task = zadanie_ukladanka
    assert ekran._validate_answer("linia1\nlinia2") is True
    assert ekran._validate_answer("linia2\nlinia1") is False
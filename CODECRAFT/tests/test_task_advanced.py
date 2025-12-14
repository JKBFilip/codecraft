from PySide6.QtCore import Qt
from app.views.task_screen import TaskScreen
from app.models.task import Task

# podstawowy mock gracza
class UdawanyGracz:
    def __init__(self):
        self.module_scores = {}
        self.completed_tasks = set()
        self.task_solutions = {}
        self.username = "testowy_gracz"

    def complete_task(self, task_id, lesson_index):
        self.completed_tasks.add(task_id)

    def save_task_answer(self, task_id, answer):
        self.task_solutions[task_id] = {"answer": answer}

    def check_achievements(self):
        return []

# mock okna glownego
class UdawaneOkno:
    def __init__(self):
        self.lesson_index = 1
        self.current_task_index = 0
        self.user_account = UdawanyGracz()
        self.user_progress = self.user_account

    def previous_task(self):
        if self.current_task_index > 0: self.current_task_index -= 1
    def next_task(self):
        self.current_task_index += 1
    def show_lesson(self): pass
    def show_achievement_notification(self, a): pass

# sprawdzamy czy ukladanka (reorder) dziala jak trzeba
def test_task_reorder_logic(qtbot, setup_fake_dirs):
    okno = UdawaneOkno()

    # wazne zeby solution pasowalo do elementow listy (laczenie przez \n)
    zadanie = Task(1, "Ułóż kod", "linia1\nlinia2", "reorder", ["linia2", "linia1"])

    ekran = TaskScreen(okno)
    ekran.filtered_tasks = [zadanie]
    ekran.update_task()
    qtbot.addWidget(ekran)

    # ukladamy dobra odpowiedz
    ekran.reorder_list.clear()
    ekran.reorder_list.addItem("linia1")
    ekran.reorder_list.addItem("linia2")

    qtbot.mouseClick(ekran.check_button, Qt.MouseButton.LeftButton)

    assert "Poprawna" in ekran.result_label.text()

# sprawdzamy czy przyciski nawigacji zmieniaja indeksy zadan
def test_task_navigation_bounds(qtbot, setup_fake_dirs):
    okno = UdawaneOkno()
    zadanie1 = Task(1, "T1", "A", "code_input")
    zadanie2 = Task(1, "T2", "B", "code_input")

    ekran = TaskScreen(okno)
    ekran.filtered_tasks = [zadanie1, zadanie2]
    ekran.update_task()
    qtbot.addWidget(ekran)

    # Jestesmy na 0, klikamy Dalej
    qtbot.mouseClick(ekran.next_button, Qt.MouseButton.LeftButton)
    assert okno.current_task_index == 1

    # Jestesmy na 1, klikamy Wstecz
    qtbot.mouseClick(ekran.prev_button, Qt.MouseButton.LeftButton)
    assert okno.current_task_index == 0
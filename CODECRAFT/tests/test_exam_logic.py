from PySide6.QtCore import Qt
from app.views.final_exam_screen import FinalExamScreen
from app.models.auth.user_account import UserAccount
from app.models.task import Task


class UdawaneOkno:
    def __init__(self, user):
        self.user_account = user
        self.user_progress = user

    def show_menu(self): pass


# sprawdzamy czy egzamin dobrze ocenia odpowiedzi
def test_exam_answering_questions(qtbot, setup_fake_dirs, monkeypatch):
    gracz = UserAccount.register("student_pilny", "pass")
    okno = UdawaneOkno(gracz)

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    # Podmieniamy losowanie zadan, zeby miec pewnosc co dostaniemy
    def podstawione_zadania():
        t1 = Task(1, "Pytanie 1", "odp1", "code_input")
        t2 = Task(1, "Pytanie 2", "A", "multiple_choice", ["A: odp", "B: zla"])
        return [t1, t2]

    screen_tasks = podstawione_zadania()
    # Wstrzykujemy zadania recznie (omijamy prepare_and_display zeby bylo szybciej)
    ekran.tasks = screen_tasks

    # Uruchamiamy
    ekran._start_exam()

    # --- Pytanie 1: Code Input ---
    assert ekran.current_index == 0
    assert ekran.answer_stack.currentWidget() == ekran.code_input

    # Wpisujemy poprawna odpowiedz
    ekran.code_input.setPlainText("odp1")
    qtbot.mouseClick(ekran.submit_button, Qt.MouseButton.LeftButton)

    # Powinno zaliczyc i przejsc dalej
    assert ekran.correct_answers == 1
    assert ekran.current_index == 1

    # --- Pytanie 2: Multiple Choice ---
    assert ekran.answer_stack.currentWidget() == ekran.option_select

    # Wybieramy BLEDNA odpowiedz
    ekran.option_select.setCurrentText("B: zla")
    qtbot.mouseClick(ekran.submit_button, Qt.MouseButton.LeftButton)

    # Wynik nie powinien wzrosnac, egzamin powinien sie skonczyc (bo to bylo ostatnie zadanie)
    assert ekran.correct_answers == 1
    assert ekran.stack.currentWidget() == ekran.results_page

    # Sprawdzamy wynik procentowy (1 z 2 = 50%)
    assert ekran.score_percentage == 50.0
    assert "niezaliczony" in ekran.results_title.text().lower()
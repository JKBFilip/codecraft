from PySide6.QtCore import Qt
from app.views.final_test_screen import FinalTestScreen
from app.views.final_exam_screen import FinalExamScreen
from app.models.auth.user_account import UserAccount
from app.models.task import Task

class UdawaneOkno:
    def __init__(self, user):
        self.user_account = user
        self.user_progress = user
    def show_menu(self): pass
    def check_achievements(self): return []
    def show_achievement_notification(self, a): pass

# sprawdzamy czy licznik zmienia kolor jak zostalo malo czasu
def test_timer_color_change(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("pan_zegarek", "pass")
    okno = UdawaneOkno(uzytkownik)

    ekran = FinalTestScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    ekran.remaining_time = 240
    ekran.update_timer()
    assert "color: #f44336" not in ekran.timer_label.styleSheet()

    ekran.remaining_time = 59
    ekran.update_timer()
    assert "color: #f44336" in ekran.timer_label.styleSheet()

# testujemy co sie stanie jak baza zadań wybuchnie
def test_exam_loading_error(qtbot, monkeypatch, setup_fake_dirs):
    uzytkownik = UserAccount.register("pan_blad", "pass")
    okno = UdawaneOkno(uzytkownik)

    def wybuch():
        raise ValueError("Baza danych wybuchła")

    monkeypatch.setattr(Task, "load_all", wybuch)

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    zadania = ekran._prepare_exam_tasks()
    assert zadania == []

# sprawdzamy czy aplikacja przezyje blad przy sprawdzaniu odpowiedzi
def test_check_answer_exception(qtbot, monkeypatch, setup_fake_dirs):
    uzytkownik = UserAccount.register("pan_psuja", "pass")
    okno = UdawaneOkno(uzytkownik)

    ekran = FinalTestScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    ekran.test_tasks = [Task(1, "Q", "A", "code_input")]
    ekran.load_task()

    def rzuc_bledem():
        raise Exception("Błąd UI")

    ekran.code_input.toPlainText = rzuc_bledem

    qtbot.mouseClick(ekran.submit_button, Qt.MouseButton.LeftButton)

    assert True
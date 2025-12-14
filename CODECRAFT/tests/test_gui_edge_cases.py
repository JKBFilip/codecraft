from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from app.views.main_window import MainWindow
from app.views.final_exam_screen import FinalExamScreen
from app.views.final_test_screen import FinalTestScreen
from app.models.auth.user_account import UserAccount
from app.models.task import Task

# sprawdzamy czy postep sie zapisuje jak zamkniemy okno recznie
def test_main_window_close_event(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("zamykacz", "pass")
    okno = MainWindow()
    okno.user_account = uzytkownik
    qtbot.addWidget(okno)

    zdarzenie = QCloseEvent()
    okno.closeEvent(zdarzenie)

    assert okno.user_account is not None

# testujemy co sie dzieje jak czas sie skonczy na egzaminie
def test_exam_timeout(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("spoznialski", "pass")
    uzytkownik.apply_cheat_code("MAX_MODULES")

    okno = MainWindow()
    okno.user_account = uzytkownik

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    ekran.prepare_and_display()
    qtbot.mouseClick(ekran.start_button, Qt.MouseButton.LeftButton)

    ekran.remaining_time = 0
    ekran.update_timer()

    assert "niezaliczony" in ekran.results_title.text().lower()
    assert ekran.exam_passed is False

# sprawdzamy czy jak ktos obleje to nie dostanie certyfikatu
def test_exam_fail_score(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("pechowiec", "pass")
    uzytkownik.apply_cheat_code("MAX_MODULES")

    okno = MainWindow()
    okno.user_account = uzytkownik

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)
    ekran.prepare_and_display()
    qtbot.mouseClick(ekran.start_button, Qt.MouseButton.LeftButton)

    ekran.end_exam()

    assert ekran.exam_passed is False
    assert ekran.download_cert_button.isVisible() is False

# testujemy czy perfekcyjny wynik jest dobrze oznaczony
def test_final_test_perfect_score(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("kujon", "pass")
    okno = MainWindow()
    okno.user_account = uzytkownik

    ekran = FinalTestScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    ekran.correct_answers = len(ekran.test_tasks)

    ekran.end_test()

    assert "Perfekcyjnie" in ekran.final_result_label.text() or "100%" in ekran.final_result_label.text()

# sprawdzamy co sie stanie jak zabraknie zadan do egzaminu
def test_not_enough_tasks_for_exam(qtbot, monkeypatch):
    monkeypatch.setattr(Task, "load_all", lambda: [])

    uzytkownik = UserAccount("pusty_user")
    okno = MainWindow()
    okno.user_account = uzytkownik

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    zadania = ekran._prepare_exam_tasks()
    assert len(zadania) == 0
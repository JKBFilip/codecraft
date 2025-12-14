from PySide6.QtCore import Qt
from app.views.final_exam_screen import FinalExamScreen
from app.views.final_test_screen import FinalTestScreen
from app.models.auth.user_account import UserAccount

class UdawaneOkno:
    def __init__(self, user):
        self.user_account = user
        self.user_progress = user # Alias

    def show_menu(self): pass
    def check_achievements(self): return []
    def show_achievement_notification(self, achs): pass

# sprawdzamy czy egzamin dziala jak trzeba
def test_final_exam_flow(qtbot, setup_fake_dirs, monkeypatch):
    uzytkownik = UserAccount.register("student_egzaminu", "pass")
    uzytkownik.apply_cheat_code("MAX_MODULES")

    okno = UdawaneOkno(uzytkownik)

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    ekran.prepare_and_display()
    qtbot.mouseClick(ekran.start_button, Qt.MouseButton.LeftButton)

    assert ekran.stack.currentWidget() == ekran.exam_page

    ekran.end_exam()

    assert ekran.stack.currentWidget() == ekran.results_page
    assert "niezaliczony" in ekran.results_title.text().lower()

# testujemy czy test modulu dziala
def test_module_test_flow(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("student_testu", "pass")
    okno = UdawaneOkno(uzytkownik)

    ekran = FinalTestScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    assert len(ekran.test_tasks) > 0

    qtbot.mouseClick(ekran.submit_button, Qt.MouseButton.LeftButton)

    assert ekran.current_index == 1
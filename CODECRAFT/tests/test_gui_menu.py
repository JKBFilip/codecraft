from app.views.menu_screen import MenuScreen
from app.models.auth.user_account import UserAccount


class UdawaneOkno:
    def __init__(self):
        self.user_account = None
        self.user_progress = None

    def show_final_exam(self): pass

    def select_lesson(self, idx): pass

    def show_achievements(self): pass

    def show_cheat_code_prompt(self): pass


# sprawdzamy czy menu sie odswieza jak uzytkownik cos zrobi
def test_menu_updates(qtbot, setup_fake_dirs):
    uzytkownik = UserAccount.register("bywalec_menu", "pass")

    uzytkownik.module_scores["1"] = 16
    uzytkownik.completed_tasks.add("final_test_1")

    okno = UdawaneOkno()
    okno.user_account = uzytkownik
    okno.user_progress = uzytkownik

    ekran = MenuScreen(okno)
    qtbot.addWidget(ekran)

    ekran.update_module_widgets()

    assert "bywalec_menu" in ekran.welcome_label.text()

    modul_pierwszy = ekran.module_widgets[1]
    assert "16/16" in modul_pierwszy['progress_label'].text()
    assert modul_pierwszy['test_icon'].text() == "✔️"
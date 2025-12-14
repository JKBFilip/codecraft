from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QInputDialog
from app.views.main_window import MainWindow
from app.models.auth.user_account import UserAccount


# sprawdzamy czy jak wpiszemy dobry kod to zadziala
def test_cheat_code_flow_success(qtbot, monkeypatch, setup_fake_dirs):
    uzytkownik = UserAccount.register("cziter_gui", "pass")
    okno = MainWindow()
    okno.user_account = uzytkownik

    qtbot.addWidget(okno)
    okno.show_menu()

    def wpisz_kod(parent, title, label):
        return "MAX_MODULES", True

    monkeypatch.setattr(QInputDialog, "getText", wpisz_kod)

    pokazalo_info = False

    def zlap_info(parent, title, text):
        nonlocal pokazalo_info
        pokazalo_info = True
        assert "Odblokowano" in text

    monkeypatch.setattr(QMessageBox, "information", zlap_info)

    qtbot.mouseClick(okno.menu_screen.cheats_button, Qt.MouseButton.LeftButton)

    assert pokazalo_info is True
    assert uzytkownik.module_scores.get("1") == 16


# testujemy czy jak anulujemy to nic sie nie stanie
def test_cheat_code_cancel(qtbot, monkeypatch, setup_fake_dirs):
    uzytkownik = UserAccount.register("niezdecydowany", "pass")
    okno = MainWindow()
    okno.user_account = uzytkownik
    qtbot.addWidget(okno)
    okno.show_menu()

    monkeypatch.setattr(QInputDialog, "getText", lambda p, t, l: ("KOD", False))

    # jak cos wyskoczy to blad
    monkeypatch.setattr(QMessageBox, "information", lambda p, t, tx: False)

    qtbot.mouseClick(okno.menu_screen.cheats_button, Qt.MouseButton.LeftButton)


# sprawdzamy cwaniakow bez logowania
def test_cheat_code_no_user(qtbot, monkeypatch):
    okno = MainWindow()
    qtbot.addWidget(okno)

    ostrzezenie_byl = False

    def zlap_ostrzezenie(parent, title, text):
        nonlocal ostrzezenie_byl
        ostrzezenie_byl = True
        assert "zalogowany" in text

    monkeypatch.setattr(QMessageBox, "warning", zlap_ostrzezenie)

    okno.show_cheat_code_prompt()
    assert ostrzezenie_byl is True
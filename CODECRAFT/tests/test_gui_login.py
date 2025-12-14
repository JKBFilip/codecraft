from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from app.views.auth.login_screen import LoginScreen
from app.models.auth.user_account import UserAccount

class UdawaneOkno:
    def __init__(self):
        self.user_account = None
    def show_menu(self): pass
    def show_register_screen(self): pass
    def show_password_reset_screen(self): pass

# sprawdzamy czy jak sie wpisze dobre dane to zaloguje
def test_login_gui_success(qtbot, setup_fake_dirs, monkeypatch):
    UserAccount.register("tester_logowania", "tajnehaslo")

    okno = UdawaneOkno()
    ekran = LoginScreen(okno)
    qtbot.addWidget(ekran)

    qtbot.keyClicks(ekran.username_input, "tester_logowania")
    qtbot.keyClicks(ekran.password_input, "tajnehaslo")

    qtbot.mouseClick(ekran.login_btn, Qt.MouseButton.LeftButton)

    assert okno.user_account is not None
    assert okno.user_account.username == "tester_logowania"

# testujemy czy krzyczy jak sie nic nie wpisze
def test_login_gui_empty_fields(qtbot, setup_fake_dirs, monkeypatch):
    pokazalo_blad = False

    def zlap_ostrzezenie(parent, title, text):
        nonlocal pokazalo_blad
        pokazalo_blad = True
        assert text == "Nazwa użytkownika i hasło są wymagane."

    monkeypatch.setattr(QMessageBox, "warning", zlap_ostrzezenie)

    okno = UdawaneOkno()
    ekran = LoginScreen(okno)
    qtbot.addWidget(ekran)

    qtbot.mouseClick(ekran.login_btn, Qt.MouseButton.LeftButton)

    assert pokazalo_blad is True
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from app.views.auth.register_screen import RegisterScreen


class UdawaneOkno:
    def __init__(self):
        self.user_account = None
    def show_login_screen(self): pass
    def show_menu(self): pass

# sprawdzamy czy aplikacja blokuje zle hasla
def test_register_validation_error(qtbot, setup_fake_dirs, monkeypatch):
    okno = UdawaneOkno()
    ekran = RegisterScreen(okno)
    qtbot.addWidget(ekran)

    ostatni_blad = None
    def zlap_ostrzezenie(parent, title, text):
        nonlocal ostatni_blad
        ostatni_blad = text
    monkeypatch.setattr(QMessageBox, "warning", zlap_ostrzezenie)

    qtbot.keyClicks(ekran.username_input, "user")
    qtbot.keyClicks(ekran.password_input, "123")
    qtbot.keyClicks(ekran.confirm_input, "123")
    qtbot.mouseClick(ekran.register_btn, Qt.MouseButton.LeftButton)
    assert "co najmniej 6 znaków" in ostatni_blad

    qtbot.keyClicks(ekran.password_input, "haslo123")
    ekran.confirm_input.clear()
    qtbot.keyClicks(ekran.confirm_input, "innehaslo")
    qtbot.mouseClick(ekran.register_btn, Qt.MouseButton.LeftButton)
    assert "nie są identyczne" in ostatni_blad

# testujemy czy da sie zalozyc konto
def test_register_success(qtbot, setup_fake_dirs, monkeypatch):
    okno = UdawaneOkno()
    ekran = RegisterScreen(okno)
    qtbot.addWidget(ekran)

    sukces = False
    def zlap_info(parent, title, text):
        nonlocal sukces
        sukces = True
    monkeypatch.setattr(QMessageBox, "information", zlap_info)

    ekran.username_input.setText("nowy_rejestrat")
    ekran.password_input.setText("tajneHaslo123")
    ekran.confirm_input.setText("tajneHaslo123")

    qtbot.mouseClick(ekran.register_btn, Qt.MouseButton.LeftButton)

    assert sukces is True
    assert okno.user_account is not None
    assert okno.user_account.username == "nowy_rejestrat"
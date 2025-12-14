import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from app.models.auth.password_reset_screen import PasswordResetScreen
from app.models.auth.user_account import UserAccount

class UdawaneOkno:
    def __init__(self):
        pass
    def show_login_screen(self): pass

# sprawdzamy czy formularz krzyczy jak sie cos zle wpisze
def test_reset_validation(qtbot, setup_fake_dirs, monkeypatch):
    okno = UdawaneOkno()
    ekran = PasswordResetScreen(okno)
    qtbot.addWidget(ekran)

    ostatni_blad = None
    def zlap_ostrzezenie(parent, title, text):
        nonlocal ostatni_blad
        ostatni_blad = text

    monkeypatch.setattr(QMessageBox, "warning", zlap_ostrzezenie)

    qtbot.mouseClick(ekran.reset_btn, Qt.MouseButton.LeftButton)
    assert "wymagane" in ostatni_blad

    ekran.username_input.setText("user")
    ekran.new_password_input.setText("haslo1")
    ekran.confirm_password_input.setText("haslo2")
    qtbot.mouseClick(ekran.reset_btn, Qt.MouseButton.LeftButton)
    assert "nie są identyczne" in ostatni_blad

    ekran.new_password_input.setText("123")
    ekran.confirm_password_input.setText("123")
    qtbot.mouseClick(ekran.reset_btn, Qt.MouseButton.LeftButton)
    assert "co najmniej 6 znaków" in ostatni_blad

# testujemy czy zmiana hasla faktycznie dziala
def test_reset_success(qtbot, setup_fake_dirs, monkeypatch):
    UserAccount.register("zapominalski", "stareHaslo")

    okno = UdawaneOkno()
    ekran = PasswordResetScreen(okno)
    qtbot.addWidget(ekran)

    sukces = False
    def zlap_info(parent, title, text):
        nonlocal sukces
        sukces = True

    monkeypatch.setattr(QMessageBox, "information", zlap_info)

    ekran.username_input.setText("zapominalski")
    ekran.new_password_input.setText("noweHaslo")
    ekran.confirm_password_input.setText("noweHaslo")

    qtbot.mouseClick(ekran.reset_btn, Qt.MouseButton.LeftButton)

    assert sukces is True

    with pytest.raises(ValueError):
        UserAccount.login("zapominalski", "stareHaslo")

    uzytkownik = UserAccount.login("zapominalski", "noweHaslo")
    assert uzytkownik is not None
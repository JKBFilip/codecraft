from app.views.main_window import MainWindow
from app.models.auth.user_account import UserAccount

# sprawdzamy czy aplikacja w ogole wstaje i ma wszystkie ekrany
def test_main_window_init(qtbot, setup_fake_dirs):
    okno = MainWindow()
    qtbot.addWidget(okno)

    assert okno.stack.count() > 0
    assert okno.login_screen is not None
    assert okno.menu_screen is not None

    assert okno.user_account is None
    assert okno.logout_button.isHidden()

# testujemy przelaczanie miedzy ekranami
def test_main_window_navigation(qtbot, setup_fake_dirs):
    okno = MainWindow()
    qtbot.addWidget(okno)

    okno.show_register_screen()
    assert okno.stack.currentWidget() == okno.register_screen

    okno.show_password_reset_screen()
    assert okno.stack.currentWidget() == okno.password_reset_screen

    okno.show_login_screen()
    assert okno.stack.currentWidget() == okno.login_screen

# sprawdzamy czy wylogowanie dziala i czysci usera
def test_logout_flow(qtbot, setup_fake_dirs):
    okno = MainWindow()
    qtbot.addWidget(okno)

    uzytkownik = UserAccount.register("tester_wylogowania", "pass")
    okno.user_account = uzytkownik

    okno.logout()

    assert okno.user_account is None
    assert okno.stack.currentWidget() == okno.login_screen
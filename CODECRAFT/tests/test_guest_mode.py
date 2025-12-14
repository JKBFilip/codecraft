from app.views.main_window import MainWindow
from app.models.auth.user_account import UserAccount

# sprawdzamy czy tworzy sie konto goscia jak nikt sie nie zaloguje
def test_guest_account_creation(qtbot):
    okno = MainWindow()
    qtbot.addWidget(okno)

    assert okno.user_account is None

    gosc = okno.user_progress

    assert gosc is not None
    assert gosc.username == "guest"
    assert hasattr(okno, '_guest_account')

# sprawdzamy czy logi przy ladowaniu danych dzialaja i nic nie wywala
def test_load_data_logs(capsys, setup_fake_dirs):
    okno = MainWindow()
    uzytkownik = UserAccount.register("log_user", "pass")
    okno.user_account = uzytkownik

    uzytkownik.load_all_data()
    # jak przeszlo bez bledu to jest git
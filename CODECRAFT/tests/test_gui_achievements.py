from PySide6.QtWidgets import QLabel
from app.views.achievements_screen import AchievementsScreen
from app.models.auth.user_account import UserAccount


class UdawaneOkno:
    def __init__(self, user):
        self.user_account = user

    def show_menu(self): pass


# sprawdzamy czy nagrody sie w ogole pokazuja na liscie
def test_achievements_display(qtbot, setup_fake_dirs):
    gracz = UserAccount.register("gracz_gui", "pass")

    gracz._unlocked_achievements.add("first_task")

    okno = UdawaneOkno(gracz)
    ekran = AchievementsScreen(okno)
    qtbot.addWidget(ekran)

    ekran.refresh_achievements()

    etykiety = ekran.content_widget.findChildren(QLabel)

    znaleziono_odblokowane = False
    znaleziono_zablokowane = False

    for lbl in etykiety:
        tekst = lbl.text()
        styl = lbl.styleSheet()

        if "Pierwszy krok" in tekst and "background-color: #283636" in styl:
            znaleziono_odblokowane = True
        if "Mistrz" in tekst and "🔒" in tekst:
            znaleziono_zablokowane = True

    assert znaleziono_odblokowane is True
    assert znaleziono_zablokowane is True


# testujemy co sie stanie jak wejdziemy bez logowania
def test_achievements_no_user(qtbot):
    okno = UdawaneOkno(None)
    ekran = AchievementsScreen(okno)
    qtbot.addWidget(ekran)

    ekran.refresh_achievements()

    etykiety = ekran.content_widget.findChildren(QLabel)
    assert any("Błąd" in lbl.text() for lbl in etykiety)
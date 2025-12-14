from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from app.views.final_exam_screen import FinalExamScreen
from app.models.auth.user_account import UserAccount

class UdawaneOkno:
    def __init__(self, user):
        self.user_account = user
        self.user_progress = user
    def show_menu(self): pass

# sprawdzamy czy da sie uciec do menu jak sie skonczy egzamin
def test_exam_back_to_menu(qtbot, setup_fake_dirs):
    gracz = UserAccount.register("uciekinier", "pass")
    okno = UdawaneOkno(gracz)

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    ekran.end_exam(timeout=True)

    assert ekran.stack.currentWidget() == ekran.results_page

    uklad = ekran.results_page.layout()
    guzik_powrotu = uklad.itemAt(uklad.count() - 1).widget()

    assert "Powrót" in guzik_powrotu.text()

    qtbot.mouseClick(guzik_powrotu, Qt.MouseButton.LeftButton)

# testujemy cwaniaka co chce pobrac dyplom bez zdania
def test_download_cert_not_passed(qtbot, monkeypatch, setup_fake_dirs):
    gracz = UserAccount.register("cwaniak", "pass")
    okno = UdawaneOkno(gracz)

    ekran = FinalExamScreen(okno)
    qtbot.addWidget(ekran)

    ekran.exam_passed = False

    ostrzezenia = []
    def lapacz_ostrzezen(parent, title, text):
        ostrzezenia.append(text)
        assert "nie został zaliczony" in text

    monkeypatch.setattr(QMessageBox, "warning", lapacz_ostrzezen)

    ekran.download_certificate()

    assert len(ostrzezenia) > 0
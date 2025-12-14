from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from app.views.final_exam_screen import FinalExamScreen, CertificateGenerator
from app.models.auth.user_account import UserAccount

class MockMainWindow:
    def __init__(self, user):
        self.user_account = user
        self.user_progress = user
    def show_menu(self): pass

# sprawdzamy czy da sie pobrac certyfikat jak sie zda
def test_download_certificate_flow(qtbot, setup_fake_dirs, monkeypatch):
    user = UserAccount.register("cert_user_final", "pass")
    user.add_test_result(0, 90.0, perfect_score=True, time_taken=100)

    window = MockMainWindow(user)
    screen = FinalExamScreen(window)
    qtbot.addWidget(screen)

    screen.prepare_and_display()

    screen.exam_passed = True
    screen.download_cert_button.setVisible(True)

    monkeypatch.setattr(CertificateGenerator, "generate", lambda *args, **kwargs: "fake_cert.png")

    msgs = []
    monkeypatch.setattr(QMessageBox, "information", lambda parent, title, text: msgs.append(text))

    qtbot.mouseClick(screen.download_cert_button, Qt.MouseButton.LeftButton)

    assert len(msgs) > 0
    assert "fake_cert.png" in msgs[0]

# testujemy co jak drukarka padnie albo cos innego wywali
def test_download_certificate_fail(qtbot, setup_fake_dirs, monkeypatch):
    user = UserAccount.register("fail_cert_final", "pass")

    window = MockMainWindow(user)
    screen = FinalExamScreen(window)
    qtbot.addWidget(screen)

    screen.prepare_and_display()

    screen.exam_passed = True
    screen.score_percentage = 80.0

    def zepsuty_generator(*args, **kwargs):
        raise Exception("Błąd drukarki")

    monkeypatch.setattr(CertificateGenerator, "generate", zepsuty_generator)

    wars = []
    monkeypatch.setattr(QMessageBox, "warning", lambda parent, title, text: wars.append(text))

    qtbot.mouseClick(screen.download_cert_button, Qt.MouseButton.LeftButton)

    assert len(wars) > 0
    assert "Nie udało się" in wars[0]
    assert "Błąd drukarki" in wars[0]
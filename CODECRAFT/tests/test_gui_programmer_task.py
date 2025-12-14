from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QTextEdit
from app.views.lesson_screen import LessonScreen, ProgrammerTaskDialog, CodeViewerDialog

class UdawaneOkno:
    def show_task(self): pass
    def start_final_test(self): pass
    def show_menu(self): pass

# sprawdzamy czy guzik otwiera to dodatkowe zadanie
def test_programmer_task_button(qtbot, monkeypatch):
    okno = UdawaneOkno()
    ekran = LessonScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    ostatnia_strona = len(ekran.theory_pages) - 1
    ekran.page = ostatnia_strona
    ekran.update_page()

    dialog_otwarty = False
    def zlap_dialog(self):
        nonlocal dialog_otwarty
        dialog_otwarty = True
        assert "Przelicznik Odległości" in self.instruction_browser.toHtml()

    monkeypatch.setattr(ProgrammerTaskDialog, "exec", zlap_dialog)

    qtbot.mouseClick(ekran.programmer_task_button, Qt.MouseButton.LeftButton)

    assert dialog_otwarty is True

# testujemy czy da sie podejrzej gotowca
def test_programmer_task_solution(qtbot, monkeypatch):
    dialog = ProgrammerTaskDialog("Instrukcja", "print('Solution')")
    qtbot.addWidget(dialog)

    podglad_otwarty = False
    def zlap_podglad(self):
        nonlocal podglad_otwarty
        podglad_otwarty = True
        assert "print('Solution')" in self.findChild(QTextEdit).toPlainText()

    monkeypatch.setattr(CodeViewerDialog, "exec", zlap_podglad)

    qtbot.mouseClick(dialog.solution_button, Qt.MouseButton.LeftButton)

    assert podglad_otwarty is True

# sprawdzamy co jak nie ma zadania dla danej lekcji
def test_missing_programmer_task(qtbot, monkeypatch):
    okno = UdawaneOkno()
    # lekcja 100 nie istnieje
    ekran = LessonScreen(okno, lesson_index=100)
    qtbot.addWidget(ekran)

    komunikat_byl = False
    def zlap_info(parent, title, text):
        nonlocal komunikat_byl
        komunikat_byl = True
        assert "Brak" in text

    monkeypatch.setattr(QMessageBox, "information", zlap_info)

    ekran.show_programmer_task()

    assert komunikat_byl is True
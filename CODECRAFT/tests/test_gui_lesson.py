from PySide6.QtCore import Qt
from app.views.lesson_screen import LessonScreen

class UdawaneOkno:
    def show_task(self): pass
    def start_final_test(self): pass
    def show_menu(self): pass

# sprawdzamy czy przyciski nastepny/poprzedni dzialaja
def test_lesson_navigation(qtbot):
    okno = UdawaneOkno()
    ekran = LessonScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    assert ekran.page == 0
    assert ekran.prev_button.isEnabled() is False

    qtbot.mouseClick(ekran.next_button, Qt.MouseButton.LeftButton)
    assert ekran.page == 1
    assert ekran.prev_button.isEnabled() is True

    qtbot.mouseClick(ekran.prev_button, Qt.MouseButton.LeftButton)
    assert ekran.page == 0

# testujemy czy na koncu lekcji pokazuja sie przyciski zadan
def test_lesson_last_page_buttons(qtbot):
    okno = UdawaneOkno()
    ekran = LessonScreen(okno, lesson_index=1)
    qtbot.addWidget(ekran)

    # musimy pokazac okno zeby isVisible nie klamalo
    with qtbot.waitExposed(ekran):
        ekran.show()

    ostatnia_strona = len(ekran.theory_pages) - 1
    ekran.page = ostatnia_strona

    ekran.update_page()

    assert ekran.task_button.isVisible() is True
    assert ekran.test_button.isVisible() is True
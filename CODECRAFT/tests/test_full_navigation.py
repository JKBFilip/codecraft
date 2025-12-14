from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
from app.views.main_window import MainWindow
from app.models.task import Task


# testujemy czy da sie przejsc cala aplikacje od a do z bez wywalania sie
def test_full_app_walkthrough(qtbot, setup_fake_dirs, monkeypatch):
    okno = MainWindow()
    qtbot.addWidget(okno)

    # 1. Rejestracja zeby wejsc do srodka
    okno.show_register_screen()
    assert okno.stack.currentWidget() == okno.register_screen

    okno.register_screen.username_input.setText("wedrowiec")
    okno.register_screen.password_input.setText("haslo123")
    okno.register_screen.confirm_input.setText("haslo123")

    # uciszamy popupy
    monkeypatch.setattr(QMessageBox, "information", lambda *args: None)

    qtbot.mouseClick(okno.register_screen.register_btn, Qt.MouseButton.LeftButton)

    # 2. Sprawdzamy czy weszlo do menu
    assert okno.stack.currentWidget() == okno.menu_screen
    assert okno.user_account.username == "wedrowiec"

    # 3. Wybor modulu (klikamy w pierwszy kafelek)
    kafelek_modulu = okno.menu_screen.module_widgets[1]['card']
    qtbot.mouseClick(kafelek_modulu, Qt.MouseButton.LeftButton)

    # 4. Czy jestesmy w lekcji?
    assert okno.stack.currentWidget() == okno.lesson_screen
    assert okno.lesson_index == 1

    # 5. Przejscie do zadan (wymuszamy pokazanie przycisku bo nie chce mi sie klikac next 10 razy)
    okno.lesson_screen.task_button.setVisible(True)
    qtbot.mouseClick(okno.lesson_screen.task_button, Qt.MouseButton.LeftButton)

    assert okno.stack.currentWidget() == okno.task_screen

    # 6. Nawigacja po zadaniach (lewo prawo)
    if not okno.task_screen.filtered_tasks:
        okno.task_screen.filtered_tasks = [Task(1, "P1", "O1", "code"), Task(1, "P2", "O2", "code")]

    startowy_index = okno.current_task_index

    qtbot.mouseClick(okno.task_screen.next_button, Qt.MouseButton.LeftButton)
    assert okno.current_task_index == startowy_index + 1

    qtbot.mouseClick(okno.task_screen.prev_button, Qt.MouseButton.LeftButton)
    assert okno.current_task_index == startowy_index

    # 7. Powrot do lekcji
    qtbot.mouseClick(okno.task_screen.back_button, Qt.MouseButton.LeftButton)
    assert okno.stack.currentWidget() == okno.lesson_screen

    # 8. Przejscie do testu modulu
    okno.lesson_screen.test_button.setVisible(True)
    qtbot.mouseClick(okno.lesson_screen.test_button, Qt.MouseButton.LeftButton)
    assert okno.stack.currentWidget() == okno.final_test_screen

    # 9. Powrot do menu
    # (symulujemy klikniecie powrotu wolajac funkcje bezposrednio, bo guzik jest schowany w layoucie)
    okno.show_menu()
    assert okno.stack.currentWidget() == okno.menu_screen

    # 10. Egzamin koncowy (na kodach zeby bylo szybciej)
    okno.user_account.apply_cheat_code("MAX_MODULES")
    okno.menu_screen._update_final_exam_button_state()

    qtbot.mouseClick(okno.menu_screen.final_exam_button, Qt.MouseButton.LeftButton)

    # Skoro uzylismy kodow, to egzamin jest zaliczony, wiec powinnismy byc na ekranie wynikow
    # ale technicznie jest to ten sam widget FinalExamScreen
    assert okno.stack.currentWidget() == okno.final_exam_screen
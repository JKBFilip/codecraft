from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from app.views.menu_screen import MenuScreen
from app.views.lesson_screen import LessonScreen
from app.views.task_screen import TaskScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CODECRAFT")
        self.setMinimumSize(800, 600)

        self.lesson_index = 1
        self.current_task_index = 0

        self.menu_screen = MenuScreen(self)
        self.lesson_screen = None
        self.task_screen = TaskScreen(self)

        central_widget = QWidget()
        self.stack = QStackedLayout()
        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.task_screen)
        central_widget.setLayout(self.stack)
        self.setCentralWidget(central_widget)

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu_screen)

    def select_lesson(self, index):
        self.lesson_index = index
        self.current_task_index = 0
        self.show_lesson()

    def show_lesson(self):
        if self.lesson_screen:
            self.stack.removeWidget(self.lesson_screen)
            self.lesson_screen.deleteLater()

        self.lesson_screen = LessonScreen(self, self.lesson_index)
        self.stack.addWidget(self.lesson_screen)
        self.stack.setCurrentWidget(self.lesson_screen)

    def show_task(self):
        self.current_task_index = 0
        self.stack.setCurrentWidget(self.task_screen)

    def previous_task(self):
        if self.current_task_index > 0:
            self.current_task_index -= 1
            self.task_screen.update_task()

    def next_task(self):
        if self.current_task_index < len(self.task_screen.filtered_tasks) - 1:
            self.current_task_index += 1
            self.task_screen.update_task()

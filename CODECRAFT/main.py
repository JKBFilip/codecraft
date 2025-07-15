import sys
import os
from PySide6.QtWidgets import QApplication
from app.views.main_window import MainWindow

if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    style_path = os.path.join(os.path.dirname(__file__), "app/assets/style.qss")
    with open(style_path, "r") as f:
        qt_app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec())

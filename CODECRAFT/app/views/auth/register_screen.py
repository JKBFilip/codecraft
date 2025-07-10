from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount

class RegisterScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = QLabel("Rejestracja nowego konta")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika (min. 3 znaki)")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło (min. 6 znaków)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Potwierdź hasło")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.confirm_input)

        self.register_btn = QPushButton("Zarejestruj")
        self.register_btn.clicked.connect(self._handle_register)
        self.layout.addWidget(self.register_btn)

        self.back_btn = QPushButton("Powrót do logowania")
        self.back_btn.clicked.connect(self.main_window.show_login_screen)
        self.layout.addWidget(self.back_btn)

    def _handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if password != confirm:
            QMessageBox.warning(self, "Błąd", "Hasła nie są identyczne")
            return

        try:
            self.main_window.user_account = UserAccount.register(username, password)
            QMessageBox.information(self, "Sukces", "Konto zostało założone!")
            self.main_window.show_menu()
        except ValueError as e:
            QMessageBox.warning(self, "Błąd rejestracji", str(e))
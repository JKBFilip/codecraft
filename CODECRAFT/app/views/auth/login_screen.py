from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount

class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Logo/Title
        title = QLabel("CODECRAFT - Logowanie")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(title)

        # Form fields
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        # Buttons
        self.login_btn = QPushButton("Zaloguj")
        self.login_btn.clicked.connect(self._handle_login)
        self.layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Zarejestruj nowe konto")
        self.register_btn.clicked.connect(self._show_register)
        self.layout.addWidget(self.register_btn)

    def _handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            self.main_window.user_account = UserAccount.login(username, password)
            self.main_window.user_account.load_progress()
            self.main_window.show_menu()
        except ValueError as e:
            QMessageBox.warning(self, "Błąd logowania", str(e))

    def _show_register(self):
        self.main_window.show_register_screen()
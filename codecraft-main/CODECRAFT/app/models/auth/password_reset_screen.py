from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount


class PasswordResetScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Resetowanie hasła")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")
        layout.addWidget(self.username_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Nowe hasło")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Powtórz nowe hasło")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)

        self.reset_btn = QPushButton("Zresetuj hasło")
        self.reset_btn.clicked.connect(self._reset_password)
        layout.addWidget(self.reset_btn)

        self.back_btn = QPushButton("Powrót do logowania")
        self.back_btn.clicked.connect(self.main_window.show_login_screen)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def _reset_password(self):
        username = self.username_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not new_password or not confirm_password:
            QMessageBox.warning(self, "Błąd", "Wszystkie pola są wymagane!")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Błąd", "Hasła nie są identyczne!")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "Błąd", "Hasło musi mieć co najmniej 6 znaków!")
            return

        try:
            # Zmodyfikuj metodę reset_password w UserAccount
            UserAccount.reset_password(username, new_password)
            QMessageBox.information(self, "Sukces", "Hasło zostało zmienione!")
            self.main_window.show_login_screen()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))
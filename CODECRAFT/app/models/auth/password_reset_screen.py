from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount

class PasswordResetScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        form_frame = QFrame(self)
        form_frame.setObjectName("formFrame")
        form_frame.setMaximumWidth(400)

        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(15)

        title = QLabel("Resetowanie Hasła")
        title.setObjectName("resetTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Wprowadź nazwę użytkownika i ustaw nowe hasło.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Nazwa użytkownika")

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("🔑 Nowe hasło")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("🔑 Potwierdź nowe hasło")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.reset_btn = QPushButton("Zatwierdź zmianę")
        self.reset_btn.setObjectName("primaryButton")
        self.reset_btn.setMinimumHeight(45)
        self.reset_btn.clicked.connect(self._reset_password)

        self.back_btn = QPushButton("Powrót do logowania")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.clicked.connect(self.main_window.show_login_screen)

        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.new_password_input)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.reset_btn)
        form_layout.addWidget(self.back_btn)

        main_layout.addWidget(form_frame)

    def _reset_password(self):
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([username, new_password, confirm_password]):
            QMessageBox.warning(self, "Błąd", "Wszystkie pola są wymagane!")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Błąd", "Hasła nie są identyczne!")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "Błąd", "Hasło musi mieć co najmniej 6 znaków!")
            return

        try:
            UserAccount.reset_password(username, new_password)
            QMessageBox.information(self, "Sukces", "Hasło zostało pomyślnie zmienione!")
            self.main_window.show_login_screen()
        except ValueError as e:
            QMessageBox.critical(self, "Błąd", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Błąd Krytyczny", f"Wystąpił nieoczekiwany błąd: {e}")
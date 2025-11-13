from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount

class RegisterScreen(QWidget):
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

        title = QLabel("Stwórz nowe konto")
        title.setObjectName("registerTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Dołącz do CODECRAFT i rozpocznij swoją przygodę z programowaniem!")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Nazwa użytkownika (min. 3 znaki)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔑 Hasło (min. 6 znaków)")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("🔑 Potwierdź hasło")
        self.confirm_input.setEchoMode(QLineEdit.Password)

        self.register_btn = QPushButton("Zarejestruj się")
        self.register_btn.setObjectName("primaryButton")
        self.register_btn.setMinimumHeight(45)
        self.register_btn.clicked.connect(self._handle_register)

        self.back_btn = QPushButton("Masz już konto? Zaloguj się")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.clicked.connect(self.main_window.show_login_screen)

        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_input)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.register_btn)
        form_layout.addWidget(self.back_btn)

        main_layout.addWidget(form_frame)

    def _handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if len(username) < 3:
            QMessageBox.warning(self, "Błąd", "Nazwa użytkownika musi mieć co najmniej 3 znaki.")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Błąd", "Hasło musi mieć co najmniej 6 znaków.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Błąd", "Hasła nie są identyczne.")
            return

        try:
            new_user = UserAccount.register(username, password)
            self.main_window.user_account = new_user
            QMessageBox.information(self, "Sukces", f"Witaj, {username}! Twoje konto zostało pomyślnie założone.")
            self.main_window.show_menu()
        except ValueError as e:
            QMessageBox.warning(self, "Błąd rejestracji", str(e))
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount

class LoginScreen(QWidget):
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

        title = QLabel("Witaj w CODECRAFT")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Zaloguj się, aby kontynuować swoją naukę.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Nazwa użytkownika")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔑 Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Zaloguj się")
        self.login_btn.setObjectName("primaryButton")
        self.login_btn.setMinimumHeight(45)
        self.login_btn.clicked.connect(self._handle_login)

        self.register_btn = QPushButton("Nie masz konta? Zarejestruj się")
        self.register_btn.setObjectName("secondaryButton")
        self.register_btn.clicked.connect(self._show_register)

        self.forgot_password_btn = QPushButton("Zapomniałem hasła")
        self.forgot_password_btn.setObjectName("secondaryButton")
        self.forgot_password_btn.clicked.connect(self._show_password_reset)

        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.login_btn)
        form_layout.addWidget(self.register_btn)
        form_layout.addWidget(self.forgot_password_btn)

        main_layout.addWidget(form_frame)

    def _handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Błąd", "Nazwa użytkownika i hasło są wymagane.")
            return

        try:
            user = UserAccount.login(username, password)
            self.main_window.user_account = user
            self.main_window.user_account.load_all_data()
            self.main_window.show_menu()
        except ValueError as e:
            QMessageBox.warning(self, "Błąd logowania", str(e))

    def _show_register(self):
        self.main_window.show_register_screen()

    def _show_password_reset(self):
        self.main_window.show_password_reset_screen()
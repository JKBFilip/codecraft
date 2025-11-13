from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PySide6.QtCore import Qt
from app.models.auth.user_account import UserAccount


class LoginScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        """Tworzy nowoczesny, wyśrodkowany layout."""
        # --- Główny layout centrujący ---
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # --- Ramka-kontener na formularz ---
        form_frame = QFrame(self)
        form_frame.setObjectName("formFrame")  # Używa stylu z .qss
        form_frame.setMaximumWidth(400)

        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(15)

        # --- Nagłówki ---
        title = QLabel("Witaj w CODECRAFT")
        title.setObjectName("loginTitle")  # ID dla stylów QSS
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Zaloguj się, aby kontynuować swoją naukę.")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)

        # --- Pola do wprowadzania danych ---
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Nazwa użytkownika")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔑 Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        # --- Przyciski akcji ---
        self.login_btn = QPushButton("Zaloguj się")
        self.login_btn.setObjectName("primaryButton")  # Przycisk główny
        self.login_btn.setMinimumHeight(45)
        self.login_btn.clicked.connect(self._handle_login)

        self.register_btn = QPushButton("Nie masz konta? Zarejestruj się")
        self.register_btn.setObjectName("secondaryButton")  # Przycisk dodatkowy
        self.register_btn.clicked.connect(self._show_register)

        self.forgot_password_btn = QPushButton("Zapomniałem hasła")
        self.forgot_password_btn.setObjectName("secondaryButton")  # Również jako przycisk dodatkowy
        self.forgot_password_btn.clicked.connect(self._show_password_reset)

        # --- Dodawanie widgetów do layoutu formularza ---
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
            # Logowanie zwraca obiekt UserAccount
            user = UserAccount.login(username, password)
            self.main_window.user_account = user

            # Po pomyślnym zalogowaniu, wczytujemy postępy tego użytkownika
            self.main_window.user_account.load_all_data()

            # Przechodzimy do menu głównego
            self.main_window.show_menu()

        except ValueError as e:
            QMessageBox.warning(self, "Błąd logowania", str(e))

    def _show_register(self):
        self.main_window.show_register_screen()

    def _show_password_reset(self):
        self.main_window.show_password_reset_screen()
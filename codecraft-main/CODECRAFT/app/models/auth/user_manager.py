# app/models/auth/user_manager.py
from datetime import datetime
import json
from app.models.auth.user_account import UserAccount
import os


class UserManager:
    def __init__(self):
        self.user_data = {}  # Tylko do przechowywania podstawowych danych kont
        self._load_accounts()

    def _load_accounts(self):
        """Ładuje dane kont z pliku"""
        accounts_file = os.path.join(UserAccount.ACCOUNTS_DIR, "users.json")
        try:
            if os.path.exists(accounts_file):
                with open(accounts_file, 'r') as f:
                    self.user_data = json.load(f)
        except Exception as e:
            print(f"Błąd ładowania kont: {e}")
            self.user_data = {}

    def load_user(self, username):
        """Ładuje użytkownika - teraz używa osobnych plików dla każdego użytkownika"""
        if username not in self.user_data:
            raise ValueError("Użytkownik nie istnieje")

        # Tworzy nową instancję UserAccount, która sama ładuje swoje dane
        user = UserAccount(username)

        # Zweryfikuj czy dane zostały poprawnie załadowane
        if not hasattr(user, '_unlocked_achievements'):
            user._unlocked_achievements = set()

        return user

    def register_user(self, username, password):
        """Rejestracja nowego użytkownika"""
        if username in self.user_data:
            raise ValueError("Użytkownik już istnieje")

        # Tworzy nowe konto
        user = UserAccount(username)
        user.save_progress()  # Tworzy początkowe pliki

        # Generuje sól i hasło
        salt = os.urandom(16).hex()
        hashed_password = UserAccount._hash_password(password, salt)

        # Dodaje do bazy kont
        self.user_data[username] = {
            'salt': salt,
            'hashed_password': hashed_password,
            'created_at': datetime.now().isoformat()
        }
        self._save_accounts()

        return user

    def _save_accounts(self):
        """Zapisuje dane kont do pliku"""
        accounts_file = os.path.join(UserAccount.ACCOUNTS_DIR, "users.json")
        try:
            with open(accounts_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Błąd zapisu kont: {e}")
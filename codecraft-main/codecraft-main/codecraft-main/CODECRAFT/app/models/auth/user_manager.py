from datetime import datetime
import json
import os
from app.models.auth.user_account import UserAccount


class UserManager:
    def __init__(self):
        self.user_data = {}
        self._load_accounts()

    def _load_accounts(self):
        accounts_file = os.path.join(UserAccount.ACCOUNTS_DIR, "users.json")
        try:
            if os.path.exists(accounts_file):
                with open(accounts_file, 'r') as f:
                    self.user_data = json.load(f)
        except Exception as e:
            print(f"Błąd ładowania kont: {e}")
            self.user_data = {}

    def load_user(self, username):
        if username not in self.user_data:
            raise ValueError("Użytkownik nie istnieje")

        user = UserAccount(username)

        if not hasattr(user, '_unlocked_achievements'):
            user._unlocked_achievements = set()

        return user

    def register_user(self, username, password):
        if username in self.user_data:
            raise ValueError("Użytkownik już istnieje")

        user = UserAccount(username)
        user.save_progress()

        salt = os.urandom(16).hex()
        hashed_password = UserAccount._hash_password(password, salt)

        self.user_data[username] = {
            'salt': salt,
            'hashed_password': hashed_password,
            'created_at': datetime.now().isoformat()
        }
        self._save_accounts()

        return user

    def _save_accounts(self):
        accounts_file = os.path.join(UserAccount.ACCOUNTS_DIR, "users.json")
        try:
            with open(accounts_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Błąd zapisu kont: {e}")
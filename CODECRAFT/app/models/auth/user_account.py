import json
import os
from hashlib import sha256
from pathlib import Path

import datetime


class UserAccount:
    ACCOUNTS_DIR = "data/accounts"
    PROGRESS_DIR = "data/progress"
    TASKS_PER_MODULE = 16

    def __init__(self, username):
        self.username = username
        self.progress_file = f"{self.PROGRESS_DIR}/{username}_progress.json"
        self.completed_tasks = set()
        self.module_scores = {}  # {lesson_index: liczba_ukończonych_zadań}
        self.first_completions = set()  # Śledzi pierwsze ukończenie modułów
        self._ensure_dirs_exist()
        self.load_progress()

    def _ensure_dirs_exist(self):
        """Tworzy wymagane katalogi jeśli nie istnieją"""
        Path(self.ACCOUNTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.PROGRESS_DIR).mkdir(parents=True, exist_ok=True)

    def save_progress(self):
        """Zapisuje postęp w sposób gwarantujący trwałość danych"""
        try:
            # Tworzymy strukturę danych
            progress_data = {
                "version": 1,
                "completed_tasks": list(self.completed_tasks),
                "module_scores": self.module_scores,
                "timestamp": datetime.datetime.now().isoformat()
            }

            # Zapis tymczasowy dla bezpieczeństwa
            temp_file = f"{self.progress_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(progress_data, f, indent=2)

            # Zamiana plików atomowo
            if os.path.exists(temp_file):
                if os.path.exists(self.progress_file):
                    os.remove(self.progress_file)
                os.rename(temp_file, self.progress_file)

        except Exception as e:
            print(f"Błąd zapisu postępu: {e}")
            raise

    def load_progress(self):
        """Ładuje postęp z silną walidacją danych"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)

                    # Walidacja struktury danych
                    if not isinstance(data, dict):
                        raise ValueError("Nieprawidłowy format danych")

                    self.completed_tasks = set(data.get("completed_tasks", []))
                    self.module_scores = data.get("module_scores", {})

                    # Wymuś zapis jeśli struktura była pusta
                    if not self.completed_tasks or not self.module_scores:
                        self.save_progress()

        except Exception as e:
            print(f"Błąd ładowania postępu: {e}")
            self.completed_tasks = set()
            self.module_scores = {}
            self.save_progress()  # Utwórz nowy plik z domyślnymi wartościami

    def complete_task(self, task_id, lesson_index):
        """Rozszerzona wersja z walidacją"""
        if not isinstance(task_id, str) or not isinstance(lesson_index, int):
            raise ValueError("Nieprawidłowe parametry zadania")

        self.completed_tasks.add(task_id)
        self.module_scores[str(lesson_index)] = self.module_scores.get(str(lesson_index), 0) + 1
        self.save_progress()  # Automatyczny zapis

    def is_module_complete(self, lesson_index, total_tasks=10):
        """
        Sprawdza czy moduł został ukończony
        :param lesson_index: indeks lekcji
        :param total_tasks: wymagana liczba zadań (domyślnie 10)
        :return: bool
        """
        return self.module_scores.get(str(lesson_index), 0) >= total_tasks

    def is_first_completion(self, lesson_index):
        """
        Sprawdza czy to pierwsze ukończenie modułu
        :param lesson_index: indeks lekcji
        :return: bool
        """
        return str(lesson_index) not in self.first_completions

    def get_module_progress(self, lesson_index):
        """
        Zwraca postęp w module
        :param lesson_index: indeks lekcji
        :return: tuple (completed, total)
        """
        return self.module_scores.get(str(lesson_index), 0), 10

    class UserAccount:
        TASKS_PER_MODULE = 16  # Nowa stała

        def is_module_fully_completed(self, lesson_index):
            """Sprawdza czy moduł jest w pełni ukończony (zadania + test)"""
            tasks_done = self.module_scores.get(str(lesson_index), 0) >= self.TASKS_PER_MODULE
            test_passed = f"final_test_{lesson_index}" in self.completed_tasks
            return tasks_done and test_passed

    @classmethod
    def register(cls, username, password):
        """Rejestracja nowego użytkownika"""
        accounts = cls._load_all_accounts()
        if username in accounts:
            raise ValueError("Użytkownik już istnieje")

        if len(username) < 3:
            raise ValueError("Nazwa użytkownika musi mieć minimum 3 znaki")

        if len(password) < 6:
            raise ValueError("Hasło musi mieć minimum 6 znaków")

        salt = os.urandom(16).hex()
        hashed_password = cls._hash_password(password, salt)

        accounts[username] = {
            "salt": salt,
            "hashed_password": hashed_password,
            "created_at": datetime.datetime.now().isoformat(),
            "last_login": None
        }

        cls._save_all_accounts(accounts)
        return cls(username)

    @classmethod
    def login(cls, username, password):
        """Logowanie istniejącego użytkownika"""
        accounts = cls._load_all_accounts()
        if username not in accounts:
            raise ValueError("Nieprawidłowy login lub hasło")

        salt = accounts[username]["salt"]
        hashed_password = cls._hash_password(password, salt)

        if hashed_password != accounts[username]["hashed_password"]:
            raise ValueError("Nieprawidłowy login lub hasło")

        # Aktualizacja daty logowania
        accounts[username]["last_login"] = datetime.datetime.now().isoformat()
        cls._save_all_accounts(accounts)

        return cls(username)

    @staticmethod
    def _hash_password(password, salt):
        """Generuje zahaszowane hasło z solą"""
        return sha256((password + salt).encode()).hexdigest()

    @classmethod
    def _load_all_accounts(cls):
        """Ładuje wszystkie konta z pliku"""
        accounts_file = f"{cls.ACCOUNTS_DIR}/users.json"
        try:
            with open(accounts_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @classmethod
    def _save_all_accounts(cls, accounts):
        """Zapisuje wszystkie konta do pliku"""
        accounts_file = f"{cls.ACCOUNTS_DIR}/users.json"
        with open(accounts_file, "w") as f:
            json.dump(accounts, f, indent=2)


# Dla zachowania wstecznej zgodności
UserProgress = UserAccount
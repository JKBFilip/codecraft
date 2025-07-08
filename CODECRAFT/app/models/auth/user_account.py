import json
import os
from hashlib import sha256
from pathlib import Path
import datetime


class UserAccount:
    ACCOUNTS_DIR = "data/accounts"
    PROGRESS_DIR = "data/progress"
    ACHIEVEMENTS_DIR = "data/achievements"
    TASKS_PER_MODULE = 16
    def __init__(self, username):
        self.username = username
        self.progress_file = f"{self.PROGRESS_DIR}/{username}_progress.json"
        self.completed_tasks = set()
        self.task_solutions = {}  # Dodaj tę linię - inicjalizacja słownika
        self.module_scores = {}
        self._ensure_dirs_exist()
        self.load_progress()  # Teraz ładujemy progres po inicjalizacji

    def _ensure_dirs_exist(self):  # Ujednolicona nazwa
        """Tworzy wymagane katalogi jeśli nie istnieją"""
        Path(self.ACCOUNTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.PROGRESS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.ACHIEVEMENTS_DIR).mkdir(parents=True, exist_ok=True)

    def save_task_answer(self, task_id: str, answer: str):
        """Zapisuje odpowiedź użytkownika dla danego zadania"""
        if not hasattr(self, 'task_answers'):
            self.task_answers = {}  # Inicjalizacja jeśli nie istnieje

        self.task_answers[task_id] = answer
        self.save_progress()  # Zapisz zmiany od razu

    def save_progress(self):
        """Rozszerzona metoda zapisu z uwzględnieniem odpowiedzi"""
        progress_data = {
            "version": 2,  # Wersja schematu danych
            "completed_tasks": list(self.completed_tasks),
            "module_scores": self.module_scores,
            "task_answers": getattr(self, 'task_answers', {}),  # Bezpieczne pobranie
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Zapisz przez plik tymczasowy (atomowość)
        temp_file = f"{self.progress_file}.tmp"
        try:
            with open(temp_file, 'w') as f:
                json.dump(progress_data, f, indent=2)

            if os.path.exists(temp_file):
                if os.path.exists(self.progress_file):
                    os.remove(self.progress_file)
                os.rename(temp_file, self.progress_file)
        except Exception as e:
            print(f"Krytyczny błąd zapisu: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def load_progress(self):
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)

                    # Dla wstecznej kompatybilności
                    self.task_solutions = data.get("task_solutions", {})  # Zawsze inicjalizuj
                    self.completed_tasks = set(data.get("completed_tasks", []))
                    self.module_scores = data.get("module_scores", {})

        except Exception as e:
            print(f"Błąd ładowania postępu: {e}")
            # Zawsze inicjalizuj puste wartości
            self.completed_tasks = set()
            self.task_solutions = {}
            self.module_scores = {}

    def complete_task(self, task_id, lesson_index):
        if task_id not in self.completed_tasks:  # Tylko jeśli zadanie nowe
            self.completed_tasks.add(task_id)
            self.module_scores[str(lesson_index)] = self.module_scores.get(str(lesson_index), 0) + 1
            self.save_progress()

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

        # Upewnij się że katalogi istnieją
        Path(cls.ACCOUNTS_DIR).mkdir(parents=True, exist_ok=True)

        # Reszta metody pozostaje bez zmian
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
        accounts_file = f"{cls.ACCOUNTS_DIR}/users.json"  # Teraz używa stałej klasy
        try:
            with open(accounts_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @classmethod
    def _save_all_accounts(cls, accounts):
        """Zapisuje wszystkie konta do pliku"""
        accounts_file = f"{cls.ACCOUNTS_DIR}/users.json"  # Używa stałej klasy
        with open(accounts_file, "w") as f:
            json.dump(accounts, f, indent=2)


# Dla zachowania wstecznej zgodności
UserProgress = UserAccount
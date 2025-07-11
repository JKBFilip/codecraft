import json
import os
from hashlib import sha256
from pathlib import Path
from datetime import datetime
from app.features.achievements import AchievementSystem


class UserAccount:
    ACCOUNTS_DIR = "data/accounts"
    PROGRESS_DIR = "data/progress"
    ACHIEVEMENTS_DIR = "data/achievements"
    TASKS_PER_MODULE = 16

    def __init__(self, username):
        self.username = username
        self.progress_file = f"{self.PROGRESS_DIR}/{username}_progress.json"
        self.achievements_file = f"{self.ACHIEVEMENTS_DIR}/{username}_achievements.json"

        # Inicjalizacja danych
        self.completed_tasks = set()
        self.task_solutions = {}
        self.module_scores = {}
        self.test_history = []
        self.experience = 0
        self._unlocked_achievements = set()  # Prywatny zbiór

        self._ensure_dirs_exist()
        self._load_progress()
        self._load_achievements()

        # System osiągnięć inicjalizowany PO załadowaniu danych
        self.achievement_system = AchievementSystem(self)

    @property
    def unlocked_achievements(self):
        return self._unlocked_achievements.copy()

    def _ensure_dirs_exist(self):
        Path(self.ACCOUNTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.PROGRESS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.ACHIEVEMENTS_DIR).mkdir(parents=True, exist_ok=True)

    def load_all_data(self):
        """Ładuje wszystkie dane użytkownika"""
        self._load_progress()
        self._load_achievements()

    def _load_progress(self):
        """Ładuje postęp użytkownika"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    self.completed_tasks = set(data.get("completed_tasks", []))
                    self.module_scores = data.get("module_scores", {})
                    self.task_solutions = data.get("task_solutions", {})
                    self.test_history = data.get("test_history", [])
                    self.experience = data.get("experience", 0)
        except Exception as e:
            print(f"Błąd ładowania postępu: {e}")

    # W klasie UserAccount zmodyfikuj metodę _load_achievements:
    def _load_achievements(self):
        """Ładuje osiągnięcia z pliku specyficznego dla użytkownika"""
        try:
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r') as f:
                    data = json.load(f)
                    # Upewnij się, że unlocked jest listą/setem
                    unlocked = data.get("unlocked", [])
                    if isinstance(unlocked, list):
                        self._unlocked_achievements = set(unlocked)
                    else:
                        self._unlocked_achievements = set()
            else:
                self._unlocked_achievements = set()

            # Upewnij się, że achievement_system jest zainicjalizowany
            if not hasattr(self, 'achievement_system') or not self.achievement_system:
                self.achievement_system = AchievementSystem(self)
        except Exception as e:
            print(f"Błąd ładowania osiągnięć: {e}")
            self._unlocked_achievements = set()

    def save_progress(self):
        """Zapisuje postęp użytkownika"""
        progress_data = {
            "completed_tasks": list(self.completed_tasks),
            "module_scores": self.module_scores,
            "task_solutions": self.task_solutions,
            "test_history": self.test_history,
            "experience": self.experience,
            "timestamp": datetime.now().isoformat()
        }
        self._safe_save(self.progress_file, progress_data)

    def save_achievements(self):
        """Zapisuje osiągnięcia do pliku użytkownika"""
        data = {
            "username": self.username,
            "achievements": list(self._unlocked_achievements),
            "timestamp": datetime.now().isoformat()
        }
        self._safe_save(self.achievements_file, data)

    def _safe_save(self, file_path, data):
        """Bezpieczny zapis z użyciem pliku tymczasowego"""
        temp_file = f"{file_path}.tmp"
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)

            if os.path.exists(temp_file):
                if os.path.exists(file_path):
                    os.remove(file_path)
                os.rename(temp_file, file_path)
        except Exception as e:
            print(f"Błąd zapisu do {file_path}: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def save_task_answer(self, task_id, answer):
        """Zapisuje odpowiedź użytkownika do zadania"""
        self.task_solutions[task_id] = {
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
        self.save_progress()

    def complete_task(self, task_id, lesson_index):
        """Zaznacza zadanie jako ukończone"""
        self.completed_tasks.add(task_id)
        lesson_key = str(lesson_index)
        count = sum(1 for t in self.completed_tasks if t.startswith(f"lesson{lesson_key}-q"))
        self.module_scores[lesson_key] = count
        self.save_progress()

    def add_experience(self, points):
        """Dodaje punkty doświadczenia"""
        self.experience += points
        self.save_progress()

    def add_test_result(self, module_index, score, perfect_score=False, time_taken=None):
        """Dodaje wynik testu"""
        self.test_history.append({
            "module": int(module_index),
            "score": float(score),
            "perfect": bool(perfect_score),
            "time_taken": float(time_taken) if time_taken is not None else 0.0,
            "completion_date": datetime.now().isoformat()
        })
        self.save_progress()

    def check_achievements(self):
        """Sprawdza i odblokowuje nowe osiągnięcia"""
        if hasattr(self, 'achievement_system') and self.achievement_system:
            new_achievements = self.achievement_system.check_for_new_achievements()
            if new_achievements:
                self.save_achievements()
            return new_achievements
        return []

    def is_module_fully_completed(self, lesson_index):
        """Sprawdza czy moduł jest w pełni ukończony (zadania + test)"""
        # Sprawdzamy czy liczba zadań jest równa wymaganej
        tasks_done = self.module_scores.get(str(lesson_index), 0) >= self.TASKS_PER_MODULE

        # Sprawdzamy czy test został zaliczony na 100%
        test_passed = any(
            t.get('module') == lesson_index and float(t.get('score', 0)) >= 100.0
            for t in self.test_history
        )

        return tasks_done and test_passed

    def get_module_completion(self, module_index):
        """Zwraca szczegółowy status ukończenia modułu"""
        return {
            'tasks_completed': self.module_scores.get(str(module_index), 0),
            'tasks_required': self.TASKS_PER_MODULE,
            'test_passed': any(t.get('module') == module_index for t in self.test_history),
            'perfect_test': any(
                t.get('module') == module_index and float(t.get('score', 0)) >= 100.0
                for t in self.test_history
            )
        }
    @classmethod
    def register(cls, username, password):
        accounts = cls._load_all_accounts()
        if username in accounts:
            raise ValueError("Użytkownik już istnieje")

        Path(cls.ACCOUNTS_DIR).mkdir(parents=True, exist_ok=True)
        salt = os.urandom(16).hex()
        hashed_password = cls._hash_password(password, salt)

        accounts[username] = {
            "salt": salt,
            "hashed_password": hashed_password,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }

        cls._save_all_accounts(accounts)
        return cls(username)

    @classmethod
    def login(cls, username, password):
        accounts = cls._load_all_accounts()
        if username not in accounts:
            raise ValueError("Nieprawidłowy login lub hasło")

        salt = accounts[username]["salt"]
        hashed_password = cls._hash_password(password, salt)

        if hashed_password != accounts[username]["hashed_password"]:
            raise ValueError("Nieprawidłowy login lub hasło")

        accounts[username]["last_login"] = datetime.now().isoformat()
        cls._save_all_accounts(accounts)
        return cls(username)

    @staticmethod
    def _hash_password(password, salt):
        return sha256((password + salt).encode()).hexdigest()

    @classmethod
    def _load_all_accounts(cls):
        accounts_file = f"{cls.ACCOUNTS_DIR}/users.json"
        try:
            with open(accounts_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @classmethod
    def _save_all_accounts(cls, accounts):
        accounts_file = f"{cls.ACCOUNTS_DIR}/users.json"
        with open(accounts_file, "w") as f:
            json.dump(accounts, f, indent=2)

    @classmethod
    def reset_password(cls, username, new_password):
        accounts = cls._load_all_accounts()

        if username not in accounts:
            raise ValueError("Użytkownik nie istnieje")

        # Generujemy nową sól i hasz
        salt = os.urandom(16).hex()
        hashed_password = cls._hash_password(new_password, salt)

        # Aktualizujemy dane
        accounts[username]["salt"] = salt
        accounts[username]["hashed_password"] = hashed_password

        # Zapisujemy
        cls._save_all_accounts(accounts)

UserProgress = UserAccount
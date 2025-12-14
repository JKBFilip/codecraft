import json
import os
from hashlib import sha256
from pathlib import Path
from datetime import datetime
from app.features.achievements import AchievementSystem

# Progi XP
XP_PER_LEVEL = [100, 250, 500, 1000, 2000, 3500, 5000, 7000, 9000, 15000, 20000]


class UserAccount:
    ACCOUNTS_DIR = "data/accounts"
    PROGRESS_DIR = "data/progress"
    ACHIEVEMENTS_DIR = "data/achievements"
    TASKS_PER_MODULE = 16

    def __init__(self, username):
        self.username = username
        self.progress_file = f"{self.PROGRESS_DIR}/{username}_progress.json"
        self.achievements_file = f"{self.ACHIEVEMENTS_DIR}/{username}_achievements.json"

        self.completed_tasks = set()
        self.task_solutions = {}
        self.module_scores = {}
        self.test_history = []
        self.experience = 0
        self._unlocked_achievements = set()
        self.redeemed_codes = set()

        self._ensure_dirs_exist()
        self._load_progress()
        self._load_achievements()
        self.achievement_system = AchievementSystem(self)

    @property
    def level(self) -> int:
        for i, xp_needed in enumerate(XP_PER_LEVEL, 1):
            if self.experience < xp_needed:
                return i
        return len(XP_PER_LEVEL) + 1

    def get_xp_for_next_level(self) -> int:
        current_level_index = self.level - 1
        if current_level_index < len(XP_PER_LEVEL):
            return XP_PER_LEVEL[current_level_index]
        else:
            return XP_PER_LEVEL[-1]

    @property
    def unlocked_achievements(self):
        return self._unlocked_achievements.copy()

    def _ensure_dirs_exist(self):
        Path(self.ACCOUNTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.PROGRESS_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.ACHIEVEMENTS_DIR).mkdir(parents=True, exist_ok=True)

    def load_all_data(self):
        self._load_progress()
        self._load_achievements()

    def _load_progress(self):
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    self.completed_tasks = set(data.get("completed_tasks", []))
                    self.module_scores = data.get("module_scores", {})
                    self.task_solutions = data.get("task_solutions", {})
                    self.test_history = data.get("test_history", [])
                    self.experience = data.get("experience", 0)
                    self.redeemed_codes = set(data.get("redeemed_codes", []))
        except Exception as e:
            print(f"Błąd ładowania postępu: {e}")

    def _load_achievements(self):
        self._unlocked_achievements = set()
        try:
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    unlocked_ids = data.get("achievements", data.get("unlocked", []))

                    if isinstance(unlocked_ids, list):
                        self._unlocked_achievements = set(unlocked_ids)
                    else:
                        print(f"OSTRZEŻENIE: Dane osiągnięć nie są listą w pliku {self.achievements_file}.")
        except (json.JSONDecodeError, Exception) as e:
            print(f"BŁĄD KRYTYCZNY: Nie udało się wczytać pliku osiągnięć ({self.achievements_file}): {e}.")
            self._unlocked_achievements = set()

    def save_progress(self):
        progress_data = {
            "completed_tasks": list(self.completed_tasks),
            "module_scores": self.module_scores,
            "task_solutions": self.task_solutions,
            "test_history": self.test_history,
            "experience": self.experience,
            "timestamp": datetime.now().isoformat(),
            "redeemed_codes": list(self.redeemed_codes)
        }
        self._safe_save(self.progress_file, progress_data)

    def save_achievements(self):
        data = {
            "username": self.username,
            "achievements": list(self._unlocked_achievements),
            "timestamp": datetime.now().isoformat()
        }
        self._safe_save(self.achievements_file, data)

    def _safe_save(self, file_path, data):
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
        self.task_solutions[task_id] = {
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
        self.save_progress()

    def complete_task(self, task_id, lesson_index):
        self.completed_tasks.add(task_id)
        lesson_key = str(lesson_index)
        count = sum(1 for t in self.completed_tasks if t.startswith(f"lesson{lesson_key}-q"))
        self.module_scores[lesson_key] = count
        self.check_achievements()
        self.save_progress()

    def add_experience(self, points):
        self.experience += points
        self.save_progress()

    def add_test_result(self, module_index, score, perfect_score=False, time_taken=None):
        test_data = {
            "module": int(module_index),
            "score": float(score),
            "perfect": bool(perfect_score),
            "time_taken": float(time_taken) if time_taken is not None else 0.0,
            "completion_date": datetime.now().isoformat(),
            "is_final_exam": (module_index == 0)
        }
        self.test_history.append(test_data)
        self.check_achievements()
        self.save_progress()

    def check_achievements(self):
        if hasattr(self, 'achievement_system') and self.achievement_system:
            new_achievements = self.achievement_system.check_for_new_achievements()
            if new_achievements:
                self.save_achievements()
            return new_achievements
        return []

    def is_module_fully_completed(self, lesson_index):
        tasks_done = self.module_scores.get(str(lesson_index), 0) >= self.TASKS_PER_MODULE
        test_passed = any(
            t.get('module') == lesson_index and float(t.get('score', 0)) >= 80.0
            for t in self.test_history
        )
        return tasks_done and test_passed

    def get_module_completion(self, module_index):
        return {
            'tasks_completed': self.module_scores.get(str(module_index), 0),
            'tasks_required': self.TASKS_PER_MODULE,
            'test_passed': any(t.get('module') == module_index for t in self.test_history),
            'perfect_test': any(
                t.get('module') == module_index and float(t.get('score', 0)) >= 100.0
                for t in self.test_history
            )
        }

    def are_all_modules_completed(self):
        for module in range(1, 6):
            if not self.is_module_fully_completed(module):
                return False
        return True

    def has_passed_final_exam(self):
        return any(
            t.get('is_final_exam', False) and float(t.get('score', 0)) >= 80.0
            for t in self.test_history)

    def get_final_exam_result(self):
        """
        Zwraca NAJLEPSZY ZDANY wynik egzaminu końcowego.
        Jeśli brak zdanych, zwraca najlepszy niezdany (choć to rzadkie w tym flow).
        """
        # Filtrujemy tylko egzaminy końcowe (module 0 lub is_final_exam)
        final_exams = [t for t in self.test_history if t.get('is_final_exam', False) or t.get('module') == 0]

        if not final_exams:
            return None

        # Szukamy zdanych egzaminów (>= 80%)
        passed_exams = [t for t in final_exams if float(t.get('score', 0)) >= 80.0]

        # Jeśli są zdane, bierzemy ten z najwyższym wynikiem
        if passed_exams:
            # Sortujemy: Najpierw po wyniku (malejąco), potem po dacie (najnowszy)
            best_exam = \
            sorted(passed_exams, key=lambda x: (x.get('score', 0), x.get('completion_date', '')), reverse=True)[0]

            return {
                'score': best_exam.get('score', 0),
                'date': best_exam.get('completion_date', ''),
                'time_taken': best_exam.get('time_taken', 0)
            }

        # Jeśli nie ma zdanych (ale funkcja jest wywoływana?), bierzemy najlepszy wynik
        best_attempt = sorted(final_exams, key=lambda x: x.get('score', 0), reverse=True)[0]
        return {
            'score': best_attempt.get('score', 0),
            'date': best_attempt.get('completion_date', ''),
            'time_taken': best_attempt.get('time_taken', 0)
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

        salt = os.urandom(16).hex()
        hashed_password = cls._hash_password(new_password, salt)

        accounts[username]["salt"] = salt
        accounts[username]["hashed_password"] = hashed_password
        cls._save_all_accounts(accounts)

    def apply_cheat_code(self, code):
        if code == "MAX_MODULES":
            self.unlock_all_modules()
            return "✅ Odblokowano wszystkie moduły i testy!"

        elif code == "MAX_ACHIEVEMENTS":
            self.unlock_all_achievements()
            return "🏆 Odblokowano wszystkie osiągnięcia!"

        if code in self.redeemed_codes:
            return "❌ Ten kod został już wykorzystany."

        if code == "XP_BOOST_100":
            self.add_experience(100)
            self.redeemed_codes.add(code)
            self.save_progress()
            return "✅ Dodano 100 XP! Kod został zapisany."

        return "❌ Nieprawidłowy kod."

    def unlock_all_modules(self):
        print("CHEAT: Odblokowywanie wszystkich modułów...")

        for i in range(1, 6):
            self.module_scores[str(i)] = self.TASKS_PER_MODULE

        for i in range(1, 6):
            if not any(t.get('module') == i and t.get('score', 0) >= 80 for t in self.test_history):
                test_data = {
                    "module": i,
                    "score": 100.0,
                    "perfect": True,
                    "time_taken": 1.0,
                    "completion_date": datetime.now().isoformat(),
                    "is_final_exam": False
                }
                self.test_history.append(test_data)

        for i in range(1, 6):
            task_id = f"final_test_{i}"
            if task_id not in self.completed_tasks:
                self.completed_tasks.add(task_id)

        self.save_progress()

    def unlock_all_achievements(self):
        print("CHEAT: Odblokowywanie wszystkich osiągnięć...")

        all_achievements = self.achievement_system.get_all_achievements()

        for ach in all_achievements:
            self._unlocked_achievements.add(ach.id)

        self.save_achievements()


UserProgress = UserAccount

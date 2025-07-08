import json
from pathlib import Path


class AchievementSystem:
    ACHIEVEMENTS_DIR = "data/achievements"

    def __init__(self, username):
        self.username = username
        self.achievements_file = f"{self.ACHIEVEMENTS_DIR}/{username}_achievements.json"
        self._ensure_dir_exists()
        self.achievements = self._load_achievements()

    def _ensure_dir_exists(self):
        Path(self.ACHIEVEMENTS_DIR).mkdir(parents=True, exist_ok=True)

    def unlock(self, achievement_id):
        if achievement_id not in self.achievements:
            self.achievements.append(achievement_id)
            self._save_achievements()
            return True
        return False

    def _save_achievements(self):
        with open(self.achievements_file, "w") as f:
            json.dump(self.achievements, f, indent=2)

    def _load_achievements(self):
        try:
            with open(self.achievements_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
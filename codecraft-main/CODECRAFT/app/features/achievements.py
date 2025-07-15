from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class Achievement:
    id: str
    name: str
    description: str
    icon: str
    points: int
    hidden: bool = False
    _owner_username: str = None

    def is_unlocked_for(self, user_account) -> bool:
        return self._owner_username == user_account.username

    def check_condition(self, user_account) -> bool:
        raise NotImplementedError()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'points': self.points,
            'hidden': self.hidden,
            'owner': self._owner_username
        }


class UserSpecificAchievement(Achievement):
    def __init__(self, user_account, achievement_id: str, name: str, description: str,
                 condition_checker: callable, icon: str = "🏆", points: int = 10, hidden: bool = False):
        super().__init__(
            id=f"{user_account.username}_{achievement_id}",
            name=name,
            description=description,
            icon=icon,
            points=points,
            hidden=hidden
        )
        self._owner_username = user_account.username
        self._condition_checker = condition_checker

    def check_condition(self, user_account) -> bool:
        return (self.is_unlocked_for(user_account) and
                self._condition_checker(user_account))


class AchievementSystem:
    def __init__(self, user_account):
        self.user_account = user_account
        self._achievements = self._initialize_user_specific_achievements()

    def _initialize_user_specific_achievements(self) -> List[UserSpecificAchievement]:
        return [
            UserSpecificAchievement(
                self.user_account,
                "first_task",
                "Pierwszy krok!",
                "Rozwiąż pierwsze zadanie.",
                lambda u: len(u.completed_tasks) >= 1,
                icon="👣",
                points=5
            ),
            UserSpecificAchievement(
                self.user_account,
                "first_module",
                "Moduł zaliczony!",
                "Ukończ wszystkie zadania w jednym module.",
                lambda u: any(v >= u.TASKS_PER_MODULE for v in u.module_scores.values()),
                icon="🎯",
                points=20
            ),
            UserSpecificAchievement(
                self.user_account,
                "module_1_master",
                "Mistrz Podstaw",
                "Ukończ wszystkie zadania w module 1.",
                lambda u: u.module_scores.get("1", 0) >= u.TASKS_PER_MODULE,
                icon="🐣",
                points=15,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "module_2_master",
                "Mistrz Warunków",
                "Ukończ wszystkie zadania w module 2.",
                lambda u: u.module_scores.get("2", 0) >= u.TASKS_PER_MODULE,
                icon="🎲",
                points=20,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "module_3_master",
                "Mistrz Pętli",
                "Ukończ wszystkie zadania w module 3.",
                lambda u: u.module_scores.get("3", 0) >= u.TASKS_PER_MODULE,
                icon="🌀",
                points=25,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "module_4_master",
                "Mistrz Funkcji",
                "Ukończ wszystkie zadania w module 4.",
                lambda u: u.module_scores.get("4", 0) >= u.TASKS_PER_MODULE,
                icon="🧩",
                points=30,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "module_5_master",
                "Mistrz List",
                "Ukończ wszystkie zadania w module 5.",
                lambda u: u.module_scores.get("5", 0) >= u.TASKS_PER_MODULE,
                icon="🗃️",
                points=35,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "perfectionist",
                "Perfekcjonista",
                "Zalicz jakikolwiek test na 100%.",
                lambda u: any(t.get('score', 0) == 100 for t in u.test_history),
                icon="💯",
                points=50
            ),
            UserSpecificAchievement(
                self.user_account,
                "ultimate_perfectionist",
                "Ultra Perfekcjonista",
                "Zalicz wszystkie testy modułów na 100%.",
                lambda u: all(
                    any(t.get('module') == mod and t.get('score', 0) == 100
                        for t in u.test_history)
                    for mod in range(1, 6)
                ),
                icon="🏆",
                points=100,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "speedrunner_3min",
                "Speedrunner (amator)",
                "Ukończ jakikolwiek test w czasie poniżej 3 minut.",
                lambda u: any(t.get('time_taken', 0) < 180 for t in u.test_history),
                icon="⏱️",
                points=10,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "speedrunner_2min",
                "Speedrunner (pro)",
                "Ukończ jakikolwiek test w czasie poniżej 2 minut.",
                lambda u: any(t.get('time_taken', 0) < 120 for t in u.test_history),
                icon="⚡",
                points=25,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "early_bird",
                "Ranny ptaszek",
                "Zaloguj się przed godziną 8:00 rano.",
                lambda u: datetime.now().hour < 8,
                icon="🌅",
                points=15,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "night_owl",
                "Nocny marek",
                "Zaloguj się po godzinie 23:00.",
                lambda u: datetime.now().hour >= 23,
                icon="🌙",
                points=15,
                hidden=True
            ),
            UserSpecificAchievement(
                self.user_account,
                "final_exam",
                "Mistrz Programowania",
                "Zdałeś egzamin końcowy z wynikiem co najmniej 80%.",
                lambda u: any(
                    t.get('module') == 0 and float(t.get('score', 0)) >= 80.0
                    for t in u.test_history
                ),
                icon="🏅",
                points=150,
                hidden=False
            )
        ]

    def check_for_new_achievements(self) -> List[Achievement]:
        new_achievements = []
        for achievement in self._achievements:
            if (achievement.id not in self.user_account.unlocked_achievements and
                    achievement.check_condition(self.user_account)):
                self._unlock_achievement(achievement)
                new_achievements.append(achievement)
        return new_achievements

    def _unlock_achievement(self, achievement: Achievement):
        if achievement.id not in self.user_account._unlocked_achievements:
            self.user_account._unlocked_achievements.add(achievement.id)
            self.user_account.add_experience(achievement.points)
            self.user_account.save_achievements()
            self.user_account.save_progress()
            print(f"Odblokowano osiągnięcie: {achievement.name} (ID: {achievement.id})")

    def get_all_achievements(self) -> List[Achievement]:
        return self._achievements

    def get_unlocked_achievements(self) -> List[Achievement]:
        return [
            a for a in self._achievements
            if a.id in self.user_account.unlocked_achievements
        ]

    def save_to_file(self):
        data = {
            'unlocked': list(self.user_account.unlocked_achievements),
            'achievements': [a.to_dict() for a in self._achievements]
        }
        filename = f"data/achievements/{self.user_account.username}_achievements.json"
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_file(self):
        filename = f"data/achievements/{self.user_account.username}_achievements.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.user_account._unlocked_achievements = set(data.get('unlocked', []))
        except FileNotFoundError:
            self.user_account._unlocked_achievements = set()
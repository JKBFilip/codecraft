from datetime import datetime
from typing import List, Dict, Any, Callable
from dataclasses import dataclass, field

# Forward declaration to help with type hinting without causing circular imports
# This tells Python "trust me, a class named UserAccount exists somewhere"
class UserAccount:
    pass

@dataclass
class Achievement:
    """
    Uproszczona, uniwersalna klasa reprezentująca jedno osiągnięcie.
    Jest to szablon, który nie zależy od konkretnego użytkownika.
    """
    id: str  # Unikalny identyfikator, np. "first_task"
    name: str
    description: str
    icon: str
    points: int
    condition: Callable[['UserAccount'], bool]  # Logika sprawdzająca warunek
    hidden: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Zwraca słownikową reprezentację osiągnięcia."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'points': self.points,
            'hidden': self.hidden,
        }

class AchievementSystem:
    """
    Zarządza logiką osiągnięć w grze.
    Sprawdza warunki i odblokowuje nagrody dla danego użytkownika.
    """
    def __init__(self, user_account: 'UserAccount'):
        # Przechowujemy referencję do konta użytkownika, aby móc sprawdzać jego postępy
        self.user_account = user_account
        # Inicjalizujemy listę wszystkich możliwych osiągnięć w grze
        self._achievements = self._initialize_achievements()

    def _initialize_achievements(self) -> List[Achievement]:
        """Tworzy i zwraca PEŁNĄ listę wszystkich definicji osiągnięć."""
        return [
            Achievement("first_task", "Pierwszy krok!", "Rozwiąż pierwsze zadanie.", "👣", 5,
                        lambda u: len(u.completed_tasks) >= 1),
            Achievement("first_module", "Moduł zaliczony!", "Ukończ wszystkie zadania w jednym module.", "🎯", 20,
                        lambda u: any(v >= u.TASKS_PER_MODULE for v in u.module_scores.values())),
            Achievement("module_1_master", "Mistrz Podstaw", "Ukończ wszystkie zadania w module 1.", "🐣", 15,
                        lambda u: u.module_scores.get("1", 0) >= u.TASKS_PER_MODULE, hidden=True),
            Achievement("module_2_master", "Mistrz Warunków", "Ukończ wszystkie zadania w module 2.", "🎲", 20,
                        lambda u: u.module_scores.get("2", 0) >= u.TASKS_PER_MODULE, hidden=True),
            Achievement("module_3_master", "Mistrz Pętli", "Ukończ wszystkie zadania w module 3.", "🌀", 25,
                        lambda u: u.module_scores.get("3", 0) >= u.TASKS_PER_MODULE, hidden=True),
            Achievement("module_4_master", "Mistrz Funkcji", "Ukończ wszystkie zadania w module 4.", "🧩", 30,
                        lambda u: u.module_scores.get("4", 0) >= u.TASKS_PER_MODULE, hidden=True),
            Achievement("module_5_master", "Mistrz List", "Ukończ wszystkie zadania w module 5.", "🗃️", 35,
                        lambda u: u.module_scores.get("5", 0) >= u.TASKS_PER_MODULE, hidden=True),
            Achievement("perfectionist", "Perfekcjonista", "Zalicz jakikolwiek test na 100%.", "💯", 50,
                        lambda u: any(t.get('score', 0) == 100 for t in u.test_history)),
            Achievement("ultimate_perfectionist", "Ultra Perfekcjonista", "Zalicz wszystkie testy modułów na 100%.",
                        "🏆", 100,
                        lambda u: all(
                            any(t.get('module') == mod and t.get('score', 0) == 100 for t in u.test_history) for mod in
                            range(1, 6)), hidden=True),
            Achievement("speedrunner_3min", "Speedrunner (amator)", "Ukończ jakikolwiek test w czasie poniżej 3 minut.",
                        "⏱️", 10,
                        lambda u: any(
                            t.get('time_taken', 0) > 0 and t.get('time_taken', 999) < 180 for t in u.test_history),
                        hidden=True),
            Achievement("speedrunner_2min", "Speedrunner (pro)", "Ukończ jakikolwiek test w czasie poniżej 2 minut.",
                        "⚡", 25,
                        lambda u: any(
                            t.get('time_taken', 0) > 0 and t.get('time_taken', 999) < 120 for t in u.test_history),
                        hidden=True),
            Achievement("early_bird", "Ranny ptaszek", "Zaloguj się przed godziną 8:00 rano.", "🌅", 15,
                        lambda u: datetime.now().hour < 8, hidden=True),
            Achievement("night_owl", "Nocny marek", "Zaloguj się po godzinie 23:00.", "🌙", 15,
                        lambda u: datetime.now().hour >= 23, hidden=True),
            Achievement("final_exam", "Mistrz Programowania", "Zdałeś egzamin końcowy z wynikiem co najmniej 80%.", "🏅",
                        150,
                        lambda u: any(
                            t.get('module') == 0 and float(t.get('score', 0)) >= 80.0 for t in u.test_history))
        ]

    def check_for_new_achievements(self) -> List[Achievement]:
        """Sprawdza wszystkie nieodblokowane osiągnięcia i przyznaje je, jeśli warunki są spełnione."""
        newly_unlocked = []
        for achievement in self._achievements:
            # Sprawdzamy tylko te osiągnięcia, których użytkownik JESZCZE NIE MA
            if achievement.id not in self.user_account.unlocked_achievements:
                # Jeśli warunek jest spełniony...
                if achievement.condition(self.user_account):
                    # ...odblokowujemy je
                    self._unlock_achievement(achievement)
                    newly_unlocked.append(achievement)
        return newly_unlocked

    def _unlock_achievement(self, achievement: Achievement):
        """
        Kluczowa metoda, która przyznaje nagrodę.
        Ma solidne zabezpieczenie, aby uniknąć wielokrotnego przyznawania punktów.
        """
        # OSTATECZNE ZABEZPIECZENIE: Sprawdzamy ponownie, czy na pewno nie mamy tego osiągnięcia
        if achievement.id not in self.user_account.unlocked_achievements:
            self.user_account._unlocked_achievements.add(achievement.id)
            self.user_account.add_experience(achievement.points)

            # Klasa UserAccount jest odpowiedzialna za zapisywanie swoich danych,
            # więc wołamy jej metody.
            self.user_account.save_achievements()
            # Metoda add_experience już powinna zapisywać postęp, ale dla pewności
            # można to wywołać także tutaj.
            self.user_account.save_progress()

            print(f"✅ Odblokowano NOWE osiągnięcie: {achievement.name}")

    def get_all_achievements(self) -> List[Achievement]:
        """Zwraca listę wszystkich możliwych osiągnięć w grze."""
        return self._achievements

    def get_unlocked_achievements(self) -> List[Achievement]:
        """Zwraca listę osiągnięć, które dany użytkownik już odblokował."""
        return [
            ach for ach in self._achievements
            if ach.id in self.user_account.unlocked_achievements
        ]
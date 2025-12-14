import pytest
import os
from app.models.auth.user_account import UserAccount

# sprawdzamy czy aplikacja przezyje jak plik postepu bedzie smieciem
def test_corrupted_progress_file(setup_fake_dirs):
    os.makedirs(UserAccount.PROGRESS_DIR, exist_ok=True)
    sciezka = os.path.join(UserAccount.PROGRESS_DIR, "zepsuty_user_progress.json")

    with open(sciezka, "w") as f:
        f.write("{to nie jest json")

    uzytkownik = UserAccount("zepsuty_user")
    # Powinien wczytac domyslne wartosci zamiast sie wywalic
    assert uzytkownik.experience == 0
    assert len(uzytkownik.completed_tasks) == 0

# sprawdzamy czy aplikacja przezyje jak plik osiagniec bedzie smieciem
def test_corrupted_achievements_file(setup_fake_dirs):
    os.makedirs(UserAccount.ACHIEVEMENTS_DIR, exist_ok=True)
    sciezka = os.path.join(UserAccount.ACHIEVEMENTS_DIR, "zepsuty_user_achievements.json")

    with open(sciezka, "w") as f:
        f.write("Not JSON content")

    uzytkownik = UserAccount("zepsuty_user")
    # Powinien zresetowac osiagniecia
    assert len(uzytkownik.unlocked_achievements) == 0

# symulujemy brak miejsca na dysku przy zapisie
def test_save_permission_error(setup_fake_dirs, monkeypatch):
    uzytkownik = UserAccount.register("pechowiec_io", "pass")

    # Definiujemy funkcję, która zawsze wywala błąd
    def zepsuty_zapis(*args, **kwargs):
        raise OSError("Dysk pełny")

    # Wskazujemy dokladnie modul, w ktorym chcemy podmienic json.dump
    monkeypatch.setattr("app.models.auth.user_account.json.dump", zepsuty_zapis)

    # Teraz wywołujemy zapis.
    # Błąd powinien zostać wyłapany przez blok try-except w metodzie _safe_save
    try:
        uzytkownik.save_progress()
    except OSError:
        pytest.fail("Błąd OSError wydostał się na zewnątrz! Powinien być obsłużony w klasie.")
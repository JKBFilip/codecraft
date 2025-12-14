import pytest
import os
import json
from app.models.auth.user_manager import UserManager
from app.models.auth.user_account import UserAccount


# sprawdzamy czy manager w ogole startuje
def test_user_manager_init(setup_fake_dirs):
    zarzadca = UserManager()
    assert zarzadca.user_data == {}


# testujemy rejestracje przez managera
def test_register_user_via_manager(setup_fake_dirs):
    zarzadca = UserManager()

    nowy_user = zarzadca.register_user("szef_rejestracji", "haslo123")
    assert nowy_user.username == "szef_rejestracji"
    assert "szef_rejestracji" in zarzadca.user_data

    sciezka_kont = os.path.join(UserAccount.ACCOUNTS_DIR, "users.json")
    assert os.path.exists(sciezka_kont)

    with open(sciezka_kont, 'r') as plik:
        dane = json.load(plik)
        assert "szef_rejestracji" in dane

    with pytest.raises(ValueError):
        zarzadca.register_user("szef_rejestracji", "haslo123")


# sprawdzamy czy da sie wczytac uzytkownika
def test_load_user_via_manager(setup_fake_dirs):
    zarzadca = UserManager()
    zarzadca.register_user("do_wczytania", "pass")

    zarzadca2 = UserManager()
    wczytany = zarzadca2.load_user("do_wczytania")

    assert wczytany.username == "do_wczytania"
    assert hasattr(wczytany, '_unlocked_achievements')

    with pytest.raises(ValueError):
        zarzadca2.load_user("duch")


# testujemy co sie stanie jak plik z kontami jest zepsuty
def test_corrupted_accounts_file(setup_fake_dirs):
    os.makedirs(UserAccount.ACCOUNTS_DIR, exist_ok=True)
    sciezka_kont = os.path.join(UserAccount.ACCOUNTS_DIR, "users.json")

    with open(sciezka_kont, 'w') as plik:
        plik.write("{to nie jest poprawny json")

    zarzadca = UserManager()
    assert zarzadca.user_data == {}
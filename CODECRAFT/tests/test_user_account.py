import pytest
from app.models.auth.user_account import UserAccount

# sprawdzamy czy rejestracja w ogole dziala
def test_registration(setup_fake_dirs):
    nowy_ziomek = UserAccount.register("tester_rejestracji", "haslo123")
    assert nowy_ziomek.username == "tester_rejestracji"
    assert nowy_ziomek.experience == 0

    with pytest.raises(ValueError):
        UserAccount.register("tester_rejestracji", "innehaslo")

# testujemy logowanie - dobre i zle hasla
def test_login(setup_fake_dirs):
    UserAccount.register("login_ziomek", "tajnehaslo")

    zalogowany = UserAccount.login("login_ziomek", "tajnehaslo")
    assert zalogowany is not None
    assert zalogowany.username == "login_ziomek"

    with pytest.raises(ValueError):
        UserAccount.login("login_ziomek", "zlehaslo")

    with pytest.raises(ValueError):
        UserAccount.login("duch", "haslo")

# sprawdzamy czy xp rosnie i lvl wskakuje
def test_progress_and_xp(setup_fake_dirs):
    gracz = UserAccount.register("xp_tester", "123456")

    assert gracz.level == 1
    gracz.add_experience(150)

    assert gracz.experience == 150
    assert gracz.level == 2
    assert gracz.get_xp_for_next_level() == 250

# testujemy czy kody dzialaja
def test_cheat_codes(setup_fake_dirs):
    cziter = UserAccount.register("cheater", "123456")

    msg = cziter.apply_cheat_code("MAX_MODULES")
    assert "Odblokowano" in msg
    assert cziter.module_scores["1"] == 16

    msg = cziter.apply_cheat_code("BLEDNY_KOD")
    assert "Nieprawidłowy" in msg

    msg = cziter.apply_cheat_code("XP_BOOST_100")
    assert "Dodano 100 XP" in msg
    assert cziter.experience == 100

    msg = cziter.apply_cheat_code("XP_BOOST_100")
    assert "wykorzystany" in msg
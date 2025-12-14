from app.features.achievements import AchievementSystem, Achievement
from app.models.auth.user_account import UserAccount

# sprawdzamy czy struktura osiagniecia sie trzyma kupy
def test_achievement_structure():
    badge = Achievement(
        id="test_id", name="Test", description="Desc",
        icon="X", points=10, condition=lambda u: True
    )
    info = badge.to_dict()
    assert info['id'] == "test_id"
    assert info['points'] == 10
    assert info['hidden'] is False

# testujemy czy system w ogole rozdaje nagrody
def test_check_new_achievements(setup_fake_dirs):
    gracz = UserAccount("ach_user")
    sys_nagrod = AchievementSystem(gracz)

    assert len(gracz.unlocked_achievements) == 0

    gracz.completed_tasks.add("lesson1-q1")

    nowe_achiv = sys_nagrod.check_for_new_achievements()

    assert len(nowe_achiv) >= 1
    assert "first_task" in gracz.unlocked_achievements
    assert gracz.experience >= 5

    nowe_achiv_2 = sys_nagrod.check_for_new_achievements()
    assert len(nowe_achiv_2) == 0

# sprawdzamy co tam juz odblokowane
def test_get_unlocked(setup_fake_dirs):
    gracz = UserAccount("filter_user")
    sys_nagrod = AchievementSystem(gracz)

    gracz._unlocked_achievements.add("first_task")

    zdobyte = sys_nagrod.get_unlocked_achievements()
    assert len(zdobyte) == 1
    assert zdobyte[0].id == "first_task"

    wszystkie = sys_nagrod.get_all_achievements()
    assert len(wszystkie) > 10
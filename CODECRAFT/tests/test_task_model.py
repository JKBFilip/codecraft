from app.models.task import Task

# sprawdzamy czy pojedyncze zadanie tworzy sie poprawnie
def test_task_initialization():
    zadanie = Task(
        lesson_index=1,
        question="Test pytania",
        solution="print('test')",
        type="code_input",
        options=["A", "B"],
        task_index=5
    )

    assert zadanie.lesson_index == 1
    assert zadanie.question == "Test pytania"
    assert zadanie.solution == "print('test')"
    assert zadanie.type == "code_input"
    assert zadanie.options == ["A", "B"]
    assert zadanie.task_index == 5
    assert zadanie.get_id() == "lesson1-q5"

# sprawdzamy czy zadania sa wczytywane z bazy
def test_load_all_tasks():
    wszystkie_zadania = Task.load_all()

    assert len(wszystkie_zadania) > 0
    assert isinstance(wszystkie_zadania[0], Task)

    pierwsze = wszystkie_zadania[0]
    assert pierwsze.lesson_index == 1
    assert "wiek" in pierwsze.question or "zmienną" in pierwsze.question
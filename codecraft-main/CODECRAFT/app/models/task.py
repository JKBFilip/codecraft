class Task:
    def __init__(self, lesson_index, question, solution, type="code_input", options=None, blocks=None, task_index=None):
        self.lesson_index = lesson_index
        self.question = question
        self.solution = solution
        self.type = type
        self.options = options or []
        self.blocks = blocks or []
        self.task_index = task_index

    def get_id(self):
        return f"lesson{self.lesson_index}-q{self.task_index}"

    @staticmethod
    def load_all():
        raw_data = [
            (1, "Przypisz wartość 10 do zmiennej 'wiek'", "wiek = 10", "code_input", None),
            (1, "Zadeklaruj zmienną 'imie' i przypisz do niej imie 'Olek'", 'imie = "Olek"', "code_input", None),
            (1, "Utwórz dwie zmienne a i b, przypisz im wartości 3 i 7", "a = 3\nb = 7", "code_input", None),
            (1, "Ustaw zmienną x na wartość 5, następnie zwiększ ją o 2.", "x = 5\nx = x + 2", "code_input", None),
            (1,
             "Co zostanie wypisane na ekranie?\n\na = 2\nb = a + 3\nprint(b)",
             "C",
             "multiple_choice",
             ["A: 2", "B: 3", "C: 5", "D: Błąd"]
             ),
            (1,
             "Jaką wartość ma zmienna x po tym kodzie?\n\nx = 4\nx = x * 2",
             "B",
             "multiple_choice",
             ["A: 4", "B: 8", "C: 6", "D: x"]
             ),
            (1,
             "Co wypisze ten kod?\n\ntekst = \"hej\"\nprint(tekst)",
             "A",
             "multiple_choice",
             ["A: hej", "B: tekst", "C: print", "D: błąd"]
             ),
            (1,
             "Ile wynosi x?\n\nx = 5\ny = 2\nx = x - y",
             "D",
             "multiple_choice",
             ["A: 7", "B: 2", "C: 1", "D: 3"]
             ),
            # ===== REORDER =====
            (1,
             "Ułóż kod tak, by wyświetlić sumę 5 i 2.",
             "x = 5\ny = 2\nprint(x + y)",
             "reorder",
             ["print(x + y)", "x = 5", "y = 2"]
             ),
            (1,
             "Ułóż kod, który przypisuje 4 do a, 6 do b i wypisuje ich iloczyn.",
             "a = 4\nb = 6\nprint(a * b)",
             "reorder",
             ["a = 4", "print(a * b)", "b = 6"]
             ),
            (1,
             "Ułóż kod, by wypisać x po nadaniu mu wartości 10.",
             "x = 10\nprint(x)",
             "reorder",
             ["print(x)", "x = 10"]
             ),
            (1,
             "Ułóż kod, który obliczy suma = a + b gdzie a=1, b=2, a następnie wypisze wynik.",
             "a = 1\nb = 2\nsuma = a + b\nprint(suma)",
             "reorder",
             ["print(suma)", "a = 1", "b = 2", "suma = a + b"]
             ),

            # ===== CODE OUTPUT =====
            (1,
             "Co wypisze ten kod?\n\nx = 2\ny = 3\nprint(x + y)",
             "5",
             "code_output",
             None
             ),
            (1,
             "Co wypisze ten kod?\n\nx = 4\nx = x + 1\nprint(x)",
             "5",
             "code_output",
             None
             ),
            (1,
             "Co wypisze ten kod?\n\na = 10\nb = a - 3\nprint(b)",
             "7",
             "code_output",
             None
             ),
            (1,
             "Co wypisze ten kod?\n\nimie = \"Ala\"\nprint(imie)",
             "Ala",
             "code_output",
             None
             ),
            (2, "Ustaw zmienną x na 7 i sprawdź, czy jest większa od 5. Jeśli tak, wypisz 'Duże'",
             "x = 7\nif x > 5:\n    print('Duże')", "code_input", None),
            (2, "Napisz program, który sprawdza, czy liczba y jest równa 10. Jeśli tak, wypisz 'Dziesięć'.",
             "y = 10\nif y == 10:\n    print('Dziesięć')", "code_input", None),
            (2, "Utwórz zmienną liczba = 3. Sprawdź, czy jest mniejsza od 5. Jeśli tak, wypisz 'Mała liczba'.",
             "liczba = 3\nif liczba < 5:\n    print('Mała liczba')", "code_input", None),
            (2,
             "Stwórz zmienną temp = 0. Jeśli jest mniejsza od 10, wypisz 'Zimno', w przeciwnym razie wypisz 'Ciepło'.",
             "temp = 0\nif temp < 10:\n    print('Zimno')\nelse:\n    print('Ciepło')", "code_input", None),
            (2, "Co wypisze ten kod?\n\nx = 8\nif x > 10:\n    print('A')\nelse:\n    print('B')", "B",
             "multiple_choice", ["A: A", "B: B", "C: Nic", "D: Błąd"]),
            (2, "Która linia jest poprawną instrukcją warunkową?", "C", "multiple_choice",
             ["A: if x => 5:", "B: if x < 10 then:", "C: if x == 0:", "D: if(x = 5):"]),
            (2, "Co wypisze ten kod?\n\nx = 5\nif x == 5:\n    print('Tak')\nelse:\n    print('Nie')", "A",
             "multiple_choice", ["A: Tak", "B: Nie", "C: Błąd", "D: x"]),
            (2, "Jakie słowo kluczowe służy do obsługi wielu warunków?", "D", "multiple_choice",
             ["A: otherwise", "B: elseif", "C: alt", "D: elif"]),
            (2, "Ułóż kod tak, by wypisał 'OK', jeśli liczba to 3", "number = 3\nif number == 3:\n    print('OK')",
             "reorder", ["print('OK')", "if number == 3:", "number = 3"]),
            (2, "Ułóż kod, który wypisze 'Zgadza się', jeśli x jest większe od 10, w przeciwnym razie 'Za mało'",
             "x = 12\nif x > 10:\n    print('Zgadza się')\nelse:\n    print('Za mało')", "reorder",
             ["    print('Zgadza się')", "x = 12", "    print('Za mało')", "else:", "if x > 10:"]),
            (2, "Ułóż instrukcję warunkową, która wypisuje 'Zero', jeśli liczba to 0",
             "liczba = 0\nif liczba == 0:\n    print('Zero')", "reorder",
             ["liczba = 0", "if liczba == 0:", "print('Zero')"]),
            (2, "Ułóż kod, który wypisuje 'OK' jeśli x < 5, w przeciwnym razie 'Nie OK'",
             "x = 4\nif x < 5:\n    print('OK')\nelse:\n    print('Nie OK')", "reorder",
             ["    print('Nie OK')", "x = 4", "if x < 5:", "else:", "    print('OK')"]),
            (2, "Jaki będzie wynik działania kodu:\n\nx = 10\nif x < 5:\n    print('Małe')\nelse:\n    print('Duże')",
             "Duże", "code_output", None),
            (2, "Jaki tekst zostanie wypisany?\n\na = 3\nb = 3\nif a == b:\n    print('Równe')", "Równe", "code_output",
             None),
            (2, "Co wypisze ten kod?\n\nliczba = 0\nif liczba:\n    print('Tak')\nelse:\n    print('Nie')", "Nie",
             "code_output", None),
            (2, "Jaki będzie wynik?\n\nif False:\n    print('Pierwsze')\nelse:\n    print('Drugie')", "Drugie",
             "code_output", None),
            (3, "Napisz pętlę for, która wypisze liczby od 0 do 4", "for i in range(5):\n    print(i)", "code_input", None),
            (3, "Napisz pętlę while, która wypisze liczby od 1 do 3", "i = 1\nwhile i <= 3:\n    print(i)\n    i += 1",
             "code_input", None),
            (3, "Wypisz 'Cześć' 3 razy za pomocą pętli for", "for i in range(3):\n    print('Cześć')", "code_input", None),
            (3, "Zlicz sumę liczb od 1 do 5 pętlą for", "suma=0\nfor i in range(1, 6):\n    suma+=i\n    print(suma)",
             "code_input", None),
            (3, "Co wypisze ten kod?\n\nfor i in range(3):\n    print(i)", "B", "multiple_choice",
             ["A: 1 2 3", "B: 0 1 2", "C: 0 1 2 3", "D: Błąd"]),
            (3, "Jak zakończyć pętlę wcześniej?", "A", "multiple_choice", ["A: break", "B: stop", "C: end", "D: exit"]),
            (3, "Która pętla wypisze 5 razy 'hej'?", "C", "multiple_choice",
             ["A: for i in range(6): print('hej')", "B: for i in range(4): print('hej')",
              "C: for i in range(5): print('hej')", "D: for i in range(1,5): print('hej')"]),
            (3, "Które zdanie jest prawdziwe o pętli while?", "D", "multiple_choice",
             ["A: Działa jak if", "B: Wykonuje się raz", "C: Wymaga range()", "D: Działa dopóki warunek jest True"]),
            (3, "Ułóż kod, który wypisuje 0 do 2 za pomocą pętli", "for i in range(3):\n    print(i)", "reorder",
             ["for i in range(3):", "print(i)"]),
            (3, "Ułóż kod z while: wypisz 1 do 3", "i = 1\nwhile i <= 3:\n    print(i)\n    i += 1", "reorder",
             ["while i <= 3:", "print(i)", "i = 1", "i += 1"]),
            (3, "Ułóż pętlę, która wypisze 3 razy 'wow'", "for i in range(3):\n    print('wow')", "reorder",
             ["print('wow')", "for i in range(3):"]),
            (3, "Ułóż kod, który sumuje liczby od 1 do 3 i wypisuje wynik",
             "suma = 0\nfor i in range(1, 4):\n    suma += i\nprint(suma)", "reorder",
             ["suma = 0", "for i in range(1, 4):", "suma += i", "print(suma)"]),
            (3, "Co wypisze ten kod?\n\nfor i in range(2):\n    print('hi')", "hi\nhi", "code_output", None),
            (3, "Co wypisze ten kod?\n\nx = 0\nwhile x < 2:\n    print(x)\n    x += 1", "0\n1", "code_output", None),
            (3, "Jaki będzie wynik?\n\nfor i in range(1, 4):\n    print(i * 2)", "2\n4\n6", "code_output", None),
            (3, "Co zostanie wypisane?\n\nfor i in range(3):\n    print(i + 1)", "1\n2\n3", "code_output", None),
            (4, "Zdefiniuj funkcję bez parametrów, która wypisuje 'Cześć!'", "def przywitaj():\n    print('Cześć!')",
             "code_input", None),
            (4, "Napisz funkcję 'dodaj', która zwraca sumę dwóch liczb a i b", "def dodaj(a, b):\n    return a + b",
             "code_input", None),
            (4, "Stwórz funkcję 'wypisz', która wypisuje 'Python' 3 razy",
             "def wypisz():\n    for i in range(3):\n        print('Python')", "code_input", None),
            (4, "Napisz funkcję 'powitaj', która przyjmuje imię i wypisuje powitanie",
             "def powitaj(imie):\n    print('Cześć, ' + imie)", "code_input", None),
            (4, "Co wypisze ten kod?\n\ndef test():\n    return 5\nprint(test())", "C", "multiple_choice",
             ["A: test", "B: None", "C: 5", "D: Błąd"]),
            (4, "Gdzie umieszczamy kod wewnątrz funkcji?", "B", "multiple_choice",
             ["A: przed def", "B: wcięcie pod def", "C: po nawiasach", "D: w zmiennej"]),
            (4, "Co oznacza słowo kluczowe 'return'?", "D", "multiple_choice",
             ["A: zakończenie pętli", "B: wyświetlenie wyniku", "C: przypisanie zmiennej", "D: zwrócenie wartości"]),
            (4, "Która funkcja zwróci poprawnie kwadrat liczby?", "A", "multiple_choice",
             ["A: def kwadrat(x): return x * x", "B: def kwadrat(x): print(x * x)", "C: def kwadrat(x): x ** 2",
              "D: def kwadrat(x): return x + x"]),
            (4, "Ułóż funkcję, która wypisuje 'OK'", "def pokaz():\n    print('OK')", "reorder",
             ["print('OK')", "def pokaz():"]),
            (4, "Ułóż funkcję, która przyjmuje liczbę i wypisuje jej podwojoną wartość",
             "def podwoj(x):\n    print(x * 2)", "reorder", ["print(x * 2)", "def podwoj(x):"]),
            (4, "Ułóż kod, który definiuje funkcję i ją wywołuje", "def hej():\n    print('Hej')\nhej()", "reorder",
             ["hej()", "print('Hej')", "def hej():"]),
            (4, "Zdefiniuj funkcję, która dodaje 2 do liczby i ją zwraca", "def dodaj_dwa(x):\n    return x + 2",
             "reorder", ["def dodaj_dwa(x):", "return x + 2"]),
            (4, "Co wypisze ten kod?\n\ndef f():\n    return 2 + 2\nprint(f())", "4", "code_output", None),
            (4, "Co wypisze ten kod?\n\ndef witaj(imie):\n    print('Hej ' + imie)\nwitaj('Kuba')", "Hej Kuba",
             "code_output", None),
            (
            4, "Co wypisze ten kod?\n\ndef suma(a, b):\n    return a + b\nprint(suma(3, 4))", "7", "code_output", None),
            (4, "Co wypisze ten kod?\n\ndef tekst():\n    return 'OK'\nprint(tekst())", "OK", "code_output", None),
            (5, "Utwórz listę 'lista' zawierającą liczby 1, 2 i 3", "lista = [1, 2, 3]", "code_input", None),
            (5, "Dodaj element 4 do listy liczby = [1, 2, 3]", "liczby = [1, 2, 3]\nliczby.append(4)", "code_input",
             None),
            (5, "Utwórz pustą listę o nazwie dane", "dane = []", "code_input", None),
            (5, "Wypisz każdy element listy za pomocą pętli for: [5, 10, 15]", "for x in [5, 10, 15]:\n    print(x)",
             "code_input", None),
            (5, "Co wypisze ten kod?\n\nlista = [1, 2, 3]\nprint(lista[0])", "A", "multiple_choice",
             ["A: 1", "B: 2", "C: 0", "D: Błąd"]),
            (5, "Jak dodać 99 na koniec listy dane?", "C", "multiple_choice",
             ["A: dane = dane + 99", "B: dane.insert(99)", "C: dane.append(99)", "D: add(dane, 99)"]),
            (5, "Który zapis usuwa element z listy?", "B", "multiple_choice",
             ["A: remove(lista)", "B: lista.remove(2)", "C: delete lista", "D: lista.delete(2)"]),
            (5, "Co wypisze ten kod?\n\ndane = [10, 20, 30]\nprint(len(dane))", "C", "multiple_choice",
             ["A: 30", "B: 0", "C: 3", "D: Błąd"]),
            (5, "Ułóż kod, który tworzy listę z 3 imionami i wypisuje je w pętli",
             "imiona = ['Ala', 'Bartek', 'Celina']\nfor imie in imiona:\n    print(imie)", "reorder",
             ["print(imie)", "for imie in imiona:", "imiona = ['Ala', 'Bartek', 'Celina']"]),
            (5, "Ułóż kod, który tworzy pustą listę i dodaje do niej 5", "liczby = []\nliczby.append(5)\nprint(liczby)",
             "reorder", ["liczby = []", "liczby.append(5)", "print(liczby)"]),
            (5, "Ułóż kod, który wypisuje liczby z listy [3, 6] tylko jeśli są większe niż 4",
             "lista = [3, 6]\nfor x in lista:\n    if x > 4:\n        print(x)", "reorder",
             ["for x in lista:", "if x > 4:", "print(x)", "lista = [3, 6]"]),
            (5, "Ułóż kod, który tworzy listę liczb od 0 do 4 i wypisuje ich kwadraty",
             "for i in range(5):\n    print(i ** 2)", "reorder", ["print(i ** 2)", "for i in range(5):"]),
            (5, "Co wypisze ten kod?\n\nlista = [1, 2, 3]\nprint(len(lista))", "3", "code_output", None),
            (5, "Co wypisze ten kod?\n\nx = [2, 4]\nx.append(6)\nprint(x)", "[2, 4, 6]", "code_output", None),
            (5, "Co wypisze ten kod?\n\nfor i in [3, 5]:\n    print(i * 2)", "6\n10", "code_output", None),
            (5, "Co wypisze ten kod?\n\nlista = [7, 8]\nprint(lista[1])", "8", "code_output", None)
        ]

        tasks = []
        lesson_index_counters = {}

        for lesson_index, question, solution, type_, options in raw_data:
            count = lesson_index_counters.get(lesson_index, 0)
            lesson_index_counters[lesson_index] = count + 1

            task = Task(
                lesson_index=lesson_index,
                question=question,
                solution=solution,
                type=type_,
                options=options,
                task_index=count
            )

            tasks.append(task)

        return tasks



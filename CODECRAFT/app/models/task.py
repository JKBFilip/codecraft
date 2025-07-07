class Task:
    def __init__(self, lesson_index, question, solution, type="code_input", options=None, blocks=None):
        self.lesson_index = lesson_index
        self.question = question
        self.solution = solution
        self.type = type  # "code_input", "multiple_choice", "reorder", "code_output"
        self.options = options or []
        self.blocks = blocks or []

    @staticmethod
    def load_all():
        return [
            # ===== CODE INPUT =====
            Task(1, "Przypisz wartość 10 do zmiennej 'wiek'", "wiek = 10"),
            Task(1, "Zadeklaruj zmienną 'imie' i przypisz do niej swoje imię", 'imie = "Kuba"'),
            Task(1, "Utwórz dwie zmienne a i b, przypisz im wartości 3 i 7", "a = 3\nb = 7"),
            Task(1, "Zmienna x ma wartość 5. Zwiększ ją o 2.", "x = 5\nx = x + 2"),

            # ===== MULTIPLE CHOICE =====
            Task(
                1,
                "Co zostanie wypisane na ekranie?\n\na = 2\nb = a + 3\nprint(b)",
                solution="C",
                type="multiple_choice",
                options=["A: 2", "B: 3", "C: 5", "D: Błąd"]
            ),
            Task(
                1,
                "Jaką wartość ma zmienna x po tym kodzie?\n\nx = 4\nx = x * 2",
                solution="B",
                type="multiple_choice",
                options=["A: 4", "B: 8", "C: 6", "D: x"]
            ),
            Task(
                1,
                "Co wypisze ten kod?\n\ntekst = \"hej\"\nprint(tekst)",
                solution="A",
                type="multiple_choice",
                options=["A: hej", "B: tekst", "C: print", "D: błąd"]
            ),
            Task(
                1,
                "Ile wynosi x?\n\nx = 5\ny = 2\nx = x - y",
                solution="D",
                type="multiple_choice",
                options=["A: 7", "B: 2", "C: 1", "D: 3"]
            ),

            # ===== REORDER =====
            Task(
                1,
                "Ułóż kod tak, by wyświetlić sumę 5 i 2.",
                solution="x = 5\ny = 2\nprint(x + y)",
                type="reorder",
                options=["print(x + y)", "x = 5", "y = 2"]
            ),
            Task(
                1,
                "Ułóż kod, który przypisuje 4 do a, 6 do b i wypisuje ich iloczyn.",
                solution="a = 4\nb = 6\nprint(a * b)",
                type="reorder",
                options=["a = 4", "print(a * b)", "b = 6"]
            ),
            Task(
                1,
                "Ułóż kod, by wypisać x po nadaniu mu wartości 10.",
                solution="x = 10\nprint(x)",
                type="reorder",
                options=["print(x)", "x = 10"]
            ),
            Task(
                1,
                "Ułóż kod, który obliczy suma = a + b gdzie a=1, b=2, a następnie wypisze wynik.",
                solution="a = 1\nb = 2\nsuma = a + b\nprint(suma)",
                type="reorder",
                options=["print(suma)", "a = 1", "b = 2", "suma = a + b"]
            ),

            # ===== CODE OUTPUT =====
            Task(
                1,
                "Co wypisze ten kod?\n\nx = 2\ny = 3\nprint(x + y)",
                solution="5",
                type="code_output"
            ),
            Task(
                1,
                "Co wypisze ten kod?\n\nx = 4\nx = x + 1\nprint(x)",
                solution="5",
                type="code_output"
            ),
            Task(
                1,
                "Co wypisze ten kod?\n\na = 10\nb = a - 3\nprint(b)",
                solution="7",
                type="code_output"
            ),
            Task(
                1,
                "Co wypisze ten kod?\n\nimie = \"Ala\"\nprint(imie)",
                solution="Ala",
                type="code_output"
            ),
            Task(2, "Ustaw zmienną x na 7 i sprawdź, czy jest większa od 5. Jeśli tak, wypisz 'Duże'",
                 "x = 7\nif x > 5:\n    print('Duże')"),

            Task(2, "Napisz program, który sprawdza, czy liczba y jest równa 10. Jeśli tak, wypisz 'Dziesięć'.",
                 "y = 10\nif y == 10:\n    print('Dziesięć')"),

            Task(2, "Utwórz zmienną liczba = 3. Sprawdź, czy jest mniejsza od 5. Jeśli tak, wypisz 'Mała liczba'.",
                 "liczba = 3\nif liczba < 5:\n    print('Mała liczba')"),

            Task(2,
                 "Stwórz zmienną temp = 0. Jeśli jest mniejsza od 10, wypisz 'Zimno', w przeciwnym razie wypisz 'Ciepło'.",
                 "temp = 0\nif temp < 10:\n    print('Zimno')\nelse:\n    print('Ciepło')"),

            Task(2,
                 "Co wypisze ten kod?\n\nx = 8\nif x > 10:\n    print('A')\nelse:\n    print('B')",
                 solution="B",
                 type="multiple_choice",
                 options=["A: A", "B: B", "C: Nic", "D: Błąd"]),

            Task(2,
                 "Która linia jest poprawną instrukcją warunkową?",
                 solution="C",
                 type="multiple_choice",
                 options=["A: if x => 5:", "B: if x < 10 then:", "C: if x == 0:", "D: if(x = 5):"]),

            Task(2,
                 "Co wypisze ten kod?\n\nx = 5\nif x == 5:\n    print('Tak')\nelse:\n    print('Nie')",
                 solution="A",
                 type="multiple_choice",
                 options=["A: Tak", "B: Nie", "C: Błąd", "D: x"]),

            Task(2,
                 "Jakie słowo kluczowe służy do obsługi wielu warunków?",
                 solution="D",
                 type="multiple_choice",
                 options=["A: otherwise", "B: elseif", "C: alt", "D: elif"]),

            Task(
                2,
                "Ułóż kod tak, by wypisał 'OK', jeśli liczba to 3",
                solution="number = 3\nif number == 3:\n    print('OK')",
                type="reorder",
                options=[
                    "print('OK')",
                    "if number == 3:",
                    "number = 3"
                ]
            ),

            Task(
                2,
                "Ułóż kod, który wypisze 'Zgadza się', jeśli x jest większe od 10, w przeciwnym razie 'Za mało'",
                solution="x = 12\nif x > 10:\n    print('Zgadza się')\nelse:\n    print('Za mało')",
                type="reorder",
                options=[
                    "    print('Zgadza się')",
                    "x = 12",
                    "    print('Za mało')",
                    "else:",
                    "if x > 10:"
                ]
            ),

            Task(
                2,
                "Ułóż instrukcję warunkową, która wypisuje 'Zero', jeśli liczba to 0",
                solution="liczba = 0\nif liczba == 0:\n    print('Zero')",
                type="reorder",
                options=[
                    "liczba = 0",
                    "if liczba == 0:",
                    "print('Zero')"
                ]
            ),

            Task(
                2,
                "Ułóż kod, który wypisuje 'OK' jeśli x < 5, w przeciwnym razie 'Nie OK'",
                solution="x = 4\nif x < 5:\n    print('OK')\nelse:\n    print('Nie OK')",
                type="reorder",
                options=[
                    "    print('Nie OK')",
                    "x = 4",
                    "if x < 5:",
                    "else:",
                    "    print('OK')"
                ]
            ),

            Task(2,
                 "Jaki będzie wynik działania kodu:\n\nx = 10\nif x < 5:\n    print('Małe')\nelse:\n    print('Duże')",
                 solution="Duże",
                 type="code_output"),

            Task(2,
                 "Jaki tekst zostanie wypisany?\n\na = 3\nb = 3\nif a == b:\n    print('Równe')",
                 solution="Równe",
                 type="code_output"),

            Task(2,
                 "Co wypisze ten kod?\n\nliczba = 0\nif liczba:\n    print('Tak')\nelse:\n    print('Nie')",
                 solution="Nie",
                 type="code_output"),

            Task(2,
                 "Jaki będzie wynik?\n\nif False:\n    print('Pierwsze')\nelse:\n    print('Drugie')",
                 solution="Drugie",
                 type="code_output"),
            Task(3, "Napisz pętlę, która wypisze liczby od 0 do 4", "for i in range(5):\n    print(i)"),

            Task(3, "Napisz pętlę while, która wypisze liczby od 1 do 3",
                 "i = 1\nwhile i <= 3:\n    print(i)\n    i += 1"),

            Task(3, "Wypisz 'Cześć' 3 razy za pomocą pętli", "for i in range(3):\n    print('Cześć')"),

            Task(3, "Zlicz sumę liczb od 1 do 5", "suma=0\nfor i in range(1, 6):\n    suma+=i\n    print(suma)"),
            Task(3,
                 "Co wypisze ten kod?\n\nfor i in range(3):\n    print(i)",
                 solution="B",
                 type="multiple_choice",
                 options=["A: 1 2 3", "B: 0 1 2", "C: 0 1 2 3", "D: Błąd"]),

            Task(3,
                 "Jak zakończyć pętlę wcześniej?",
                 solution="A",
                 type="multiple_choice",
                 options=["A: break", "B: stop", "C: end", "D: exit"]),

            Task(3,
                 "Która pętla wypisze 5 razy 'hej'?",
                 solution="C",
                 type="multiple_choice",
                 options=["A: for i in range(6): print('hej')", "B: for i in range(4): print('hej')",
                          "C: for i in range(5): print('hej')", "D: for i in range(1,5): print('hej')"]),

            Task(3,
                 "Które zdanie jest prawdziwe o pętli while?",
                 solution="D",
                 type="multiple_choice",
                 options=["A: Działa jak if", "B: Wykonuje się raz", "C: Wymaga range()",
                          "D: Działa dopóki warunek jest True"]),
            Task(3,
                 "Ułóż kod, który wypisuje 0 do 2 za pomocą pętli",
                 solution="for i in range(3):\n    print(i)",
                 type="reorder",
                 options=["for i in range(3):", "print(i)"]),

            Task(3,
                 "Ułóż kod z while: wypisz 1 do 3",
                 solution="i = 1\nwhile i <= 3:\n    print(i)\n    i += 1",
                 type="reorder",
                 options=["while i <= 3:", "print(i)", "i = 1", "i += 1"]),

            Task(3,
                 "Ułóż pętlę, która wypisze 3 razy 'wow'",
                 solution="for i in range(3):\n    print('wow')",
                 type="reorder",
                 options=["print('wow')", "for i in range(3):"]),

            Task(3,
                 "Ułóż kod, który sumuje liczby od 1 do 3 i wypisuje wynik",
                 solution="suma = 0\nfor i in range(1, 4):\n    suma += i\nprint(suma)",
                 type="reorder",
                 options=["suma = 0", "for i in range(1, 4):", "suma += i", "print(suma)"]),
            Task(3,
                 "Co wypisze ten kod?\n\nfor i in range(2):\n    print('hi')",
                 solution="hi\nhi",
                 type="code_output"),

            Task(3,
                 "Co wypisze ten kod?\n\nx = 0\nwhile x < 2:\n    print(x)\n    x += 1",
                 solution="0\n1",
                 type="code_output"),

            Task(3,
                 "Jaki będzie wynik?\n\nfor i in range(1, 4):\n    print(i * 2)",
                 solution="2\n4\n6",
                 type="code_output"),

            Task(3,
                 "Co zostanie wypisane?\n\nfor i in range(3):\n    print(i + 1)",
                 solution="1\n2\n3",
                 type="code_output"),
            Task(4,
                 "Zdefiniuj funkcję bez parametrów, która wypisuje 'Cześć!'",
                 solution="def przywitaj():\n    print('Cześć!')",
                 type="code_input"
                 ),

            Task(4,
                 "Napisz funkcję dodaj, która zwraca sumę dwóch liczb a i b",
                 solution="def dodaj(a, b):\n    return a + b",
                 type="code_input"
                 ),

            Task(4,
                 "Stwórz funkcję, która wypisuje 'Python' 3 razy",
                 solution="def wypisz():\n    for i in range(3):\n        print('Python')",
                 type="code_input"
                 ),

            Task(4,
                 "Napisz funkcję, która przyjmuje imię i wypisuje powitanie",
                 solution="def powitaj(imie):\n    print('Cześć, ' + imie)",
                 type="code_input"
                 ),
            Task(4,
                 "Co wypisze ten kod?\n\ndef test():\n    return 5\nprint(test())",
                 solution="C",
                 type="multiple_choice",
                 options=["A: test", "B: None", "C: 5", "D: Błąd"]
                 ),
            Task(4,
                 "Gdzie umieszczamy kod wewnątrz funkcji?",
                 solution="B",
                 type="multiple_choice",
                 options=["A: przed def", "B: wcięcie pod def", "C: po nawiasach", "D: w zmiennej"]
                 ),
            Task(4,
                 "Co oznacza słowo kluczowe 'return'?",
                 solution="D",
                 type="multiple_choice",
                 options=["A: zakończenie pętli", "B: wyświetlenie wyniku", "C: przypisanie zmiennej",
                          "D: zwrócenie wartości"]
                 ),
            Task(4,
                 "Która funkcja zwróci poprawnie kwadrat liczby?",
                 solution="A",
                 type="multiple_choice",
                 options=[
                     "A: def kwadrat(x): return x * x",
                     "B: def kwadrat(x): print(x * x)",
                     "C: def kwadrat(x): x ** 2",
                     "D: def kwadrat(x): return x + x"
                 ]
                 ),
            Task(4,
                 "Ułóż funkcję, która wypisuje 'OK'",
                 solution="def pokaz():\n    print('OK')",
                 type="reorder",
                 options=["print('OK')", "def pokaz():"]
                 ),
            Task(4,
                 "Ułóż funkcję, która przyjmuje liczbę i wypisuje jej podwojoną wartość",
                 solution="def podwoj(x):\n    print(x * 2)",
                 type="reorder",
                 options=["print(x * 2)", "def podwoj(x):"]
                 ),
            Task(4,
                 "Ułóż kod, który definiuje funkcję i ją wywołuje",
                 solution="def hej():\n    print('Hej')\nhej()",
                 type="reorder",
                 options=["hej()", "print('Hej')", "def hej():"]
                 ),
            Task(4,
                 "Zdefiniuj funkcję, która dodaje 2 do liczby i ją zwraca",
                 solution="def dodaj_dwa(x):\n    return x + 2",
                 type="reorder",
                 options=["def dodaj_dwa(x):", "return x + 2"]
                 ),
            Task(4,
                 "Co wypisze ten kod?\n\ndef f():\n    return 2 + 2\nprint(f())",
                 solution="4",
                 type="code_output"
                 ),
            Task(4,
                 "Co wypisze ten kod?\n\ndef witaj(imie):\n    print('Hej ' + imie)\nwitaj('Kuba')",
                 solution="Hej Kuba",
                 type="code_output"
                 ),
            Task(4,
                 "Co wypisze ten kod?\n\ndef suma(a, b):\n    return a + b\nprint(suma(3, 4))",
                 solution="7",
                 type="code_output"
                 ),
            Task(4,
                 "Co wypisze ten kod?\n\ndef tekst():\n    return 'OK'\nprint(tekst())",
                 solution="OK",
                 type="code_output"
                 ),
            Task(
                5,
                "Utwórz listę zawierającą liczby 1, 2 i 3",
                solution="lista = [1, 2, 3]",
                type="code_input"
            ),

            Task(
                5,
                "Dodaj element 4 do listy liczby = [1, 2, 3]",
                solution="liczby = [1, 2, 3]\nliczby.append(4)",
                type="code_input"
            ),

            Task(
                5,
                "Utwórz pustą listę o nazwie dane",
                solution="dane = []",
                type="code_input"
            ),

            Task(
                5,
                "Wypisz każdy element listy za pomocą pętli for: [5, 10, 15]",
                solution="for x in [5, 10, 15]:\n    print(x)",
                type="code_input"
            ),
            Task(
                5,
                "Co wypisze ten kod?\n\nlista = [1, 2, 3]\nprint(lista[0])",
                solution="A",
                type="multiple_choice",
                options=["A: 1", "B: 2", "C: 0", "D: Błąd"]
            ),

            Task(
                5,
                "Jak dodać 99 na koniec listy dane?",
                solution="C",
                type="multiple_choice",
                options=["A: dane = dane + 99", "B: dane.insert(99)", "C: dane.append(99)", "D: add(dane, 99)"]
            ),

            Task(
                5,
                "Który zapis usuwa element z listy?",
                solution="B",
                type="multiple_choice",
                options=["A: remove(lista)", "B: lista.remove(2)", "C: delete lista", "D: lista.delete(2)"]
            ),

            Task(
                5,
                "Co wypisze ten kod?\n\ndane = [10, 20, 30]\nprint(len(dane))",
                solution="C",
                type="multiple_choice",
                options=["A: 30", "B: 0", "C: 3", "D: Błąd"]
            ),
            Task(
                5,
                "Ułóż kod, który tworzy listę z 3 imionami i wypisuje je w pętli",
                solution="imiona = ['Ala', 'Bartek', 'Celina']\nfor imie in imiona:\n    print(imie)",
                type="reorder",
                options=["print(imie)", "for imie in imiona:", "imiona = ['Ala', 'Bartek', 'Celina']"]
            ),

            Task(
                5,
                "Ułóż kod, który tworzy pustą listę i dodaje do niej 5",
                solution="liczby = []\nliczby.append(5)\nprint(liczby)",
                type="reorder",
                options=["liczby = []", "liczby.append(5)", "print(liczby)"]
            ),

            Task(
                5,
                "Ułóż kod, który wypisuje liczby z listy [3, 6] tylko jeśli są większe niż 4",
                solution="lista = [3, 6]\nfor x in lista:\n    if x > 4:\n        print(x)",
                type="reorder",
                options=["for x in lista:", "if x > 4:", "print(x)", "lista = [3, 6]"]
            ),

            Task(
                5,
                "Ułóż kod, który tworzy listę liczb od 0 do 4 i wypisuje ich kwadraty",
                solution="for i in range(5):\n    print(i ** 2)",
                type="reorder",
                options=["print(i ** 2)", "for i in range(5):"]
            ),
            Task(
                5,
                "Co wypisze ten kod?\n\nlista = [1, 2, 3]\nprint(len(lista))",
                solution="3",
                type="code_output"
            ),

            Task(
                5,
                "Co wypisze ten kod?\n\nx = [2, 4]\nx.append(6)\nprint(x)",
                solution="[2, 4, 6]",
                type="code_output"
            ),

            Task(
                5,
                "Co wypisze ten kod?\n\nfor i in [3, 5]:\n    print(i * 2)",
                solution="6\n10",
                type="code_output"
            ),

            Task(
                5,
                "Co wypisze ten kod?\n\nlista = [7, 8]\nprint(lista[1])",
                solution="8",
                type="code_output"
            ),

        ]

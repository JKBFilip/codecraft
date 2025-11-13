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
            # === Moduł 1: Zmienne ===
            (1, "Przypisz wartość **liczbową** 10 do zmiennej o nazwie `wiek`", "wiek = 10", "code_input", None),
            (1, "Zadeklaruj zmienną o nazwie `imie` i przypisz do niej **tekst** 'Olek' (użyj cudzysłowów)",
             'imie = "Olek"', "code_input", None),
            (1, "Utwórz dwie zmienne: `a` z wartością 3 i `b` z wartością 7", "a = 3\nb = 7", "code_input", None),
            (1, "Ustaw zmienną `x` na wartość 5, następnie w **następnej linii** zwiększ jej wartość o 2.",
             "x = 5\nx = x + 2", "code_input", None),
            (1, "Co zostanie wypisane? `a = 2`, `b = a + 3`, `print(b)`", "C", "multiple_choice",
             ["A: 2", "B: 3", "C: 5", "D: Błąd"]),
            (1, "Jaką wartość ma `x`? `x = 4`, `x = x * 2`", "B", "multiple_choice", ["A: 4", "B: 8", "C: 6", "D: x"]),
            (1, "Co wypisze kod? `tekst = \"hej\"`, `print(tekst)`", "A", "multiple_choice",
             ["A: hej", "B: tekst", "C: print", "D: błąd"]),
            (1, "Ile wynosi `x`? `x = 5`, `y = 2`, `x = x - y`", "D", "multiple_choice",
             ["A: 7", "B: 2", "C: 1", "D: 3"]),
            (1, "Ułóż kod: 1. `x=5`, 2. `y=2`, 3. wypisz `x + y`.", "x = 5\ny = 2\nprint(x + y)", "reorder",
             ["print(x + y)", "x = 5", "y = 2"]),
            (1, "Ułóż kod: 1. `a=4`, 2. `b=6`, 3. wypisz `a * b`.", "a = 4\nb = 6\nprint(a * b)", "reorder",
             ["a = 4", "print(a * b)", "b = 6"]),
            (1, "Ułóż kod: 1. `x=10`, 2. wypisz `x`.", "x = 10\nprint(x)", "reorder", ["print(x)", "x = 10"]),
            (1, "Ułóż kod: 1. `a=1`, 2. `b=2`, 3. `suma = a + b`, 4. wypisz `suma`.",
             "a = 1\nb = 2\nsuma = a + b\nprint(suma)", "reorder", ["print(suma)", "a = 1", "b = 2", "suma = a + b"]),
            (1, "Co wypisze kod? `x = 2`, `y = 3`, `print(x + y)`", "5", "code_output", None),
            (1, "Co wypisze kod? `x = 4`, `x = x + 1`, `print(x)`", "5", "code_output", None),
            (1, "Co wypisze kod? `a = 10`, `b = a - 3`, `print(b)`", "7", "code_output", None),
            (1, "Co wypisze kod? `imie = \"Ala\"`, `print(imie)`", "Ala", "code_output", None),

            # === Moduł 2: Warunki ===
            (2,
             "Ustaw zmienną `x` na 7. W **następnej linii** sprawdź, czy `x` jest większe od 5. Jeśli tak, wypisz **tekst** 'Duże'.",
             "x = 7\nif x > 5:\n    print('Duże')", "code_input", None),
            (2, "Napisz kod: zmienna `y` = 10. Jeśli `y` jest **równe** 10, wypisz **tekst** 'Dziesięć'.",
             "y = 10\nif y == 10:\n    print('Dziesięć')", "code_input", None),
            (2, "Utwórz zmienną `liczba` = 3. Jeśli jest **mniejsza niż** 5, wypisz **tekst** 'Mała liczba'.",
             "liczba = 3\nif liczba < 5:\n    print('Mała liczba')", "code_input", None),
            (2, "Zmienna `temp` = 0. Jeśli `temp` < 10, wypisz 'Zimno', w przeciwnym razie ('else') wypisz 'Ciepło'.",
             "temp = 0\nif temp < 10:\n    print('Zimno')\nelse:\n    print('Ciepło')", "code_input", None),
            (2, "Co wypisze kod? `x = 8`, `if x > 10: print('A') else: print('B')`", "B", "multiple_choice",
             ["A: A", "B: B", "C: Nic", "D: Błąd"]),
            (2, "Która linia jest poprawną instrukcją warunkową w Pythonie?", "C", "multiple_choice",
             ["A: if x => 5:", "B: if x < 10 then:", "C: if x == 0:", "D: if(x = 5):"]),
            (2, "Co wypisze kod? `x = 5`, `if x == 5: print('Tak') else: print('Nie')`", "A", "multiple_choice",
             ["A: Tak", "B: Nie", "C: Błąd", "D: x"]),
            (2, "Jakie słowo kluczowe w Pythonie służy do obsługi kolejnego warunku po 'if'?", "D", "multiple_choice",
             ["A: otherwise", "B: elseif", "C: alt", "D: elif"]),
            (2, "Ułóż kod: 1. `number = 3`, 2. jeśli `number == 3`, 3. wypisz 'OK'.",
             "number = 3\nif number == 3:\n    print('OK')", "reorder",
             ["print('OK')", "if number == 3:", "number = 3"]),
            (2,
             "Ułóż kod: 1. `x = 12`, 2. jeśli `x > 10`, 3. wypisz 'Zgadza się', 4. w przeciwnym razie ('else'), 5. wypisz 'Za mało'.",
             "x = 12\nif x > 10:\n    print('Zgadza się')\nelse:\n    print('Za mało')", "reorder",
             ["    print('Zgadza się')", "x = 12", "    print('Za mało')", "else:", "if x > 10:"]),
            (2, "Ułóż kod: 1. `liczba = 0`, 2. jeśli `liczba == 0`, 3. wypisz 'Zero'.",
             "liczba = 0\nif liczba == 0:\n    print('Zero')", "reorder",
             ["liczba = 0", "if liczba == 0:", "    print('Zero')"]),
            (2,
             "Ułóż kod: 1. `x = 4`, 2. jeśli `x < 5`, 3. wypisz 'OK', 4. w przeciwnym razie ('else'), 5. wypisz 'Nie OK'.",
             "x = 4\nif x < 5:\n    print('OK')\nelse:\n    print('Nie OK')", "reorder",
             ["    print('Nie OK')", "x = 4", "if x < 5:", "else:", "    print('OK')"]),
            (2, "Co wypisze kod? `x = 10`, `if x < 5: print('Małe') else: print('Duże')`", "Duże", "code_output", None),
            (2, "Co wypisze kod? `a = 3`, `b = 3`, `if a == b: print('Równe')`", "Równe", "code_output", None),
            (2, "Co wypisze kod? `liczba = 0`, `if liczba: print('Tak') else: print('Nie')`", "Nie", "code_output",
             None),
            (2, "Co wypisze kod? `if False: print('Pierwsze') else: print('Drugie')`", "Drugie", "code_output", None),

            # === Moduł 3: Pętle ===
            (
            3, "Napisz pętlę `for`, która wypisze liczby od 0 **do 4** (włącznie).", "for i in range(5):\n    print(i)",
            "code_input", None),
            (3, "Napisz pętlę `while`, która wypisze liczby od 1 **do 3** (włącznie).",
             "i = 1\nwhile i <= 3:\n    print(i)\n    i += 1", "code_input", None),
            (3, "Wypisz **tekst** 'Cześć' dokładnie 3 razy, używając pętli `for`.",
             "for i in range(3):\n    print('Cześć')", "code_input", None),
            (3,
             "Zadeklaruj zmienną `suma` równą 0. Następnie pętlą `for` zlicz sumę liczb od 1 **do 5** (włącznie). Po pętli wypisz wartość `suma`.",
             "suma = 0\nfor i in range(1, 6):\n    suma += i\nprint(suma)", "code_input", None),
            (3, "Co wypisze kod? `for i in range(3): print(i)`", "B", "multiple_choice",
             ["A: 1 2 3", "B: 0 1 2", "C: 0 1 2 3", "D: Błąd"]),
            (3, "Jak **natychmiastowo** zakończyć bieżącą iterację pętli i przejść do następnej?", "C",
             "multiple_choice", ["A: break", "B: stop", "C: continue", "D: next"]),
            (3, "Która pętla wypisze dokładnie 5 razy 'hej'?", "C", "multiple_choice",
             ["A: for i in range(6): print('hej')", "B: for i in range(4): print('hej')",
              "C: for i in range(5): print('hej')", "D: for i in range(1,5): print('hej')"]),
            (3, "Które zdanie jest prawdziwe o pętli `while`?", "D", "multiple_choice",
             ["A: Działa jak if", "B: Wykonuje się tylko raz", "C: Zawsze wymaga range()",
              "D: Działa dopóki jej warunek jest True"]),
            (3, "Ułóż kod, który pętlą `for` wypisuje liczby 0, 1, 2.", "for i in range(3):\n    print(i)", "reorder",
             ["for i in range(3):", "    print(i)"]),
            (3, "Ułóż kod z `while`, który wypisuje liczby 1, 2, 3.", "i = 1\nwhile i <= 3:\n    print(i)\n    i += 1",
             "reorder", ["while i <= 3:", "    print(i)", "i = 1", "    i += 1"]),
            (3, "Ułóż pętlę `for`, która wypisze 3 razy 'wow'.", "for i in range(3):\n    print('wow')", "reorder",
             ["    print('wow')", "for i in range(3):"]),
            (3, "Ułóż kod: 1. `suma=0`, 2. pętla `for` od 1 do 3, 3. w pętli `suma += i`, 4. po pętli wypisz `suma`.",
             "suma = 0\nfor i in range(1, 4):\n    suma += i\nprint(suma)", "reorder",
             ["suma = 0", "for i in range(1, 4):", "    suma += i", "print(suma)"]),
            (3, "Co wypisze kod? `for i in range(2): print('hi')`", "hi\nhi", "code_output", None),
            (3, "Co wypisze kod? `x = 0`, `while x < 2: print(x); x += 1`", "0\n1", "code_output", None),
            (3, "Jaki będzie wynik? `for i in range(1, 4): print(i * 2)`", "2\n4\n6", "code_output", None),
            (3, "Co zostanie wypisane? `for i in range(3): print(i + 1)`", "1\n2\n3", "code_output", None),

            # === Moduł 4: Funkcje ===
            (4, "Zdefiniuj funkcję o nazwie `przywitaj`, która nie przyjmuje argumentów i wypisuje **tekst** 'Cześć!'.",
             "def przywitaj():\n    print('Cześć!')", "code_input", None),
            (4,
             "Napisz funkcję o nazwie `dodaj`, która przyjmuje dwa argumenty (`a`, `b`) i **zwraca** (`return`) ich sumę.",
             "def dodaj(a, b):\n    return a + b", "code_input", None),
            (4,
             "Stwórz funkcję o nazwie `wypisz_python`, która wypisuje **tekst** 'Python' dokładnie 3 razy (użyj pętli).",
             "def wypisz_python():\n    for i in range(3):\n        print('Python')", "code_input", None),
            (4,
             "Napisz funkcję o nazwie `powitanie`, która przyjmuje jeden argument `imie` i wypisuje powitanie, np. 'Cześć, Ania' (użyj konkatenacji '+' lub f-stringa).",
             "def powitanie(imie):\n    print('Cześć, ' + imie)", "code_input", None),
            (4, "Co wypisze kod? `def test(): return 5`, `print(test())`", "C", "multiple_choice",
             ["A: test", "B: None", "C: 5", "D: Błąd"]),
            (4, "Gdzie umieszczamy kod, który ma być wykonany wewnątrz funkcji?", "B", "multiple_choice",
             ["A: Przed słowem kluczowym 'def'", "B: We wcięciu (indentacji) pod linią 'def'",
              "C: Po nawiasach definicji funkcji", "D: W osobnym pliku"]),
            (4, "Co robi instrukcja `return` w funkcji?", "D", "multiple_choice",
             ["A: Natychmiast kończy cały program", "B: Wypisuje wartość na ekranie", "C: Tworzy nową zmienną",
              "D: Zwraca wartość z funkcji i kończy jej działanie"]),
            (4, "Która definicja funkcji poprawnie zwraca kwadrat podanej liczby `x`?", "A", "multiple_choice",
             ["A: def kwadrat(x): return x * x", "B: def kwadrat(x): print(x * x)", "C: def kwadrat(x): x ** 2",
              "D: def kwadrat(x): return x + x"]),
            (4, "Ułóż kod: 1. zdefiniuj funkcję `pokaz`, 2. wewnątrz wypisz 'OK'.", "def pokaz():\n    print('OK')",
             "reorder", ["    print('OK')", "def pokaz():"]),
            (4, "Ułóż kod: 1. zdefiniuj funkcję `podwoj(x)`, 2. wewnątrz wypisz `x * 2`.",
             "def podwoj(x):\n    print(x * 2)", "reorder", ["    print(x * 2)", "def podwoj(x):"]),
            (4, "Ułóż kod: 1. zdefiniuj funkcję `hej`, 2. wewnątrz wypisz 'Hej', 3. wywołaj funkcję `hej`.",
             "def hej():\n    print('Hej')\nhej()", "reorder", ["hej()", "    print('Hej')", "def hej():"]),
            (4, "Ułóż kod: 1. zdefiniuj funkcję `dodaj_dwa(x)`, 2. wewnątrz zwróć (`return`) `x + 2`.",
             "def dodaj_dwa(x):\n    return x + 2", "reorder", ["def dodaj_dwa(x):", "    return x + 2"]),
            (4, "Co wypisze kod? `def f(): return 2 + 2`, `print(f())`", "4", "code_output", None),
            (4, "Co wypisze kod? `def witaj(imie): print('Hej ' + imie)`, `witaj('Kuba')`", "Hej Kuba", "code_output",
             None),
            (4, "Co wypisze kod? `def suma(a, b): return a + b`, `print(suma(3, 4))`", "7", "code_output", None),
            (4, "Co wypisze kod? `def tekst(): return 'OK'`, `print(tekst())`", "OK", "code_output", None),

            # === Moduł 5: Listy ===
            (
            5, "Utwórz listę o nazwie `liczby` zawierającą liczby 1, 2 i 3.", "liczby = [1, 2, 3]", "code_input", None),
            (5, "Masz listę `liczby = [1, 2, 3]`. Dodaj do niej element 4 **na koniec**.",
             "liczby = [1, 2, 3]\nliczby.append(4)", "code_input", None),
            (5, "Utwórz **pustą** listę o nazwie `dane`.", "dane = []", "code_input", None),
            (5,
             "Masz listę `elementy = [5, 10, 15]`. Używając pętli `for`, wypisz **każdy element** tej listy w osobnej linii.",
             "elementy = [5, 10, 15]\nfor x in elementy:\n    print(x)", "code_input", None),
            (5, "Co wypisze kod? `lista = [1, 2, 3]`, `print(lista[0])`", "A", "multiple_choice",
             ["A: 1", "B: 2", "C: 0", "D: Błąd"]),
            (5, "Jak dodać element 99 na **koniec** listy `dane`?", "C", "multiple_choice",
             ["A: dane = dane + 99", "B: dane.insert(99)", "C: dane.append(99)", "D: add(dane, 99)"]),
            (5, "Jak usunąć **pierwsze wystąpienie** elementu o wartości 2 z listy `lista`?", "B", "multiple_choice",
             ["A: remove(lista, 2)", "B: lista.remove(2)", "C: del lista[2]", "D: lista.delete(2)"]),
            (5, "Co wypisze kod? `dane = [10, 20, 30]`, `print(len(dane))`", "C", "multiple_choice",
             ["A: 30", "B: 0", "C: 3", "D: Błąd"]),
            (5, "Ułóż kod: 1. stwórz listę `imiona` z 'Ala', 'Jan', 2. pętlą `for` wypisz każde `imie`.",
             "imiona = ['Ala', 'Jan']\nfor imie in imiona:\n    print(imie)", "reorder",
             ["    print(imie)", "for imie in imiona:", "imiona = ['Ala', 'Jan']"]),
            (5, "Ułóż kod: 1. stwórz pustą listę `liczby`, 2. dodaj do niej 5 (`append`), 3. wypisz `liczby`.",
             "liczby = []\nliczby.append(5)\nprint(liczby)", "reorder",
             ["liczby = []", "liczby.append(5)", "print(liczby)"]),
            (5, "Ułóż kod: 1. `lista = [3, 6]`, 2. dla każdego `x` w `lista`, 3. jeśli `x > 4`, 4. wypisz `x`.",
             "lista = [3, 6]\nfor x in lista:\n    if x > 4:\n        print(x)", "reorder",
             ["for x in lista:", "    if x > 4:", "        print(x)", "lista = [3, 6]"]),
            (5, "Ułóż kod: 1. pętla `for i` od 0 do 4, 2. wypisz kwadrat `i` (`i**2`).",
             "for i in range(5):\n    print(i ** 2)", "reorder", ["    print(i ** 2)", "for i in range(5):"]),
            (5, "Co wypisze kod? `lista = [1, 2, 3]`, `print(len(lista))`", "3", "code_output", None),
            (5, "Co wypisze kod? `x = [2, 4]`, `x.append(6)`, `print(x)`", "[2, 4, 6]", "code_output", None),
            (5, "Co wypisze kod? `for i in [3, 5]: print(i * 2)`", "6\n10", "code_output", None),
            (5, "Co wypisze kod? `lista = [7, 8]`, `print(lista[1])`", "8", "code_output", None)
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



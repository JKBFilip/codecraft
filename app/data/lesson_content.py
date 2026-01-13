# ===================================================================
# ===               ZADANIA PROGRAMISTY (WYZWANIA)                ===
# ===================================================================

PROGRAMMER_TASKS = {
    1: {
        "instruction": """
            <h2>Zadanie Programisty: Przelicznik Odległości 📏</h2>
            Napisz program, który:
            <ol>
                <li>Zapyta użytkownika o odległość w kilometrach (może być liczba z przecinkiem) za pomocą funkcji `input()`.</li>
                <li>Przechowa tę wartość w zmiennej o nazwie `kilometry_str`.</li>
                <li>Przekonwertuje wartość ze zmiennej `kilometry_str` na liczbę zmiennoprzecinkową (float) i zapisze ją w zmiennej `kilometry_liczba`.</li>
                <li>Wiedząc, że <b>1 kilometr to około 0.621371 mili</b>, obliczy odległość w milach i zapisze ją w zmiennej `mile`.</li>
                <li>Wypisze wynik w formacie: "X kilometrów to Y mil." (użyj f-stringa do wyświetlenia wartości zmiennych `kilometry_liczba` i `mile`).</li>
            </ol>
            <b>Wskazówka:</b> Pamiętaj o użyciu funkcji `float()` do konwersji i odpowiednich nazwach zmiennych.
            """,
        "solution": """
# Współczynnik przeliczeniowy
przelicznik_km_na_mile = 0.621371

# Zapytaj użytkownika o odległość w km
kilometry_str = input("Podaj odległość w kilometrach: ")

# Przekonwertuj tekst na liczbę zmiennoprzecinkową
kilometry_liczba = float(kilometry_str)

# Oblicz odległość w milach
mile = kilometry_liczba * przelicznik_km_na_mile

# Wypisz wynik
print(f"{kilometry_liczba} kilometrów to {mile} mil.")
"""
    },
    2: {
        "instruction": """
        <h2>Zadanie Programisty: Prosty System Oceniania 🎓</h2>
        Napisz program, który:
        <ol>
            <li>Poprosi użytkownika o podanie liczby punktów z testu (0-100) za pomocą `input()`.</li>
            <li>Na podstawie liczby punktów wystawi ocenę słowną według skali:
                <ul>
                    <li>90-100: Bardzo dobry</li>
                    <li>70-89: Dobry</li>
                    <li>50-69: Dostateczny</li>
                    <li>Poniżej 50: Niedostateczny</li>
                </ul>
            </li>
            <li>Wypisze uzyskaną ocenę.</li>
            <li>Obsłuży sytuację, gdy użytkownik poda liczbę spoza zakresu 0-100 (wypisze błąd).</li>
        </ol>
        <b>Wskazówka:</b> Użyj zagnieżdżonych `if/elif/else` oraz operatorów porównania. Pamiętaj o konwersji `input()` na `int()`.
        """,
        "solution": """
punkty_str = input("Podaj liczbę punktów (0-100): ")
punkty = int(punkty_str)

if punkty < 0 or punkty > 100:
    print("Błąd: Liczba punktów musi być w zakresie 0-100.")
elif punkty >= 90:
    print("Ocena: Bardzo dobry")
elif punkty >= 70:
    print("Ocena: Dobry")
elif punkty >= 50:
    print("Ocena: Dostateczny")
else:
    print("Ocena: Niedostateczny")
"""
    },
    3: {
        "instruction": "<h2>Zadanie Programisty: Tabliczka Mnożenia ✖️</h2>Napisz program używający zagnieżdżonych pętli `for`, który wypisze tabliczkę mnożenia od 1 do 5 (każdy wynik w osobnym `print`).",
        "solution": "for i in range(1, 6):\n    for j in range(1, 6):\n        print(f'{i} * {j} = {i*j}')\n    print('-'*10) # Separator"
    },
    4: {
        "instruction": """
        <h2>Zadanie Programisty: Funkcja Silnia !</h2>
        Napisz funkcję o nazwie `silnia`, która:
        <ol>
            <li>Przyjmuje jeden argument `n` (liczbę całkowitą).</li>
            <li>Oblicza silnię liczby `n` (n! = 1 * 2 * ... * n).</li>
            <li><b>Zwraca</b> obliczoną wartość.</li>
            <li>Jeśli `n` jest mniejsze od 0, funkcja powinna zwrócić `None`.</li>
            <li>Pamiętaj, że silnia z 0 (0!) wynosi 1.</li>
        </ol>
        <b>Poza funkcją:</b>
        <ul>
            <li>Wywołaj funkcję `silnia` dla `n = 5`.</li>
            <li>Wypisz wynik na ekranie.</li>
        </ul>
        """,
        "solution": """
def silnia(n):
    if n < 0:
        return None
    if n == 0:
        return 1

    wynik = 1
    for i in range(1, n + 1):
        wynik = wynik * i

    return wynik

liczba = 5
wynik_silni = silnia(liczba)

if wynik_silni is not None:
    print(f"Silnia z {liczba} wynosi: {wynik_silni}")
else:
    print("Nie można obliczyć silni dla liczby ujemnej.")
"""
    },
    5: {
        "instruction": "<h2>Zadanie Programisty: Statystyki Listy 📊</h2>Napisz funkcję `statystyki(lista)`, która przyjmuje listę liczb i **zwraca** słownik zawierający trzy klucze: 'min' (najmniejsza wartość), 'max' (największa wartość) i 'srednia' (średnia arytmetyczna). Przetestuj funkcję na liście `[3, 1, 4, 1, 5, 9, 2]`.",
        "solution": "def statystyki(lista):\n    if not lista:\n        return {'min': None, 'max': None, 'srednia': None}\n    return {\n        'min': min(lista),\n        'max': max(lista),\n        'srednia': sum(lista) / len(lista)\n    }\n\ndane = [3, 1, 4, 1, 5, 9, 2]\nprint(statystyki(dane))"
    }
}


def get_programmer_task(lesson_index):
    """Zwraca dane zadania programisty dla danego modułu."""
    return PROGRAMMER_TASKS.get(lesson_index, {"instruction": "Brak zadania.", "solution": ""})


# ===================================================================
# ===                TREŚCI EDUKACYJNE (TEORIA)                   ===
# ===================================================================
# Importy widgetów gier są tutaj potrzebne, aby zwrócić instancję widgetu
from app.views.games.variable_box_game import VariableGameWidget
from app.views.games.conditional_sorter_game import ConditionalSorterGame
from app.views.games.loop_garden_game import LoopGardenGame
from app.views.games.function_pizza_game import FunctionPizzaGame
from app.views.games.list_train_game import ListTrainGame


def get_lesson_data(lesson_index):
    """Zwraca listę stron (słowników) dla danego modułu."""

    # --- MODUŁ 1: Podstawy ---
    if lesson_index == 1:
        return [
            # Strona 0: Mini-Gra
            {
                "type": "widget",
                "content": VariableGameWidget()
            },
            # Strony tekstowe
            {
                "type": "html",
                "content": """
                <h2>Co to są zmienne? 📦</h2>
                Wyobraź sobie, że zmienna to <b>pudełko z etykietą</b>, do którego możesz włożyć jakąś informację. 
                Dzięki etykiecie (nazwie zmiennej) możesz łatwo odnaleźć tę informację w przyszłości.
                <br><br>
                W Pythonie, aby stworzyć zmienną, wystarczy nadać jej nazwę i przypisać wartość za pomocą znaku <b>=</b>.
                <pre><code># Tworzymy zmienną o nazwie 'wiek' i wkładamy do niej liczbę 25
wiek = 25

# Tworzymy zmienną 'imie' i wkładamy do niej tekst "Ala"
imie = "Ala"</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Typy danych</h2>
                Python automatycznie rozpoznaje, co wkładasz do "pudełka". Najważniejsze typy to:
                <ul>
                    <li><b>int</b> (integer) - liczby całkowite, np. <code>10</code>, <code>-5</code>, <code>0</code></li>
                    <li><b>float</b> - liczby zmiennoprzecinkowe, np. <code>3.14</code>, <code>-0.5</code></li>
                    <li><b>str</b> (string) - tekst, zawsze w cudzysłowach, np. <code>"Cześć"</code> lub <code>'Python'</code></li>
                    <li><b>bool</b> (boolean) - wartość prawda/fałsz, tylko <code>True</code> lub <code>False</code></li>
                </ul>
                <pre><code># Przykłady różnych typów
liczba_uczniow = 20      # to jest int
srednia_ocen = 4.5       # to jest float
nazwa_szkoly = "CodeCraft" # to jest str
czy_zaliczone = True     # to jest bool</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Dobre i złe nazwy zmiennych ✅❌</h2>
                Nazwy zmiennych muszą przestrzegać kilku zasad:
                <ul>
                    <li>Muszą zaczynać się od litery lub znaku podkreślenia `_`.</li>
                    <li>Nie mogą zaczynać się od cyfry.</li>
                    <li>Mogą zawierać tylko litery, cyfry i znak podkreślenia.</li>
                    <li>Nie mogą zawierać spacji (używaj `_`, np. `liczba_punktow`).</li>
                    <li>Wielkość liter ma znaczenie (`imie` to inna zmienna niż `Imie`).</li>
                </ul>
                <pre><code># ✅ Poprawne nazwy:
moja_zmienna = 1
punkty_gracza_1 = 100
_sekretny_kod = "tajne"

# ❌ Niepoprawne nazwy:
1_gracz = "Kuba"   # Zaczyna się od cyfry
moja zmienna = 2 # Zawiera spację
twoja-zmienna = 3 # Zawiera niedozwolony znak '-'</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Operacje na zmiennych ⚙️</h2>
                Gdy masz już dane w zmiennych, możesz wykonywać na nich różne operacje.
                <br><br>
                Możesz też "nadpisać" wartość zmiennej, przypisując jej nową.
                <pre><code>a = 10
b = 5
suma = a + b  # W zmiennej 'suma' będzie teraz 15
print(suma)

# Nadpisywanie zmiennej
punkty = 100
punkty = punkty + 50 # Bierzemy starą wartość (100), dodajemy 50 i zapisujemy
print(punkty)      # Wypisze 150</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Rozmowa z programem: funkcja `input()` 🗣️</h2>
                Programy często potrzebują danych od użytkownika. Służy do tego funkcja <b>`input()`</b>.
                Wyświetla ona podany tekst (tzw. "prompt") i czeka, aż użytkownik coś wpisze i naciśnie Enter.
                <br><br>
                <b>Ważne:</b> `input()` <u>zawsze</u> zwraca tekst (string, `str`), nawet jeśli użytkownik wpisze cyfry!
                <pre><code># Program zapyta "Jak masz na imię? " i zapisze odpowiedź w zmiennej 'odpowiedz'
odpowiedz = input("Jak masz na imię? ")
print(f"Cześć, {odpowiedz}!")

# Program zapyta o wiek, ale zapisze go jako TEKST
wiek_tekst = input("Ile masz lat? ") 
# Próba dodania liczby do tekstu spowoduje błąd!
# print(wiek_tekst + 1) # <-- BŁĄD TypeError
</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Zmiana typu danych: `int()`, `float()`, `str()` ⚙️➡️🔢</h2>
                Skoro `input()` zwraca tekst, a my często potrzebujemy liczb, musimy nauczyć się **konwertować** (zmieniać) typy danych.
                <ul>
                    <li><code>int(wartosc)</code>: Zamienia `wartosc` na liczbę całkowitą (integer).</li>
                    <li><code>float(wartosc)</code>: Zamienia `wartosc` na liczbę zmiennoprzecinkową (float).</li>
                    <li><code>str(wartosc)</code>: Zamienia `wartosc` na tekst (string).</li>
                </ul>
                <pre><code>wiek_tekst = input("Ile masz lat? ") 
# Konwertujemy tekst na liczbę całkowitą
wiek_liczba = int(wiek_tekst) 
# Teraz możemy wykonywać obliczenia!
print(f"Za rok będziesz mieć {wiek_liczba + 1} lat.")

liczba_z_tekstu = "3.14"
liczba_float = float(liczba_z_tekstu)
print(liczba_float * 2) # Wypisze 6.28

liczba = 100
tekst_z_liczby = str(liczba)
print("Twoja liczba to: " + tekst_z_liczby)
</code></pre>
                """
            }
        ]

    # --- MODUŁ 2: Warunki ---
    elif lesson_index == 2:
        return [
            {"type": "widget", "content": ConditionalSorterGame()},
            {
                "type": "html",
                "content": """
                <h2>Instrukcje warunkowe: `if` 🤔</h2>
                Programy często muszą podejmować decyzje. Do tego służą instrukcje warunkowe. 
                Najważniejszą z nich jest <b>`if`</b> (jeśli). Działa ona prosto:
                <br><br>
                <b>Jeśli</b> warunek jest prawdziwy (<code>True</code>), <b>wykonaj</b> kod, który znajduje się we wcięciu.
                <pre><code>temperatura = 25

# Sprawdzamy, czy temperatura jest większa niż 20
if temperatura > 20:
    print("Jest ciepło! Można iść na spacer.")

# Ten kod wykona się zawsze, bo nie jest we wcięciu
print("Koniec programu.")</code></pre>
                Jeśli `temperatura` byłaby równa 15, napis "Jest ciepło!" by się nie pojawił.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>A co, jeśli nie? Użyj `else` 🤷</h2>
                Często chcemy, aby program wykonał alternatywną akcję, gdy warunek `if` jest fałszywy (<code>False</code>).
                Do tego służy słowo kluczowe <b>`else`</b> (w przeciwnym razie).
                <pre><code>wiek = 16

if wiek >= 18:
    print("Jesteś osobą dorosłą.")
else:
    print("Jesteś osobą niepełnoletnią.")</code></pre>
                <b>Ważne:</b> `else` nie ma własnego warunku. Wykonuje się zawsze, gdy `if` nad nim nie został spełniony.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Wiele możliwości: `elif` 🚦</h2>
                Czasami mamy więcej niż dwie opcje do sprawdzenia. Zamiast pisać wiele zagnieżdżonych `if`-ów, używamy <b>`elif`</b> (skrót od "else if").
                <br><br>
                Python sprawdza warunki po kolei: najpierw `if`, potem każdy `elif`. Wykona kod dla <b>pierwszego prawdziwego warunku</b> i pominie resztę.
                <pre><code>ocena = 4

if ocena == 6:
    print("Celujący!")
elif ocena == 5:
    print("Bardzo dobry!")
elif ocena >= 3:
    print("Zaliczone.")
else:
    print("Niezaliczone, spróbuj ponownie.")</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Operatory porównania ⚖️</h2>
                Do tworzenia warunków potrzebujesz operatorów, które porównują wartości. Oto najważniejsze z nich:
                <ul>
                    <li><code>==</code> &nbsp; czy równe?</li>
                    <li><code>!=</code> &nbsp; czy różne?</li>
                    <li><code>></code> &nbsp;  czy większe?</li>
                    <li><code><</code> &nbsp;  czy mniejsze?</li>
                    <li><code>>=</code> &nbsp; czy większe lub równe?</li>
                    <li><code><=</code> &nbsp; czy mniejsze lub równe?</li>
                </ul>
                <pre><code>liczba = 10

if liczba != 0:
    print("Liczba jest różna od zera.")

if liczba > 5:
    print("Liczba jest większa od 5.")</code></pre>
                Świetnie! Potrafisz już sterować przepływem programu. Przejdź do zadań, aby to przećwiczyć.
                """
            }
        ]

    # --- MODUŁ 3: Pętle ---
    elif lesson_index == 3:
        return [
            {"type": "widget", "content": LoopGardenGame()},
            {
                "type": "html",
                "content": """
                <h2>Pętle: Po co powtarzać? 🔁</h2>
                Pętle pozwalają na wielokrotne wykonywanie tego samego bloku kodu bez potrzeby jego kopiowania. To jedno z najpotężniejszych narzędzi w programowaniu!
                <br><br>
                Wyobraź sobie, że masz wypisać liczby od 1 do 5. Zamiast pisać 5 linijek `print()`, możesz użyć pętli.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Pętla `for` - powtórz określoną liczbę razy</h2>
                Pętla <b>`for`</b> jest idealna, gdy wiesz dokładnie, ile razy chcesz coś powtórzyć. Najczęściej używa się jej z funkcją `range()`.
                <br><br>
                `range(5)` generuje liczby od 0 do 4 (łącznie 5 liczb).
                <pre><code># Wypisz "Cześć" 3 razy
for i in range(3):
    print("Cześć!")

# Wypisz liczby od 0 do 4
for liczba in range(5):
    print(liczba)</code></pre>
                Zmienna `i` lub `liczba` w każdym "obrocie" pętli przechowuje kolejną wartość z `range()`.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Pętla `while` - powtarzaj, dopóki...</h2>
                Pętla <b>`while`</b> (dopóki) wykonuje kod tak długo, jak jej warunek jest prawdziwy (<code>True</code>).
                <br><br>
                Jest przydatna, gdy nie wiesz, ile dokładnie powtórzeń będzie potrzebnych.
                <pre><code>licznik = 0

while licznik < 3:
    print(f"Licznik ma wartość: {licznik}")
    # WAŻNE: musimy zmieniać zmienną z warunku!
    licznik = licznik + 1 

print("Koniec pętli.")</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Uwaga na nieskończone pętle! ♾️</h2>
                Najczęstszy błąd przy pętli `while` to zapomnienie o zmianie wartości, od której zależy warunek. Prowadzi to do pętli, która nigdy się nie kończy.
                <pre><code># ❌ ZŁY KOD - TA PĘTLA DZIAŁA WIECZNIE!
# Warunek "True" jest zawsze prawdziwy
while True:
    print("To się nigdy nie skończy!")

# ❌ ZŁY KOD - ZAPOMNIANO O `i = i + 1`
i = 0
while i < 5:
    print("Nieskończoność...")</code></pre>
                Jeśli Twój program się zawiesi, to prawdopodobnie przez taką pętlę!
                <br><br>
                Opanowałeś pętle! Czas wykorzystać je w praktyce.
                """
            }
        ]

    # --- MODUŁ 4: Funkcje ---
    elif lesson_index == 4:
        return [
            {"type": "widget", "content": FunctionPizzaGame()},
            {
                "type": "html",
                "content": """
                <h2>Funkcje: Twoje własne narzędzia 🔧</h2>
                Funkcja to nazwany blok kodu, który wykonuje określone zadanie. Możesz go "wywołać" (uruchomić) w dowolnym momencie, podając jego nazwę.
                <br><br>
                Główna zaleta? <b>Unikasz powtarzania kodu!</b> Jeśli masz fragment, który pojawia się w wielu miejscach, zamknij go w funkcji.
                <br><br>
                Funkcję tworzymy za pomocą słowa kluczowego <b>`def`</b>.
                <pre><code># Definicja (stworzenie) funkcji
def przywitaj_sie():
    print("Cześć!")
    print("Miło mi Cię poznać.")

# Wywołanie (użycie) funkcji
przywitaj_sie()
przywitaj_sie()</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Argumenty: Przekazywanie danych do funkcji</h2>
                Funkcje mogą przyjmować dane z zewnątrz. Te dane nazywamy <b>argumentami</b> (lub parametrami).
                <br><br>
                Dzięki nim funkcja staje się bardziej elastyczna.
                <pre><code># Funkcja 'przywitaj' oczekuje jednego argumentu: 'imie'
def przywitaj(imie):
    print(f"Cześć, {imie}!")

# Wywołujemy funkcję, przekazując jej konkretne dane
przywitaj("Anna")
przywitaj("Piotr")</code></pre>
                Możesz przekazywać wiele argumentów, oddzielając je przecinkami.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>`return`: Zwracanie wyniku z funkcji</h2>
                Funkcje mogą nie tylko coś robić (np. drukować tekst), ale też <b>zwracać wynik</b> swoich obliczeń. Służy do tego instrukcja <b>`return`</b>.
                <br><br>
                Gdy funkcja coś zwraca, możemy przypisać ten wynik do zmiennej.
                <pre><code># Ta funkcja oblicza sumę i ją ZWRACA
def dodaj(a, b):
    wynik_dodawania = a + b
    return wynik_dodawania

# Wywołujemy funkcję i łapiemy jej wynik do zmiennej
suma = dodaj(5, 3)
print(suma)  # Wypisze 8

# Można też użyć wyniku bezpośrednio
print(dodaj(10, 20)) # Wypisze 30</code></pre>
                Instrukcja `return` natychmiast kończy działanie funkcji.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Po co to wszystko? Przykład</h2>
                Połączenie argumentów i `return` tworzy potężne, uniwersalne narzędzia.
                <pre><code>def oblicz_pole_prostokata(dlugosc, szerokosc):
    if dlugosc <= 0 or szerokosc <= 0:
        return 0 # Zwracamy 0 dla błędnych danych

    pole = dlugosc * szerokosc
    return pole

# Używamy naszej funkcji wielokrotnie
pole1 = oblicz_pole_prostokata(10, 5)
pole2 = oblicz_pole_prostokata(7, 3)

print(f"Pole pierwszego prostokąta: {pole1}")
print(f"Pole drugiego prostokąta: {pole2}")</code></pre>
                Jesteś gotów, aby zacząć pisać własne funkcje. Do dzieła!
                """
            }
        ]

    # --- MODUŁ 5: Listy ---
    elif lesson_index == 5:
        return [
            {"type": "widget", "content": ListTrainGame()},
            {
                "type": "html",
                "content": """
                <h2>Listy: Twoja kolekcja danych 📚</h2>
                Do tej pory zmienna przechowywała jedną wartość (np. jedną liczbę lub jeden tekst). <b>Lista</b> to specjalny typ zmiennej, która może przechowywać <b>wiele wartości</b> w uporządkowanej kolejności.
                <br><br>
                Listy tworzymy za pomocą nawiasów kwadratowych <code>[]</code>, a elementy oddzielamy przecinkami.
                <pre><code># Pusta lista
pusta_lista = []

# Lista liczb
liczby = [1, 2, 3, 5, 8]

# Lista tekstów
owoce = ["jabłko", "banan", "gruszka"]

# Lista może zawierać różne typy danych
rozne_rzeczy = [10, "napis", True, 3.14]</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Dostęp do elementów: Indeksy</h2>
                Każdy element w liście ma swoją pozycję, zwaną <b>indeksem</b>.
                <br><br>
                <b>Najważniejsza zasada:</b> indeksowanie w Pythonie zaczyna się od <b>0</b>! Pierwszy element ma indeks 0, drugi ma indeks 1, i tak dalej.
                <pre><code>owoce = ["jabłko", "banan", "gruszka"]

# Dostęp do pierwszego elementu (indeks 0)
pierwszy_owoc = owoce[0]
print(pierwszy_owoc)  # Wypisze "jabłko"

# Dostęp do trzeciego elementu (indeks 2)
trzeci_owoc = owoce[2]
print(trzeci_owoc)   # Wypisze "gruszka"</code></pre>
                Próba dostępu do nieistniejącego indeksu (np. `owoce[3]`) spowoduje błąd.
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Modyfikacja list ✏️</h2>
                Listy są "mutowalne", co oznacza, że możemy je zmieniać po utworzeniu: dodawać, usuwać i modyfikować elementy.
                <ul>
                    <li><code>nazwa_listy.append(element)</code> - dodaje element na końcu listy.</li>
                    <li><code>nazwa_listy[indeks] = nowa_wartosc</code> - podmienia element na danej pozycji.</li>
                    <li><code>del nazwa_listy[indeks]</code> - usuwa element o danym indeksie.</li>
                </ul>
                <pre><code>kolory = ["czerwony", "zielony"]

# Dodajemy nowy kolor
kolory.append("niebieski")
print(kolory)  # ["czerwony", "zielony", "niebieski"]

# Zmieniamy pierwszy element
kolory[0] = "fioletowy"
print(kolory)  # ["fioletowy", "zielony", "niebieski"]

# Usuwamy drugi element
del kolory[1]
print(kolory)  # ["fioletowy", "niebieski"]</code></pre>
                """
            },
            {
                "type": "html",
                "content": """
                <h2>Pętla `for` i listy: Idealna para 🤝</h2>
                Najczęstszym sposobem pracy z listami jest przeglądanie ich wszystkich elementów za pomocą pętli `for`.
                <pre><code>zakupy = ["chleb", "mleko", "jajka"]

print("Lista zakupów:")
for produkt in zakupy:
    # W każdej iteracji zmienna 'produkt' przyjmuje kolejną wartość z listy
    print(f"- {produkt}")

# Przykład z liczbami
liczby = [10, 20, 30]
suma = 0
for liczba in liczby:
    suma = suma + liczba

print(f"Suma liczb: {suma}") # Wypisze 60</code></pre>
                Gratulacje! Listy to kluczowy element Pythona. Czas sprawdzić swoją wiedzę w zadaniach.
                """
            }
        ]
    else:
        return [{"type": "html", "content": "<h1>Brak teorii dla tego modułu</h1>"}]
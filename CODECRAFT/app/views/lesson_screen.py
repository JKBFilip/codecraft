from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt

class LessonScreen(QWidget):
    def __init__(self, main_window, lesson_index):
        super().__init__()
        self.main_window = main_window
        self.lesson_index = lesson_index
        self.page = 0
        self.theory_pages = self.get_theory_pages(lesson_index)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("\U0001F4D8 Lekcja")
        self.title_label.setStyleSheet("font-size: 18pt; font-weight: bold")
        layout.addWidget(self.title_label)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.prev_button = QPushButton("← Poprzednia strona")
        self.prev_button.clicked.connect(self.prev_page)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Następna strona →")
        self.next_button.clicked.connect(self.next_page)
        layout.addWidget(self.next_button)

        self.task_button = QPushButton("Przejdź do zadań")
        self.task_button.clicked.connect(lambda: self.main_window.show_task())
        layout.addWidget(self.task_button)

        self.menu_button = QPushButton("Powrót do menu")
        self.menu_button.clicked.connect(self.back_to_menu)
        layout.addWidget(self.menu_button)

        self.test_button = QPushButton("Rozpocznij test końcowy")
        self.test_button.clicked.connect(lambda: self.main_window.start_final_test())
        layout.addWidget(self.test_button)

        self.setLayout(layout)
        self.update_page()

    def update_page(self):
        self.text_edit.setPlainText(self.theory_pages[self.page])
        self.prev_button.setEnabled(self.page > 0)
        self.next_button.setEnabled(self.page < len(self.theory_pages) - 1)

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.update_page()

    def next_page(self):
        if self.page < len(self.theory_pages) - 1:
            self.page += 1
            self.update_page()

    def back_to_menu(self):
        self.main_window.show_menu()

    def get_theory_pages(self, lesson_index):
        if lesson_index == 1:
            return [
                "Zmienne to sposób na przechowywanie danych w programie. Przykład:\n\nwiek = 10\nimie = 'Kuba'",
                "Nazwy zmiennych nie mogą zaczynać się od cyfry i nie mogą zawierać spacji.\n\nPoprawne:\nliczba_uczniow = 20\nniepoprawne: 1liczba = 5, liczba uczniow = 20",
                "Można wykonywać operacje na zmiennych:\n\n\na = 5\nb = 3\nsuma = a + b\nprint(suma)  # wypisze 8",
                "Zmienną można nadpisać:\n\n\nx = 10\nx = x + 1\nprint(x)  # wypisze 11",
            ]
        elif lesson_index == 2:
            return [
                "Instrukcje warunkowe pozwalają podejmować decyzje w kodzie.\n\nif warunek:\n    # kod gdy warunek prawdziwy",
                "Można też dodać else:\n\nif warunek:\n    # kod gdy prawda\nelse:\n    # kod gdy fałsz",
                "Porównania w Pythonie:\n== równe\n!= różne\n<  mniejsze\n>  większe\n<= mniejsze/równe\n>= większe/równe",
                "Przykład:\n\nx = 5\nif x > 3:\n    print('Większe')\nelse:\n    print('Mniejsze lub równe')",
            ]
        elif lesson_index == 3:
            return [
                "Pętle umożliwiają wielokrotne wykonywanie kodu.\nNajczęściej używana to pętla for:",
                "Przykład:\n\nfor i in range(5):\n    print(i)\n\nWypisze liczby od 0 do 4.",
                "Pętla while działa dopóki warunek jest prawdziwy:\n\ni = 0\nwhile i < 3:\n    print(i)\n    i += 1",
                "Uważaj na pętle nieskończone!\n\nwhile True:\n    print('To się nigdy nie skończy')",
            ]
        elif lesson_index == 4:
            return [
                "Funkcje pozwalają grupować kod i wielokrotnie go używać. Tworzymy je za pomocą `def`:\n\ndef przywitaj():\n    print('Cześć!')",
                "Aby uruchomić funkcję, wystarczy ją wywołać:\n\nprzywitaj()",
                "Funkcje mogą mieć argumenty:\n\ndef dodaj(a, b):\n    print(a + b)\n\ndodaj(2, 3)  # wypisze 5",
                "Funkcje mogą też zwracać wartość:\n\ndef pomnoz(a, b):\n    return a * b\n\nwynik = pomnoz(2, 4)\nprint(wynik)  # wypisze 8",
            ]
        elif lesson_index == 5:
            return [
            "Listy w Pythonie to uporządkowane zbiory danych. Tworzy się je za pomocą nawiasów kwadratowych:\n\nowoce = ['jabłko', 'banan', 'gruszka']",
            "Do elementów listy można się odwołać za pomocą indeksów:\n\nprint(owoce[0])  # jabłko\nprint(owoce[1])  # banan",
            "Listy można modyfikować:\n\nowoce.append('śliwka')  # dodaje element\nowoce[1] = 'malina'  # zmienia element",
            "Listy można też przeglądać w pętli:\n\nfor owoc in owoce:\n    print(owoc)",
        ]

        else:
            return ["Brak teorii dla tego modułu"]

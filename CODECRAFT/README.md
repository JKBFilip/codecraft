# 📘 CODECRAFT

**CODECRAFT** to interaktywna aplikacja desktopowa do nauki podstaw programowania w języku Python. Projekt został zrealizowany w ramach pracy inżynierskiej na Uniwersytecie Warmińsko-Mazurskim.

Aplikacja łączy ustrukturyzowaną wiedzę teoretyczną z praktycznymi zadaniami oraz zaawansowanym systemem **grywalizacji** (XP, poziomy, osiągnięcia), aby zwiększyć zaangażowanie i motywację użytkownika, przeciwdziałając zjawisku rezygnacji z nauki.

---

## 🚀 Główne Funkcjonalności

### 🎓 Moduły Edukacyjne
Aplikacja oferuje kompletną ścieżkę nauki podzieloną na 5 głównych modułów:
1.  **Podstawy:** Zmienne i typy danych.
2.  **Decyzje:** Instrukcje warunkowe (`if`/`else`).
3.  **Powtórzenia:** Pętle (`for`, `while`).
4.  **Organizacja:** Funkcje i ich parametry.
5.  **Kolekcje:** Listy i operacje na nich.

### 🎮 System Grywalizacji
* **Punkty XP i Poziomy:** Użytkownik zdobywa punkty za każdą aktywność, awansując na kolejne poziomy zaawansowania.
* **System Osiągnięć:** Rozbudowany system odznak (w tym osiągnięcia ukryte) nagradzający specyficzne zachowania (np. "Speedrunner", "Perfekcjonista").

### 📝 Interaktywne Zadania
Różnorodne typy zadań sprawdzające wiedzę w praktyce:
* **Code Input:** Pisanie kodu weryfikowane przez analizę drzewa składniowego (AST) – odporne na różnice w formatowaniu.
* **Code Output:** Przewidywanie wyniku działania programu.
* **Multiple Choice:** Zadania wielokrotnego wyboru.
* **Reorder:** Układanie fragmentów kodu w poprawnej kolejności logicznej.
* **Wyzwania Koderskie:** Złożone zadania projektowe do wykonania w zewnętrznym edytorze (np. "Kalkulator wieku psa").

### ✅ Weryfikacja Wiedzy
* **Testy Modułowe:** Sprawdziany kończące każdy rozdział (wymagany próg 80%).
* **Egzamin Końcowy:** Przekrojowy test z całości materiału (20 losowych pytań, limit czasu).
* **Certyfikat:** Automatyczne generowanie imiennego certyfikatu ukończenia kursu (PNG).

---

## 🛠️ Technologie

Projekt został zrealizowany przy użyciu nowoczesnego stosu technologicznego:

* **Język:** Python 3.13
* **GUI Framework:** PySide6 (Qt for Python) – zapewnia nowoczesny, responsywny interfejs.
* **Przechowywanie danych:** JSON – lokalny system zapisu postępów, kont i osiągnięć (brak zewnętrznej bazy danych SQL).
* **Analiza kodu:** Moduł `ast` (Abstract Syntax Tree) do inteligentnej weryfikacji rozwiązań użytkownika.
* **Generowanie grafik:** Moduł `QPainter` do dynamicznego tworzenia certyfikatów.

---

## 📂 Struktura Projektu

```text
CODECRAFT/
│
├── app/
│   ├── assets/             # Zasoby statyczne (style QSS, ikony)
│   ├── features/           # Logika biznesowa (system osiągnięć)
│   ├── models/             # Modele danych (użytkownik, zadania)
│   │   ├── auth/           # Logika logowania i rejestracji
│   │   └── task.py         # Klasa reprezentująca zadanie
│   ├── views/              # Warstwa wizualna (ekrany aplikacji)
│   │   ├── auth/           # Ekrany logowania/rejestracji/resetu
│   │   ├── menu_screen.py  # Główne menu z wyborem modułów
│   │   ├── lesson_screen.py# Ekran teorii i wyzwań
│   │   ├── task_screen.py  # Ekran rozwiązywania zadań
│   │   ├── final_exam_screen.py # Egzamin końcowy
│   │   └── achievements_screen.py # Ekran osiągnięć
│   └── widgets/            # Niestandardowe widgety (np. lista do układania)
│
├── data/                   # Lokalne pliki zapisu (tworzone automatycznie)
│   ├── accounts/           # Dane logowania (hasła hashowane SHA-256)
│   ├── achievements/       # Odblokowane osiągnięcia użytkowników
│   └── progress/           # Zapisane postępy, wyniki testów i historia
│
├── certificates/           # Folder wyjściowy dla wygenerowanych certyfikatów
├── main.py                 # Główny punkt wejścia aplikacji
└── requirements.txt        # Lista wymaganych bibliotek
````

-----

## ⚙️ Instalacja i Uruchomienie

1.  **Wymagania:** Zainstalowany Python w wersji 3.10 lub nowszej.

2.  **Instalacja zależności:**
    Otwórz terminal w folderze projektu i wpisz:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Uruchomienie:**

    ```bash
    python main.py
    ```

-----

## 🧪 Tryb Deweloperski (Kody)

W aplikacji zaimplementowano system kodów (dostępny pod ikoną 🎁 w menu głównym), ułatwiający testowanie i prezentację funkcjonalności:

  * `MAX_MODULES` – Odblokowuje wszystkie moduły i zalicza testy modułowe.
  * `MAX_ACHIEVEMENTS` – Odblokowuje wszystkie dostępne osiągnięcia.
  * `XP_BOOST_100` – Dodaje jednorazowo 100 punktów doświadczenia.

-----
## 🤖 Wykorzystanie Narzędzi AI

W procesie realizacji projektu wykorzystano wsparcie asystentów sztucznej inteligencji (**ChatGPT** oraz **Gemini AI**). Narzędzia te posłużyły jako wsparcie w:
* Generowaniu przykładowych treści zadań dydaktycznych i pytań testowych.
* Restrukturyzacji, optymalizacji i formatowaniu kodu źródłowego zgodnie z zasadami "Czystego Kodu".
## 👤 Autor

**Jakub Filipiak**

  * Nr indeksu: 169237
  * **Uniwersytet Warmińsko-Mazurski w Olsztynie**
  * Wydział Matematyki i Informatyki
  * Kierunek: Informatyka

*Projekt inżynierski 2025*

```
```
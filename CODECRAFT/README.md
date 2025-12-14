# 📘 CODECRAFT

**CODECRAFT** to nowoczesna, interaktywna aplikacja desktopowa do nauki podstaw programowania w języku **Python**, stworzona jako projekt pracy inżynierskiej na **Uniwersytecie Warmińsko-Mazurskim**.

Celem aplikacji jest skuteczne wprowadzenie początkujących użytkowników w świat programowania poprzez połączenie **klarownej teorii**, **praktycznych zadań** oraz **rozbudowanej grywalizacji**, która zwiększa motywację i ogranicza zjawisko porzucania nauki.

---

## 🚀 Kluczowe Funkcjonalności

### 🎓 Moduły Edukacyjne

CODECRAFT oferuje kompletną ścieżkę nauki składającą się z **5 głównych modułów**. Każdy z nich zawiera interaktywną mini-grę edukacyjną, wizualizującą omawiane zagadnienia:

| Moduł       | Zakres                | Mini-gra              |
| ----------- | --------------------- | --------------------- |
| Podstawy    | Zmienne i typy danych | 🧺 *Pudełko Zmiennej* |
| Decyzje     | Instrukcje warunkowe  | 📦 *Sortownia Paczek* |
| Powtórzenia | Pętle                 | 🤖 *Robot Ogrodnik*   |
| Organizacja | Funkcje               | 🍕 *Fabryka Pizzy*    |
| Kolekcje    | Listy                 | 🚆 *Pociąg*           |

---

### 🎮 Grywalizacja i Rozrywka

* **System XP i Poziomów** – użytkownik zdobywa punkty doświadczenia za każdą aktywność i awansuje na kolejne poziomy.
* **System Osiągnięć** – rozbudowany zestaw odznak (w tym osiągnięcia ukryte) nagradzający konkretne style nauki, np. *Speedrunner*, *Perfekcjonista*.
* **🕹️ Retro Konsola** – unikalny moduł z klasycznymi grami arcade napisanymi w **Pygame**:

  * Pong
  * Snake
  * Space Invaders
    Gry odblokowywane są wraz z postępami użytkownika.

---

### 📝 Interaktywne Zadania

Aplikacja wykorzystuje różnorodne typy zadań sprawdzających wiedzę w praktyce:

* **Code Input** – pisanie kodu analizowanego za pomocą drzewa składniowego (**AST**), odporne na różnice formatowania.
* **Code Output** – przewidywanie wyniku działania programu.
* **Multiple Choice** – pytania wielokrotnego wyboru.
* **Reorder** – układanie fragmentów kodu w poprawnej kolejności.

#### 💻 Wyzwania Koderskie

Rozbudowane zadania projektowe wykonywane w zewnętrznym edytorze (np. *Kalkulator wieku psa*), wzbogacone o instrukcje oraz gotowe rozwiązania.

#### 🐍 Playground

Wbudowany **interaktywny plac zabaw (sandbox)** umożliwiający swobodne pisanie i uruchamianie kodu Python w czasie rzeczywistym.

---

### ✅ Weryfikacja Wiedzy

* **Testy modułowe** – wymagany próg zaliczenia: **80%**.
* **Egzamin końcowy** – 20 losowych pytań z limitowanym czasem.
* **Certyfikat ukończenia** – automatycznie generowany imienny certyfikat (PNG) z:

  * unikalnym identyfikatorem,
  * kodem QR weryfikującym autentyczność.

---

### ♿ Dostępność i UX

* 🌓 **Tryb jasny / ciemny** – przełączany w dowolnym momencie.
* 🔊 **Syntezator mowy (TTS)** – lektor czytający treść lekcji i polecenia zadań (SAPI / WinRT).

---

## 🛠️ Technologie

Projekt został zrealizowany przy użyciu następującego stosu technologicznego:

* **Język:** Python 3.13
* **GUI:** PySide6 (Qt for Python)
* **Silnik gier:** Pygame
* **Persistencja danych:** JSON (lokalny zapis postępów)
* **Analiza kodu:** `ast` (Abstract Syntax Tree)
* **Generowanie grafiki:** QPainter, `qrcode`
* **Synteza mowy:** QTextToSpeech

---

## 📂 Struktura Projektu

```text
CODECRAFT/
│
├── app/
│   ├── assets/                 # Style QSS, ikony
│   ├── data/                   # Treści lekcji i zadania
│   ├── features/               # Logika biznesowa (osiągnięcia, XP)
│   ├── games/                  # Mini-gry edukacyjne (Qt)
│   ├── models/                 # Modele danych
│   ├── retrogames/             # Gry arcade (Pygame)
│   ├── views/                  # Ekrany aplikacji
│   │   ├── auth/
│   │   ├── retrogames_splash/
│   │   ├── menu_screen.py
│   │   ├── lesson_screen.py
│   │   ├── playground_screen.py
│   │   ├── final_exam_screen.py
│   │   └── ...
│   └── widgets/                # Niestandardowe komponenty UI
│
├── data/                       # Lokalne pliki zapisu użytkownika
├── certificates/               # Wygenerowane certyfikaty
├── tests/                      # Testy automatyczne (pytest)
├── main.py                     # Punkt wejścia aplikacji
└── requirements.txt            # Zależności
```

---

## ⚙️ Instalacja i Uruchomienie

### Wymagania

* Python **3.10+**

### Instalacja zależności

```bash
pip install -r requirements.txt
```

> Wymagane biblioteki m.in.: `PySide6`, `pygame`, `qrcode[pil]`

### Uruchomienie aplikacji

```bash
python main.py
```

---

## 📌 Informacje końcowe

CODECRAFT został zaprojektowany jako kompletne, samodzielne środowisko do nauki programowania, kładące nacisk na **praktykę**, **zaangażowanie użytkownika** oraz **wysoką jakość UX**. Projekt może stanowić solidną bazę do dalszej rozbudowy o kolejne języki programowania lub tryb online.

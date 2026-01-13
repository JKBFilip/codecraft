# 📘 CODECRAFT

**CODECRAFT** to nowoczesna, interaktywna aplikacja desktopowa do nauki podstaw programowania w języku **Python**, stworzona jako projekt pracy inżynierskiej na **Uniwersytecie Warmińsko-Mazurskim**.

Celem aplikacji jest skuteczne wprowadzenie początkujących użytkowników w świat programowania poprzez połączenie:
- klarownej teorii,
- praktycznych zadań,
- rozbudowanej **grywalizacji**, która zwiększa motywację i ogranicza zjawisko porzucania nauki.

---

## ⚠️ Uwaga techniczna (TTS)

Aplikacja korzysta z **systemowego silnika syntezy mowy** (Windows SAPI / WinRT).

> **Zalecenie:**  
> Po uruchomieniu lektora (ikona głośnika 🔊) należy poczekać do zakończenia czytania tekstu.  
> Gwałtowne przerywanie syntezy (np. szybkie przełączanie ekranów w trakcie mówienia) może w specyficznych konfiguracjach systemowych przeciążyć sterownik audio i spowodować niestabilność lub zamknięcie aplikacji.

---

## 🎁 Informacja dla testerów / recenzentów

Aby szybko przetestować wszystkie funkcjonalności aplikacji (w tym **Egzamin Końcowy** oraz **Gry Retro**) bez konieczności przechodzenia całego kursu, zaimplementowano **Kody Deweloperskie**.

**Instrukcja:**
1. Po zalogowaniu przejdź do ekranu głównego
2. Kliknij ikonę prezentu 🎁
3. Wpisz jeden z kodów:

| Kod | Działanie |
|----|----------|
| `MAX_MODULES` | Zalicza wszystkie lekcje i testy, odblokowując Egzamin Końcowy |
| `MAX_ACHIEVEMENTS` | Odblokowuje wszystkie osiągnięcia (w tym ukryte) |
| `MAX_LVL` | Przyznaje maksymalny poziom XP i odblokowuje wszystkie gry Retro |

---

## 🚀 Kluczowe funkcjonalności

### 🎓 Moduły edukacyjne

CODECRAFT oferuje kompletną ścieżkę nauki składającą się z **5 głównych modułów**. Każdy moduł zawiera interaktywną mini-grę edukacyjną wizualizującą omawiane zagadnienia.

| Moduł | Zakres | Mini-gra |
|-----|------|--------|
| Podstawy | Zmienne i typy danych | 🧺 Pudełko Zmiennej |
| Decyzje | Instrukcje warunkowe | 📦 Sortownia Paczek |
| Powtórzenia | Pętle | 🤖 Robot Ogrodnik |
| Organizacja | Funkcje | 🍕 Fabryka Pizzy |
| Kolekcje | Listy | 🚆 Pociąg |

---

### 🎮 Grywalizacja i rozrywka

- **System XP i poziomów** – zdobywanie doświadczenia za każdą aktywność
- **System osiągnięć** – rozbudowany zestaw odznak (w tym ukryte), m.in.:
  - *Speedrunner*
  - *Perfekcjonista*

#### 🕹️ Retro Konsola

Unikalny moduł z klasycznymi grami arcade napisanymi w **Pygame**:
- Pong
- Snake
- Space Invaders

Gry odblokowywane są wraz z postępami użytkownika.

---

### 📝 Interaktywne zadania

Aplikacja wykorzystuje różnorodne typy zadań sprawdzających wiedzę w praktyce:

- **Code Input** – pisanie kodu analizowanego za pomocą AST, odporne na różnice formatowania
- **Code Output** – przewidywanie wyniku działania programu
- **Multiple Choice** – pytania wielokrotnego wyboru
- **Reorder** – układanie fragmentów kodu w poprawnej kolejności

---

### 💻 Wyzwania koderskie

Rozbudowane zadania projektowe wykonywane w zewnętrznym edytorze (np. *Kalkulator wieku psa*), wzbogacone o:
- instrukcje,
- gotowe rozwiązania.

---

### 🐍 Playground

Wbudowany interaktywny **sandbox**, umożliwiający swobodne pisanie i uruchamianie kodu Python w czasie rzeczywistym.

---

### ✅ Weryfikacja wiedzy

- **Testy modułowe** – próg zaliczenia: **80%**
- **Egzamin końcowy** – 20 losowych pytań z limitem czasu
- **Certyfikat ukończenia** (PNG):
  - imienny,
  - unikalny identyfikator,
  - kod QR weryfikujący autentyczność

---

## ♿ Dostępność i UX

- 🌓 Tryb jasny / ciemny
- 🔊 Syntezator mowy (TTS – SAPI / WinRT)

---

## 🛠️ Technologie

- **Język:** Python 3.13
- **GUI:** PySide6 (Qt for Python)
- **Silnik gier:** Pygame
- **Persistencja danych:** JSON
- **Analiza kodu:** `ast`
- **Generowanie grafiki:** QPainter, qrcode
- **Synteza mowy:** QTextToSpeech

---

## 📂 Struktura projektu

```text
CODECRAFT/
│
├── app/
│   ├── assets/
│   ├── data/
│   ├── features/
│   ├── games/
│   ├── models/
│   ├── retrogames/
│   ├── views/
│   │   ├── auth/
│   │   ├── retrogames_splash/
│   │   ├── menu_screen.py
│   │   ├── lesson_screen.py
│   │   ├── playground_screen.py
│   │   ├── final_exam_screen.py
│   │   └── ...
│   └── widgets/
│
├── data/
├── certificates/
├── tests/
├── main.py
└── requirements.txt
```
## ⚙️ Instalacja i uruchomienie

### Wymagania
- Python **3.10+**

### Instalacja zależności
```bash
pip install -r requirements.txt
```
Wymagane biblioteki m.in:

- PySide6 ,pygame ,qrcode[pil]

### Uruchomienie aplikacji
```bash
python main.py
```

### 📌 Informacje końcowe
CODECRAFT został zaprojektowany jako kompletne, samodzielne środowisko do nauki programowania, kładące nacisk na praktykę, zaangażowanie użytkownika oraz wysoką jakość UX. Projekt może stanowić solidną bazę do dalszej rozbudowy o kolejne języki programowania lub tryb online.
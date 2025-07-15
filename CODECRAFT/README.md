# CODECRAFT

CODECRAFT to edukacyjna aplikacja desktopowa do nauki programowania w języku Python, która łączy teorię, praktyczne zadania oraz system testów i osiągnięć. Projekt jest zbudowany na frameworku PySide6 z pełną obsługą systemu kont użytkowników, postępów i gamifikacji.

## 📜 Główne funkcjonalności

* ✅ Logowanie i rejestracja użytkowników z systemem kont
* ✅ Lekcje teoretyczne podzielone na moduły
* ✅ Interaktywne zadania z różnymi typami odpowiedzi:

  * Wpisywanie kodu (code\_input)
  * Wybór wielokrotny (multiple\_choice)
  * Reorder – układanie kodu w poprawnej kolejności
  * Przewidywanie wyniku działania kodu (code\_output)
* ✅ Test końcowy dla każdego modułu z limitem czasu
* ✅ System osiągnięć z automatycznym odblokowywaniem i punktami doświadczenia
* ✅ Zapis i wczytywanie postępu użytkownika
* ✅ Przyjazny interfejs użytkownika z obsługą GUI (PySide6)
* ✅ Powiadomienia o nowych osiągnięciach

## 📁 Struktura projektu

```
CODECRAFT/
├── app/
│   ├── assets/                 # Style CSS do podsumowań testów
│   ├── features/               # System osiągnięć
│   ├── models/                 # Modele użytkowników, konta, zadań
│   ├── views/                  # Widoki GUI (ekrany logowania, lekcji, testów, osiągnięć)
├── data/                       # Przechowywanie danych użytkowników i postępów
├── main.py                     # Główna aplikacja PySide6
```

## 🛠️ Jak uruchomić

### 1. Klonowanie repozytorium

```bash
git clone <link_do_repozytorium>
cd CODECRAFT
```

### 2. Instalacja zależności

```bash
pip install -r requirements.txt
```

Minimalne wymagania:

* Python 3.10+
* PySide6

### 3. Uruchomienie aplikacji

```bash
python main.py
```

## 🎁 Osiągnięcia

Aplikacja zawiera gamifikację z systemem osiągnięć. Osiągnięcia przyznawane są m.in. za:

* Rozwiązanie pierwszego zadania
* Ukończenie modułu
* Perfekcyjne zaliczenie testu

Każde osiągnięcie przyznaje punkty doświadczenia, które są zapisywane dla konta użytkownika.

## 📊 Postęp i historia użytkownika

Dane użytkowników oraz ich postęp (ukończone zadania, testy, zdobyte osiągnięcia) są zapisywane lokalnie w folderze `data/`:

* `data/accounts/` — dane logowania
* `data/progress/` — postęp użytkownika
* `data/achievements/` — zdobyte osiągnięcia

## 📦 Wersja desktopowa

Całość opiera się o PySide6, dzięki czemu aplikacja działa jako klasyczna aplikacja desktopowa, bez przeglądarki.

## 💡 Przykładowe ekrany

* Ekran logowania / rejestracji
* Panel główny użytkownika
* Interaktywny moduł nauki z lekcjami i zadaniami
* Testy końcowe z limitem czasu
* Ekran osiągnięć z graficznymi odznakami

## 📌 Technologie

* Python 3.10+
* PySide6 (Qt for Python)
* JSON do przechowywania danych użytkowników
* System plików do trwałego zapisu postępów

## 📄 Licencja

Projekt edukacyjny - open source.

---

Zaprojektowane z myślą o początkujących programistach 💻🚀

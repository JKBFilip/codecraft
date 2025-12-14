import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextBrowser, QHBoxLayout, QFrame, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Ścieżka do gry: views/retrogames_splash -> views -> app -> retrogames -> pong.py
# Musimy wyjść o 3 poziomy w górę
GAME_PATH = Path(__file__).resolve().parent.parent.parent.parent / "app" / "retrogames" / "pong.py"


class PongInfoScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # --- Nagłówek ---
        title = QLabel("🏓 PONG - Legenda Gier Wideo")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("welcomeHeader")
        title.setStyleSheet("font-size: 36px; margin-bottom: 20px;")
        layout.addWidget(title)

        # --- Treść (Historia + Instrukcja) ---
        content_frame = QFrame()
        content_frame.setObjectName("formFrame")
        frame_layout = QVBoxLayout(content_frame)

        info_text = QTextBrowser()
        info_text.setOpenExternalLinks(True)
        # Używamy koloru tekstu zależnego od motywu (w CSS zdefiniujemy #infoText)
        # Tutaj inline style dla nagłówków są OK
        info_text.setHtml("""
            <h3 style="color: #6200ea;">📜 Krótka Historia</h3>
            <p>Choć wielu uważa <b>Ponga</b> za pierwszą grę wideo, historia jest nieco bardziej skomplikowana!</p>
            <ul>
                <li><b>1958:</b> William Higinbotham tworzy <i>Tennis for Two</i> na... <b>ekranie oscyloskopu</b>! To był prawdziwy przodek Ponga.</li>
                <li><b>1972:</b> Firma <b>Atari</b> (założona przez Nolana Bushnella) wypuszcza Ponga jako automat do gier (arcade). Gra stała się globalnym fenomenem.</li>
            </ul>
            <p>Ciekawostka: Pierwszy prototyp automatu w barze przestał działać następnego dnia, bo wrzutnia monet <b>przepełniła się od nadmiaru ćwierćdolarówek!</b> 💰</p>

            <hr>

            <h3 style="color: #ff9800;">🎮 Jak grać?</h3>
            <p><b>Cel:</b> Odbijaj piłkę paletką, aby przeciwnik (komputer) nie mógł jej odebrać.</p>
            <p><b>Sterowanie:</b></p>
            <ul>
                <li>Strzałka W GÓRĘ / W DÓŁ (lub klawisze W / S).</li>
            </ul>
            <p><b>Zasady:</b></p>
            <ul>
                <li>Każde odbicie lekko przyspiesza piłkę!</li>
                <li>Gra toczy się bez limitu punktów (tryb Arcade).</li>
            </ul>
        """)
        info_text.setStyleSheet("background-color: transparent; border: none; font-size: 16px;")

        frame_layout.addWidget(info_text)
        layout.addWidget(content_frame)

        # --- Przyciski ---
        buttons_layout = QHBoxLayout()

        back_btn = QPushButton("🔙 Wróć do konsoli")
        back_btn.setObjectName("secondaryButton")
        back_btn.setMinimumHeight(50)
        back_btn.clicked.connect(self.go_back)

        play_btn = QPushButton("🕹️ URUCHOM GRĘ")
        play_btn.setObjectName("primaryButton")
        play_btn.setMinimumHeight(60)
        play_btn.setMinimumWidth(250)
        play_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        play_btn.setCursor(Qt.PointingHandCursor)
        play_btn.clicked.connect(self.run_game)

        buttons_layout.addWidget(back_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(play_btn)

        layout.addLayout(buttons_layout)

    def run_game(self):
        """Uruchamia proces z grą Pygame."""
        if not GAME_PATH.exists():
            # Fallback: spróbuj znaleźć bez wychodzenia tak wysoko (zależy od struktury uruchamiania)
            # Ale przy main.py w root powinno działać
            QMessageBox.critical(self, "Błąd", f"Nie znaleziono pliku gry:\n{GAME_PATH}\nSprawdź strukturę folderów.")
            return

        try:
            subprocess.Popen([sys.executable, str(GAME_PATH)])
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się uruchomić gry:\n{e}")

    def go_back(self):
        self.main_window.show_retro_console()
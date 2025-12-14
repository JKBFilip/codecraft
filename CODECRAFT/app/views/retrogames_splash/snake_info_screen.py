import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextBrowser, QHBoxLayout, QFrame, QMessageBox)
from PySide6.QtCore import Qt

# Ścieżka do gry: views/retrogames_splash -> views -> app -> retrogames -> snake.py
GAME_PATH = Path(__file__).resolve().parent.parent.parent.parent / "app" / "retrogames" / "snake.py"


class SnakeInfoScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # --- Nagłówek ---
        title = QLabel("🐍 SNAKE - Kultowy Wąż")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("welcomeHeader")
        title.setStyleSheet("font-size: 36px; margin-bottom: 20px;")
        layout.addWidget(title)

        # --- Treść ---
        content_frame = QFrame()
        content_frame.setObjectName("formFrame")
        frame_layout = QVBoxLayout(content_frame)

        info_text = QTextBrowser()
        info_text.setOpenExternalLinks(True)
        info_text.setHtml("""
            <h3 style="color: #6200ea;">📜 Krótka Historia</h3>
            <p>Gra w węża powstała w <b>1976 roku</b> pod nazwą <i>Blockade</i> jako gra na automaty. Jednak prawdziwą nieśmiertelność zyskała pod koniec lat 90.</p>
            <ul>
                <li><b>1997:</b> Nokia instaluje grę <i>Snake</i> na modelu <b>6110</b>. To był moment przełomowy dla gier mobilnych.</li>
                <li>Wersja na Nokię 3310 (Snake II) stała się ikoną popkultury. Wiele osób kupowało ten telefon tylko dla tej gry!</li>
            </ul>
            <p>Zasada jest prosta, ale uzależniająca: jedz, rośnij i nie ugryź własnego ogona.</p>

            <hr>

            <h3 style="color: #ff9800;">🎮 Jak grać?</h3>
            <p><b>Cel:</b> Steruj wężem, zjadaj jedzenie (czerwone punkty) i zdobywaj punkty. Każdy posiłek wydłuża węża.</p>
            <p><b>Sterowanie:</b></p>
            <ul>
                <li>Strzałki kierunkowe lub klawisze <b>W / S / A / D</b>.</li>
                <li><b>ESC</b> - Pauza.</li>
                <li><b>X</b> - Wyjście z gry (tylko podczas pauzy).</li>
            </ul>
            <p><b>Zasady:</b></p>
            <ul>
                <li>Uderzenie w ścianę lub własny ogon kończy grę (resetuje wynik).</li>
                <li>Im dłuższy wąż, tym trudniej manewrować!</li>
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
        if not GAME_PATH.exists():
            QMessageBox.critical(self, "Błąd", f"Nie znaleziono pliku gry:\n{GAME_PATH}")
            return
        try:
            subprocess.Popen([sys.executable, str(GAME_PATH)])
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się uruchomić gry:\n{e}")

    def go_back(self):
        self.main_window.show_retro_console()
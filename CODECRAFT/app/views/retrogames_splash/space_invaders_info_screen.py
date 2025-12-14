import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextBrowser, QHBoxLayout, QFrame, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

GAME_PATH = Path(__file__).resolve().parent.parent.parent.parent / "app" / "retrogames" / "space_invaders.py"


class SpaceInvadersInfoScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("👾 SPACE INVADERS - Ikona Arkadówek")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("welcomeHeader")
        title.setStyleSheet("font-size: 36px; margin-bottom: 20px;")
        layout.addWidget(title)

        content_frame = QFrame()
        content_frame.setObjectName("formFrame")
        frame_layout = QVBoxLayout(content_frame)

        info_text = QTextBrowser()
        info_text.setOpenExternalLinks(True)
        info_text.setHtml("""
            <h3 style="color: #6200ea;">📜 Krótka Historia</h3>
            <p>Gra stworzona w <b>1978 roku</b> przez Tomohiro Nishikado. Była tak popularna w Japonii, że rzekomo spowodowała <b>niedobór monet 100-jenowych</b>!</p>
            <ul>
                <li>Jest to pierwsza gra, w której wrogowie "odpowiadają ogniem".</li>
                <li>Oryginalny kod był tak obciążający dla procesora, że wrogowie poruszali się wolno na początku, a przyspieszali w miarę ich zabijania (bo procesor miał mniej do rysowania). Twórca uznał to za "mechanikę trudności" i zostawił!</li>
            </ul>

            <hr>

            <h3 style="color: #ff9800;">🎮 Jak grać?</h3>
            <p><b>Cel:</b> Zestrzel wszystkich kosmitów zanim dotrą do Twojego statku.</p>
            <p><b>Sterowanie:</b></p>
            <ul>
                <li><b>Strzałki Lewo/Prawo</b> (lub A/D) - Ruch statkiem.</li>
                <li><b>SPACJA</b> - Strzał.</li>
                <li><b>ESC</b> - Pauza.</li>
                <li><b>X</b> - Wyjście (w pauzie).</li>
            </ul>
        """)
        info_text.setStyleSheet("background-color: transparent; border: none; font-size: 16px;")

        frame_layout.addWidget(info_text)
        layout.addWidget(content_frame)

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
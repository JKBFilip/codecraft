import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QGridLayout, QFrame, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt

GAMES_DIR = Path(__file__).resolve().parent.parent.parent / "app" / "retrogames"


class RetroConsoleScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        header = QLabel("🕹️ RETRO KONSOLA 🕹️")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-family: 'Consolas', monospace; 
            font-size: 36px; 
            font-weight: bold; 
            color: #00ff00; 
            background-color: #000000;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #00ff00;
        """)
        layout.addWidget(header)

        info = QLabel("Wbijaj kolejne poziomy, aby odblokować klasyczne gry!")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-size: 18px; color: #aaa; margin-bottom: 10px;")
        layout.addWidget(info)

        games_scroll = QScrollArea()
        games_scroll.setWidgetResizable(True)
        games_scroll.setFrameShape(QFrame.NoFrame)

        self.games_container = QWidget()
        self.games_grid = QGridLayout(self.games_container)
        self.games_grid.setSpacing(20)

        self.refresh_state()

        games_scroll.setWidget(self.games_container)
        layout.addWidget(games_scroll)

        back_btn = QPushButton("🔙 Powrót do menu")
        back_btn.setObjectName("secondaryButton")
        back_btn.setMinimumHeight(50)
        back_btn.clicked.connect(self.main_window.show_menu)
        layout.addWidget(back_btn)

    def _add_game_card(self, row, col, title, icon, min_level, action_callback):
        card = QFrame()
        card.setFixedSize(200, 200)
        card_layout = QVBoxLayout(card)

        user_level = 1
        if self.main_window.user_account:
            user_level = self.main_window.user_account.level

        is_unlocked = user_level >= min_level

        if is_unlocked:
            card.setStyleSheet("""
                QFrame {
                    background-color: #2a2a40;
                    border: 2px solid #6200ea;
                    border-radius: 15px;
                }
                QFrame:hover { border-color: #00ff00; }
            """)
            status_text = "ZAGRAJ"
            status_color = "#00ff00"
        else:
            card.setStyleSheet("""
                QFrame {
                    background-color: #1a1a1a;
                    border: 2px dashed #444;
                    border-radius: 15px;
                }
            """)
            status_text = f"Wymagany LVL {min_level}"
            status_color = "#666"
            icon = "🔒"

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 60px; border: none; background: transparent;")

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; border: none; background: transparent; color: white;")

        status_label = QLabel(status_text)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(
            f"font-size: 14px; font-weight: bold; color: {status_color}; border: none; background: transparent;")

        card_layout.addWidget(icon_label)
        card_layout.addWidget(title_label)
        card_layout.addWidget(status_label)

        if is_unlocked:
            btn = QPushButton(card)
            btn.resize(200, 200)
            btn.setStyleSheet("background: transparent; border: none;")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(action_callback)

        self.games_grid.addWidget(card, row, col)

    def refresh_state(self):
        while self.games_grid.count():
            item = self.games_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # Pong
        def pong_action():
            if hasattr(self.main_window, 'show_pong_info'):
                self.main_window.show_pong_info()
            else:
                self.launch_game("pong.py")

        # Snake
        def snake_action():
            if hasattr(self.main_window, 'show_snake_info'):
                self.main_window.show_snake_info()
            else:
                self.launch_game("snake.py")

        # Space Invaders (NOWE!)
        def space_action():
            if hasattr(self.main_window, 'show_space_invaders_info'):
                self.main_window.show_space_invaders_info()
            else:
                self.launch_game("space_invaders.py")

        self._add_game_card(0, 0, "Ping Pong", "🏓", 2, action_callback=pong_action)
        self._add_game_card(0, 1, "Space Invaders", "👾", 5, action_callback=space_action)
        self._add_game_card(0, 2, "Snake", "🐍", 8, action_callback=snake_action)

        self.games_grid.setRowStretch(1, 1)

    def launch_game(self, script_name):
        game_path = GAMES_DIR / script_name

        if not game_path.exists():
            QMessageBox.critical(self, "Błąd", f"Nie znaleziono pliku gry:\n{game_path}")
            return

        try:
            subprocess.Popen([sys.executable, str(game_path)])
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się uruchomić gry:\n{e}")
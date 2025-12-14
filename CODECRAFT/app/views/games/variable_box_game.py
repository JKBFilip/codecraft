from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap


class DraggableLabel(QLabel):
    """Klocek, który można przeciągać (np. liczba 10, napis 'Kot')."""

    def __init__(self, text, value_type, parent=None):
        super().__init__(text, parent)
        self.value_type = value_type
        self.setAlignment(Qt.AlignCenter)
        # Ten styl zostawiamy w kodzie, bo fioletowy pasuje do obu motywów
        self.setStyleSheet("""
            QLabel {
                background-color: #6200ea;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QLabel:hover { background-color: #7c43bd; }
        """)
        self.setFixedSize(100, 50)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            mime_data.setData("application/x-type", self.value_type.encode())
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            drag.exec_(Qt.CopyAction | Qt.MoveAction)


class VariableBox(QFrame):
    """Pudełko reprezentujące zmienną."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.current_value = None
        self.variable_name = ""
        self.setFixedSize(200, 200)

        self.setObjectName("variableBox")

        self.layout = QVBoxLayout(self)
        self.content_label = QLabel("PUSTE")
        self.content_label.setAlignment(Qt.AlignCenter)
        # Usunąłem sztywny kolor tekstu #aaa, ustawi się go w QSS
        self.content_label.setObjectName("boxContentLabel")
        self.content_label.setStyleSheet("border: none; background: transparent; font-size: 20px;")
        self.layout.addWidget(self.content_label)

    def set_name(self, name):
        self.variable_name = name

        # --- ZMIANA: Zamiast setStyleSheet, ustawiamy właściwość ---
        self.setProperty("is_named", True)

        # Odświeżamy style, żeby QSS zauważył zmianę właściwości
        self.style().unpolish(self)
        self.style().polish(self)
        # -----------------------------------------------------------

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if not self.variable_name:
            QMessageBox.warning(self, "Błąd", "Najpierw nazwij zmienną (naklej etykietę)!")
            return

        text = event.mimeData().text()
        val_type = bytes(event.mimeData().data("application/x-type")).decode()

        self.current_value = text
        self.content_label.setText(f"{text}\n({val_type})")
        # Tutaj ustawiamy styl tekstu (zielony), bo to specyficzna akcja sukcesu
        self.content_label.setStyleSheet(
            "color: #4CAF50; font-size: 24px; font-weight: bold; border: none; background: transparent;")
        event.acceptProposedAction()

        print(f"Przypisano {text} do zmiennej {self.variable_name}")


class VariableGameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "🎮 MINI-GRA: Zrozum Zmienną\n1. Nadaj nazwę pudełku (zmiennej).\n2. Przeciągnij wartość do środka.")
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName("gameInstruction")
        layout.addWidget(info)

        # Sekcja nazywania
        name_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nazwa zmiennej (np. wiek)")

        self.name_btn = QPushButton("Naklej Etykietę")
        self.name_btn.clicked.connect(self.apply_label)
        self.name_btn.setObjectName("finalTestButton")

        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.name_btn)
        layout.addLayout(name_layout)

        # Scena gry
        game_area = QHBoxLayout()
        game_area.setSpacing(30)
        game_area.setAlignment(Qt.AlignCenter)

        # Pudełko
        self.box = VariableBox()
        game_area.addWidget(self.box)

        # Wartości
        values_layout = QVBoxLayout()
        values_layout.setSpacing(10)

        values_header = QLabel("Dostępne wartości:")
        values_header.setObjectName("gameHeader")
        values_layout.addWidget(values_header)

        values_layout.addWidget(DraggableLabel("10", "int"))
        values_layout.addWidget(DraggableLabel("'Kotek'", "str"))
        values_layout.addWidget(DraggableLabel("3.14", "float"))
        values_layout.addStretch()

        game_area.addLayout(values_layout)
        layout.addLayout(game_area)

        # Wynik
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("gameResult")
        layout.addWidget(self.result_label)

    def apply_label(self):
        name = self.name_input.text().strip()
        if not name:
            return
        if not name.isidentifier():
            QMessageBox.warning(self, "Błąd", "To nie jest poprawna nazwa zmiennej w Pythonie!")
            return

        self.box.set_name(name)
        self.name_input.setDisabled(True)
        self.name_btn.setDisabled(True)
        self.name_btn.setText(f"Nazwa: {name}")
        self.result_label.setText(f"Super! Stworzyłeś zmienną '{name}'. Teraz wrzuć coś do niej!")
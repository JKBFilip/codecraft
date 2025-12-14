from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QInputDialog, QMessageBox)
from PySide6.QtCore import Qt


class TrainCar(QLabel):
    """Wagon (Element listy)."""

    def __init__(self, text, index):
        super().__init__(f"{text}\n[{index}]")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(60, 60)
        self.setStyleSheet("""
            background-color: #03a9f4;
            color: white;
            border: 2px solid #0288d1;
            border-radius: 5px;
            font-weight: bold;
        """)


class ListTrainGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.train_data = ["Lokomotywa"]  # Początkowa lista
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "🎮 MINI-GRA: Pociąg (Lista)\nLista to uporządkowana kolekcja. Dodawaj i usuwaj wagony, używając metod list.")
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName("gameInstruction")
        layout.addWidget(info)

        # Wizualizacja Pociągu
        self.track_frame = QFrame()
        self.track_frame.setObjectName("variableBox")
        self.track_frame.setMinimumHeight(100)
        self.track_layout = QHBoxLayout(self.track_frame)
        self.track_layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(self.track_frame)

        # Przyciski Metod
        methods_layout = QHBoxLayout()

        btn_append = QPushButton("append(wagon)")
        btn_append.clicked.connect(self.append_wagon)
        btn_append.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px;")

        btn_pop = QPushButton("pop()")
        btn_pop.clicked.connect(self.pop_wagon)
        btn_pop.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 5px;")

        btn_clear = QPushButton("clear()")
        btn_clear.clicked.connect(self.clear_train)
        btn_clear.setStyleSheet("padding: 5px;")

        methods_layout.addWidget(btn_append)
        methods_layout.addWidget(btn_pop)
        methods_layout.addWidget(btn_clear)

        layout.addLayout(methods_layout)

        # Etykieta statusu (zmienna self.status_label musi być stworzona PRZED użyciem refresh_train)
        self.status_label = QLabel(f"pociag = {self.train_data}")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setObjectName("gameHeader")
        layout.addWidget(self.status_label)

        # ✅ POPRAWKA: Wywołujemy odświeżanie DOPIERO TERAZ, gdy status_label już istnieje
        self.refresh_train()

    def refresh_train(self):
        # Czyścimy tory
        while self.track_layout.count():
            child = self.track_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        for i, item in enumerate(self.train_data):
            wagon = TrainCar(item[0], i)  # Pokazujemy pierwszą literę i indeks
            self.track_layout.addWidget(wagon)
            if i < len(self.train_data) - 1:
                link = QLabel("🔗")
                self.track_layout.addWidget(link)

        # Aktualizujemy tekst statusu (teraz bezpiecznie)
        if hasattr(self, 'status_label'):
            self.status_label.setText(f"pociag = {self.train_data}")

    def append_wagon(self):
        text, ok = QInputDialog.getText(self, "Dodaj wagon", "Co przewozi ten wagon?")
        if ok and text:
            self.train_data.append(text)
            self.refresh_train()

    def pop_wagon(self):
        if self.train_data:
            removed = self.train_data.pop()
            QMessageBox.information(self, "Pop!", f"Odczepiono wagon: {removed}")
            self.refresh_train()
        else:
            QMessageBox.warning(self, "Błąd", "Pociąg jest już pusty! (IndexError)")

    def clear_train(self):
        self.train_data.clear()
        self.refresh_train()
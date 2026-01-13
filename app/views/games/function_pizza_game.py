from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QComboBox)
from PySide6.QtCore import Qt


class FunctionPizzaGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "🎮 MINI-GRA: Funkcja Robienia Pizzy\nZdefiniuj argumenty funkcji `zrob_pizze(skladnik1, skladnik2)`, aby otrzymać jadalny wynik.")
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName("gameInstruction")
        layout.addWidget(info)

        # Wizualizacja Funkcji (Maszyna)
        machine_frame = QFrame()
        machine_frame.setObjectName("variableBox")
        machine_layout = QHBoxLayout(machine_frame)

        # Wejścia (Argumenty)
        inputs_layout = QVBoxLayout()
        self.ing1 = QComboBox()
        self.ing1.addItems(["---", "Ciasto", "But", "Kamień"])
        self.ing2 = QComboBox()
        self.ing2.addItems(["---", "Sos Pomidorowy", "Olej Silnikowy", "Ser"])

        inputs_layout.addWidget(QLabel("Argument 1:"))
        inputs_layout.addWidget(self.ing1)
        inputs_layout.addWidget(QLabel("Argument 2:"))
        inputs_layout.addWidget(self.ing2)

        # Strzałka
        arrow = QLabel("➡\nFunkcja\n➡")
        arrow.setAlignment(Qt.AlignCenter)

        # Wyjście (Return)
        self.output_label = QLabel("❓")
        self.output_label.setStyleSheet("font-size: 60px;")
        self.output_label.setAlignment(Qt.AlignCenter)

        machine_layout.addLayout(inputs_layout)
        machine_layout.addWidget(arrow)
        machine_layout.addWidget(self.output_label)

        layout.addWidget(machine_frame)

        # Przycisk Wywołania
        self.call_btn = QPushButton("zrob_pizze(...)")
        self.call_btn.setObjectName("taskButton")
        self.call_btn.clicked.connect(self.call_function)
        layout.addWidget(self.call_btn)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("gameResult")
        layout.addWidget(self.result_label)

    def call_function(self):
        arg1 = self.ing1.currentText()
        arg2 = self.ing2.currentText()

        if arg1 == "---" or arg2 == "---":
            self.result_label.setText("Błąd: Funkcja potrzebuje dwóch argumentów!")
            self.result_label.setStyleSheet("color: orange;")
            return

        # Logika "Maszyny"
        if arg1 == "Ciasto" and arg2 in ["Sos Pomidorowy", "Ser"]:
            self.output_label.setText("🍕")
            self.result_label.setText("Sukces! Funkcja zwróciła (return) pyszną pizzę.")
            self.result_label.setStyleSheet("color: #50fa7b;")
        elif arg1 == "But" or arg2 == "Olej Silnikowy":
            self.output_label.setText("🤢")
            self.result_label.setText("Ble! Niejadalne argumenty. Funkcja zwróciła odpad.")
            self.result_label.setStyleSheet("color: #ff5555;")
        else:
            self.output_label.setText("🧱")
            self.result_label.setText("To nie wygląda jak pizza...")
            self.result_label.setStyleSheet("color: #ff5555;")
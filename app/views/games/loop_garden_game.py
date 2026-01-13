from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSlider, QFrame)
from PySide6.QtCore import Qt, QTimer


class Flower(QLabel):
    """Kwiatek, który można podlać."""

    def __init__(self):
        super().__init__("🥀")  # Zwiędły
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 40px;")
        self.is_watered = False

    def water(self):
        self.setText("🌻")  # Podlany
        self.is_watered = True

    def reset(self):
        self.setText("🥀")
        self.is_watered = False


class LoopGardenGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        info = QLabel(
            "🎮 MINI-GRA: Pętla FOR\nUstaw liczbę powtórzeń pętli `range(x)`, aby podlać wszystkie 5 kwiatków.\nUważaj, żeby nie przelać!")
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName("gameInstruction")
        layout.addWidget(info)

        # Ogród
        garden_frame = QFrame()
        garden_frame.setObjectName("variableBox")  # Używamy istniejącego stylu ramki
        garden_layout = QHBoxLayout(garden_frame)

        self.flowers = []
        for _ in range(5):
            f = Flower()
            self.flowers.append(f)
            garden_layout.addWidget(f)

        layout.addWidget(garden_frame)

        # Panel sterowania
        control_layout = QHBoxLayout()

        self.code_label = QLabel("for i in range( 0 ):")
        self.code_label.setObjectName("gameHeader")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.update_code_label)

        self.run_btn = QPushButton("▶ Uruchom Kod")
        self.run_btn.setObjectName("taskButton")
        self.run_btn.clicked.connect(self.run_simulation)

        control_layout.addWidget(self.code_label)
        control_layout.addWidget(self.slider)
        control_layout.addWidget(self.run_btn)

        layout.addLayout(control_layout)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("gameResult")
        layout.addWidget(self.result_label)

    def update_code_label(self, value):
        self.code_label.setText(f"for i in range( {value} ):")

    def run_simulation(self):
        count = self.slider.value()

        # Resetujemy kwiatki
        for f in self.flowers: f.reset()
        self.result_label.setText("Robot pracuje...")

        # Symulacja krokowa
        self.step = 0
        self.max_steps = count
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulation_step)
        self.timer.start(500)  # Co pół sekundy ruch

    def simulation_step(self):
        if self.step >= self.max_steps:
            self.timer.stop()
            self.check_win()
            return

        if self.step < len(self.flowers):
            self.flowers[self.step].water()
        else:
            # Wylanie wody poza grządkę
            self.result_label.setText("💦 Ała! Woda wylewa się poza ogród! Za dużo powtórzeń!")
            self.result_label.setStyleSheet("color: #ff5555; font-weight: bold; font-size: 16px;")
            self.timer.stop()
            return

        self.step += 1

    def check_win(self):
        if all(f.is_watered for f in self.flowers):
            self.result_label.setText("🎉 Idealnie! Wszystkie kwiatki podlane pętlą.")
            self.result_label.setStyleSheet("color: #50fa7b; font-weight: bold; font-size: 16px;")
        else:
            self.result_label.setText("❌ Za mało! Niektóre kwiatki wciąż są zwiędłe.")
            self.result_label.setStyleSheet("color: #ff5555; font-weight: bold; font-size: 16px;")
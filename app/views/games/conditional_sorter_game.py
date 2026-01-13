from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QMimeData, QTimer
from PySide6.QtGui import QDrag, QPixmap

import random


class DraggableParcel(QLabel):
    """Paczka do sortowania."""

    def __init__(self, value, parent=None):
        super().__init__(str(value), parent)
        self.value = value
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(80, 80)
        self.setStyleSheet("""
            QLabel {
                background-color: #ff9800;
                color: white;
                border: 2px solid #e65100;
                border-radius: 10px;
                font-weight: bold;
                font-size: 18px;
            }
            QLabel:hover { background-color: #ffb74d; }
        """)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(str(self.value))
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            # Ukrywamy oryginał na czas przeciągania
            self.hide()

            # Uruchamiamy akcję przeciągania
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            # --- POPRAWKA ---
            # Zawsze pokazujemy po zakończeniu.
            # Jeśli element został usunięty w dropEvent (sukces), to deleteLater() i tak go usunie za chwilę.
            # Jeśli drop się nie udał, element po prostu wróci na miejsce.
            self.show()
            # ----------------


class SortingBin(QFrame):
    """Kosz na paczki (If / Else)."""

    def __init__(self, label_text, condition_check, parent=None):
        super().__init__(parent)
        self.condition_check = condition_check
        self.setAcceptDrops(True)
        self.setFixedSize(200, 250)
        self.setObjectName("sortingBin")

        layout = QVBoxLayout(self)
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f8f8f2;")
        layout.addWidget(self.label)

        self.status_label = QLabel("📥")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 40px;")
        layout.addWidget(self.status_label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        try:
            value = int(event.mimeData().text())
            if self.condition_check(value):
                self.status_label.setText("✅")
                event.acceptProposedAction()
                self.parent().on_correct_sort()
            else:
                self.status_label.setText("❌")
                event.ignore()
                QMessageBox.warning(self, "Błąd", "Ta paczka tu nie pasuje! Spróbuj drugiego kosza.")
                # Tutaj nie musimy już nic ręcznie przywracać,
                # bo mousePressEvent w DraggableParcel zajmie się pokazaniem elementu
        except ValueError:
            event.ignore()

        QTimer.singleShot(1000, lambda: self.status_label.setText("📥"))


class ConditionalSorterGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.target_score = 5
        self.current_parcel = None
        self.init_ui()
        self.spawn_new_parcel()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.condition_text = "x > 50"
        info = QLabel(
            f"🎮 MINI-GRA: Sortownia IF/ELSE\nZasada: Jeśli {self.condition_text}, wrzuć do TRUE, w przeciwnym razie do FALSE.")
        info.setAlignment(Qt.AlignCenter)
        info.setObjectName("gameInstruction")
        layout.addWidget(info)

        self.score_label = QLabel("Punkty: 0/5")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setObjectName("gameHeader")
        layout.addWidget(self.score_label)

        game_area = QHBoxLayout()

        self.bin_true = SortingBin("TRUE (IF)", lambda x: x > 50, self)
        self.bin_true.setStyleSheet("background-color: #2e7d32; border-radius: 15px;")

        self.spawn_area = QFrame()
        self.spawn_area.setFixedSize(150, 150)
        self.spawn_layout = QVBoxLayout(self.spawn_area)
        self.spawn_layout.setAlignment(Qt.AlignCenter)

        self.bin_false = SortingBin("FALSE (ELSE)", lambda x: x <= 50, self)
        self.bin_false.setStyleSheet("background-color: #c62828; border-radius: 15px;")

        game_area.addWidget(self.bin_true)
        game_area.addWidget(self.spawn_area)
        game_area.addWidget(self.bin_false)

        layout.addLayout(game_area)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setObjectName("gameResult")
        layout.addWidget(self.result_label)

    def spawn_new_parcel(self):
        if self.current_parcel:
            self.current_parcel.deleteLater()
            self.current_parcel = None

        val = random.randint(1, 100)
        self.current_parcel = DraggableParcel(val, self)
        self.spawn_layout.addWidget(self.current_parcel)

    def restore_parcel(self):
        """Metoda pomocnicza (już nieużywana bezpośrednio, ale zostawiam dla kompatybilności)."""
        if self.current_parcel:
            self.current_parcel.show()

    def on_correct_sort(self):
        self.score += 1
        self.score_label.setText(f"Punkty: {self.score}/{self.target_score}")

        if self.current_parcel:
            self.current_parcel.deleteLater()
            self.current_parcel = None

        if self.score >= self.target_score:
            self.result_label.setText("🎉 Brawo! Zrozumiałeś instrukcje warunkowe!")
        else:
            QTimer.singleShot(500, self.spawn_new_parcel)
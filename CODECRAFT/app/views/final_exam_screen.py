from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTextEdit, QComboBox, QScrollArea, QMessageBox)
from PySide6.QtCore import Qt, QTimer, QElapsedTimer
from PySide6.QtGui import QPixmap, QPainter, QFont, QFontMetrics
from app.models.task import Task
import random
from app.views.task_screen import codes_match_ast
from app.widgets.reorder_list import ReorderList
from app.assets.test_summary_styles import generate_summary_html
import os
from pathlib import Path


class CertificateGenerator:
    @staticmethod
    def generate(username, score, date_str, output_path="certificates"):
        Path(output_path).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(output_path, f"certificate_{username}.png")
        pixmap = QPixmap(1200, 900)
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.TextAntialiasing)
            font = QFont("Arial", 48, QFont.Bold)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignTop | Qt.AlignHCenter, "Certyfikat Ukończenia\nCODECRAFT")
            font = QFont("Arial", 32)
            painter.setFont(font)
            text_rect = pixmap.rect().adjusted(0, 200, 0, -200)
            lines = [
                f"Niniejszym potwierdza się, że",
                f"{username}",
                f"pomyślnie ukończył(a) egzamin końcowy",
                f"z wynikiem {score}%",
                f"w dniu {date_str}"
            ]

            line_height = QFontMetrics(font).height()
            current_y = text_rect.top()

            for line in lines:
                if line == username:
                    name_font = QFont("Arial", 40, QFont.Bold)
                    painter.setFont(name_font)
                    line_height = QFontMetrics(name_font).height()
                else:
                    painter.setFont(font)
                    line_height = QFontMetrics(font).height()

                painter.drawText(text_rect, Qt.AlignHCenter | Qt.AlignTop, line)
                text_rect.adjust(0, line_height + 20, 0, 0)

            font = QFont("Arial", 16)
            painter.setFont(font)
            painter.drawText(
                pixmap.rect().adjusted(0, 0, 0, -50),
                Qt.AlignBottom | Qt.AlignHCenter,
                "Certyfikat wygenerowany automatycznie przez system CODECRAFT"
            )

            painter.setPen(Qt.black)
            painter.drawRect(pixmap.rect().adjusted(10, 10, -10, -10))
        finally:
            painter.end()

        pixmap.save(file_path)
        return file_path


class FinalExamScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.exam_passed = False
        self.has_previous_pass = self.main_window.user_account.has_passed_final_exam()
        self.final_exam_result = self.main_window.user_account.get_final_exam_result()
        self.init_ui()
        if self.has_previous_pass:
            self.show_certificate_screen()
        else:
            self.start_new_exam()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.timer_label = QLabel("Czas: 30:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #d32f2f;")
        self.layout.addWidget(self.timer_label)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        self.scroll.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll)
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 18px; margin-bottom: 15px;")
        self.content_layout.addWidget(self.question_label)
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Wpisz tutaj swój kod...")
        self.content_layout.addWidget(self.code_input)
        self.option_select = QComboBox()
        self.content_layout.addWidget(self.option_select)
        self.reorder_list = ReorderList()
        self.content_layout.addWidget(self.reorder_list)
        self.submit_button = QPushButton("Zatwierdź odpowiedź")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.hide()
        self.layout.addWidget(self.summary_text)
        self.certificate_section = QWidget()
        self.certificate_layout = QVBoxLayout()
        self.certificate_section.setLayout(self.certificate_layout)
        self.certificate_label = QLabel()
        self.certificate_label.setAlignment(Qt.AlignCenter)
        self.certificate_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.certificate_layout.addWidget(self.certificate_label)
        self.download_cert_button = QPushButton("📄 Pobierz certyfikat")
        self.download_cert_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.download_cert_button.clicked.connect(self.download_certificate)
        self.certificate_layout.addWidget(self.download_cert_button)
        self.layout.addWidget(self.certificate_section)
        self.certificate_section.hide()
        self.back_button = QPushButton("🔙 Powrót do menu")
        self.back_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.back_button.clicked.connect(self.main_window.show_menu)
        self.layout.addWidget(self.back_button)

    def start_new_exam(self):
        self.tasks = self._prepare_exam_tasks()
        self.current_index = 0
        self.correct_answers = 0
        self.remaining_time = 1800
        self.user_answers = []
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_timer)
        self.elapsed_timer = QElapsedTimer()
        self.load_task()
        self.start_exam()

    def show_certificate_screen(self):
        self.timer_label.hide()
        self.submit_button.hide()
        self.scroll.hide()
        if self.final_exam_result:
            date_obj = datetime.fromisoformat(self.final_exam_result['date'])
            date_str = date_obj.strftime("%d.%m.%Y")
            self.summary_text.setHtml(f"""
                <h2 style="text-align: center;">Egzamin już zaliczony!</h2>
                <div style="text-align: center; font-size: 16px;">
                    <p>Twój poprzedni wynik: <strong>{self.final_exam_result['score']}%</strong></p>
                    <p>Data zaliczenia: {date_str}</p>
                    <p>Czas wykonania: {self.final_exam_result['time_taken']:.1f} sekund</p>
                </div>
            """)
            self.summary_text.show()
            self.certificate_label.setText("🎉 Możesz pobrać swój certyfikat ponownie")
            self.certificate_label.setStyleSheet("color: #2E7D32; font-size: 18px;")
            self.certificate_section.show()
            self.download_cert_button.show()
            self.back_button.show()

    def _prepare_exam_tasks(self):
        all_tasks = Task.load_all()
        exam_tasks = []
        for module in range(1, 6):
            module_tasks = [t for t in all_tasks if t.lesson_index == module]
            if len(module_tasks) >= 2:
                exam_tasks.extend(random.sample(module_tasks, 2))
            elif module_tasks:
                exam_tasks.extend(module_tasks)

        remaining_slots = max(0, 20 - len(exam_tasks))
        if remaining_slots > 0:
            extra_tasks = [t for t in all_tasks if t not in exam_tasks]
            if extra_tasks:
                exam_tasks.extend(random.sample(extra_tasks, min(remaining_slots, len(extra_tasks))))

        if not exam_tasks:
            exam_tasks = [Task(0, "Debug: Wpisz 'print('Egzamin')'", "print('Egzamin')", "code_input")]
        random.shuffle(exam_tasks)
        return exam_tasks

    def start_exam(self):
        self.elapsed_timer.start()
        self.countdown_timer.start(1000)
        self.remaining_time = 1800

    def update_timer(self):
        self.remaining_time -= 1
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.setText(f"Czas: {minutes:02d}:{seconds:02d}")

        if self.remaining_time <= 300:
            self.timer_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #d32f2f;")

        if self.remaining_time <= 0:
            self.countdown_timer.stop()
            self.end_exam(timeout=True)

    def load_task(self):
        if self.current_index >= len(self.tasks):
            self.end_exam()
            return

        task = self.tasks[self.current_index]
        self.current_task = task
        self.code_input.hide()
        self.option_select.hide()
        self.reorder_list.hide()
        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()
        self.question_label.setText(
            f"Pytanie {self.current_index + 1}/{len(self.tasks)} (Moduł {task.lesson_index}):\n\n{task.question}"
        )

        if task.type in ("code_input", "code_output"):
            self.code_input.show()
            if task.type == "code_output":
                self.code_input.setPlaceholderText("Wpisz oczekiwany wynik...")
        elif task.type == "multiple_choice":
            self.option_select.show()
            for opt in task.options:
                self.option_select.addItem(opt)
        elif task.type == "reorder":
            self.reorder_list.show()
            for block in task.options:
                self.reorder_list.addItem(block)

    def check_answer(self):
        if not hasattr(self, 'current_task'):
            return

        task = self.current_task
        user_answer = ""
        correct_answer = task.solution
        is_correct = False

        if task.type == "code_input":
            user_answer = self.code_input.toPlainText()
            is_correct = codes_match_ast(user_answer, correct_answer)
        elif task.type == "code_output":
            user_answer = self.code_input.toPlainText().strip()
            is_correct = (user_answer == correct_answer.strip())
        elif task.type == "multiple_choice":
            user_answer = self.option_select.currentText().strip()
            is_correct = user_answer.startswith(correct_answer)
        elif task.type == "reorder":
            user_answer = self.reorder_list.get_code_string().strip()
            correct_lines = [line.strip() for line in correct_answer.strip().splitlines()]
            user_lines = [line.strip() for line in user_answer.splitlines()]
            is_correct = user_lines == correct_lines

        self.user_answers.append({
            "question": task.question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "type": task.type,
            "module": task.lesson_index
        })

        if is_correct:
            self.correct_answers += 1

        self.current_index += 1
        self.load_task()

    def end_exam(self, timeout=False):
        self.countdown_timer.stop()
        elapsed_time = float(self.elapsed_timer.elapsed()) / 1000
        total_questions = len(self.tasks)
        score_percentage = (self.correct_answers / total_questions) * 100
        self.exam_passed = score_percentage >= 80
        self.timer_label.hide()
        self.submit_button.hide()
        self.scroll.hide()
        self.summary_text.setHtml(generate_summary_html(self.user_answers, self.correct_answers))
        self.summary_text.show()

        if timeout:
            result_msg = "Czas minął! Egzamin niezaliczony."
            self.certificate_label.setStyleSheet("color: #d32f2f;")
        elif self.exam_passed:
            result_msg = f"Egzamin zdany! Wynik: {score_percentage:.1f}%"
            self.certificate_label.setStyleSheet("color: #2E7D32;")
            self.certificate_label.setText("🎉 Gratulacje! Zdobyłeś certyfikat!")
            self.download_cert_button.show()
        else:
            result_msg = f"Egzamin niezaliczony. Wynik: {score_percentage:.1f}% (wymagane 80%)"
            self.certificate_label.setStyleSheet("color: #d32f2f;")

        self.certificate_label.setText(result_msg)
        self.certificate_section.show()
        self.back_button.show()
        self.summary_text.setMinimumHeight(400)
        self.summary_text.setMaximumHeight(600)
        self.main_window.user_progress.add_test_result(
            module_index=0,
            score=score_percentage,
            perfect_score=(score_percentage == 100),
            time_taken=elapsed_time
        )
        self.main_window.user_progress.save_progress()
        new_achievements = self.main_window.user_progress.check_achievements()
        if new_achievements:
            self.main_window.show_achievement_notification(new_achievements)

    def download_certificate(self):
        if not self.exam_passed and not self.has_previous_pass:
            return

        username = self.main_window.user_account.username
        if self.has_previous_pass:
            score = self.final_exam_result['score']
        else:
            score = (self.correct_answers / len(self.tasks)) * 100

        date_str = datetime.now().strftime("%d.%m.%Y")
        try:
            cert_path = CertificateGenerator.generate(
                username=username,
                score=f"{score:.1f}",
                date_str=date_str
            )

            QMessageBox.information(
                self,
                "Certyfikat wygenerowany",
                f"Certyfikat został zapisany w:\n{cert_path}"
            )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Błąd",
                f"Nie udało się wygenerować certyfikatu:\n{str(e)}"
            )
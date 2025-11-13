import random
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QElapsedTimer, QRectF
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor, QPen, QTextDocument
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QTextEdit, QComboBox, QMessageBox, QStackedWidget, QFrame)

from app.models.task import Task
from app.views.task_screen import codes_match_ast
from app.widgets.reorder_list import ReorderList
from app.assets.test_summary_styles import generate_summary_html

class CertificateGenerator:
    @staticmethod
    def generate(username, score, date_str, output_path="certificates"):
        Path(output_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(output_path) / f"certificate_{username}.png"
        pixmap = QPixmap(1200, 800)
        pixmap.fill(QColor("#fdf6e3"))
        painter = QPainter(pixmap)
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            border_color = QColor("#002b36")
            pen = QPen(border_color, 15)
            painter.setPen(pen)
            painter.drawRect(pixmap.rect().adjusted(10, 10, -10, -10))
            painter.setPen(border_color)
            painter.setFont(QFont("Georgia", 48, QFont.Bold))
            painter.drawText(QRectF(0, 60, 1200, 150), Qt.AlignHCenter, "Certyfikat Ukończenia")
            painter.setFont(QFont("Segoe UI", 32, QFont.Bold))
            painter.setPen(QColor("#cb4b16"))
            painter.drawText(QRectF(0, 150, 1200, 100), Qt.AlignHCenter, "CODECRAFT")
            painter.setPen(border_color)
            main_text = (
                f"Niniejszym potwierdza się, że",
                f"<b>{username}</b>",
                f"pomyślnie ukończył(a) egzamin końcowy",
                f"z wynikiem <b>{score}%</b> w dniu {date_str}"
            )
            doc = QTextDocument()
            html = f"<div style='text-align: center; color: #002b36;'>{'<br>'.join(main_text)}</div>"
            doc.setHtml(html)
            doc.setDefaultFont(QFont("Georgia", 24))
            doc.setTextWidth(1000)
            painter.save()
            painter.translate(100, 300)
            doc.drawContents(painter)
            painter.restore()
            painter.setFont(QFont("Segoe UI", 14))
            painter.drawText(QRectF(0, 720, 1180, 50), Qt.AlignRight, "System Edukacyjny CODECRAFT")
        finally:
            painter.end()
        pixmap.save(str(file_path))
        return str(file_path)

class FinalExamScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.tasks, self.user_answers = [], []
        self.current_index, self.correct_answers, self.remaining_time = 0, 0, 1800
        self.countdown_timer, self.elapsed_timer = QTimer(self), QElapsedTimer()

        self.stack = QStackedWidget(self)
        self.start_page = self._create_start_page()
        self.exam_page = self._create_exam_page()
        self.results_page = self._create_results_page()
        self.exam_passed = False

        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.exam_page)
        self.stack.addWidget(self.results_page)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)

    def _create_start_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        self.start_info_label = QLabel("Witaj na Egzaminie Końcowym!")
        self.start_info_label.setObjectName("welcomeHeader")

        rules_label = QLabel("Egzamin składa się z 20 pytań i masz na niego 30 minut.\nPowodzenia!")
        rules_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("🚀 Rozpocznij Egzamin")
        self.start_button.setMinimumHeight(50)
        self.start_button.setObjectName("primaryButton")
        self.start_button.clicked.connect(self._start_exam)

        back_button = QPushButton("🔙 Powrót do menu")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.main_window.show_menu)

        layout.addWidget(self.start_info_label)
        layout.addWidget(rules_label)
        layout.addSpacing(30)
        layout.addWidget(self.start_button)
        layout.addWidget(back_button)
        return page

    def _create_exam_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addStretch()
        self.timer_label = QLabel("Czas: 30:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ffca8a; padding: 5px; background-color: #2a2a40; border-radius: 5px;")
        top_bar_layout.addWidget(self.timer_label)
        layout.addLayout(top_bar_layout)

        question_frame = QFrame()
        question_frame.setObjectName("formFrame")
        q_layout = QVBoxLayout(question_frame)
        q_layout.setSpacing(10)

        self.question_label = QLabel("Pytanie...")
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet(
            "font-size: 18px; color: #f8f8f2; margin-bottom: 10px;")
        q_layout.addWidget(self.question_label)

        self.answer_stack = QStackedWidget()
        self.code_input = QTextEdit()
        self.option_select = QComboBox()
        self.reorder_list = ReorderList()
        self.answer_stack.addWidget(self.code_input)
        self.answer_stack.addWidget(self.option_select)
        self.answer_stack.addWidget(self.reorder_list)
        q_layout.addWidget(self.answer_stack)

        layout.addWidget(question_frame)

        self.submit_button = QPushButton("Zatwierdź odpowiedź")
        self.submit_button.setObjectName("primaryButton")
        self.submit_button.setMinimumHeight(45)
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)
        return page

    def _create_results_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        self.results_title = QLabel("Wyniki Egzaminu")
        self.results_title.setObjectName("welcomeHeader")
        self.results_title.setAlignment(Qt.AlignCenter)
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setObjectName("summaryText")
        self.download_cert_button = QPushButton("📄 Pobierz certyfikat")
        self.download_cert_button.setObjectName("primaryButton")
        self.download_cert_button.clicked.connect(self.download_certificate)
        back_button = QPushButton("🔙 Powrót do menu")
        back_button.setObjectName("secondaryButton")
        back_button.clicked.connect(self.main_window.show_menu)
        layout.addWidget(self.results_title)
        layout.addWidget(self.summary_text)
        layout.addWidget(self.download_cert_button)
        layout.addWidget(back_button)
        return page

    def prepare_and_display(self):
        if not self.main_window.user_account:
            self.stack.setCurrentWidget(self.start_page)
            return
        if self.main_window.user_account.has_passed_final_exam():
            self._show_results_page(previous_pass=True)
        else:
            self.tasks = self._prepare_exam_tasks()
            self.stack.setCurrentWidget(self.start_page)

    def _start_exam(self):
        self.current_index, self.correct_answers = 0, 0
        self.user_answers, self.remaining_time = [], 1800
        self.countdown_timer.timeout.connect(self.update_timer)
        self.elapsed_timer.start()
        self.countdown_timer.start(1000)
        self.load_task()
        self.stack.setCurrentWidget(self.exam_page)

    def update_timer(self):
        self.remaining_time -= 1
        minutes, seconds = self.remaining_time // 60, self.remaining_time % 60
        self.timer_label.setText(f"Czas: {minutes:02d}:{seconds:02d}")
        if self.remaining_time <= 300:
            self.timer_label.setStyleSheet(
                "font-size: 16px; font-weight: bold; color: #f44336; padding: 5px; background-color: #2a2a40; border-radius: 5px;")
        if self.remaining_time <= 0:
            self.end_exam(timeout=True)

    def load_task(self):
        if self.current_index >= len(self.tasks):
            self.end_exam()
            return

        self.current_task = self.tasks[self.current_index]
        self.question_label.setText(f"Pytanie {self.current_index + 1}/{len(self.tasks)}: {self.current_task.question}")
        task_type = self.current_task.type

        self.code_input.clear()
        self.option_select.clear()
        self.reorder_list.clear()

        if task_type in ("code_input", "code_output"):
            self.code_input.setPlaceholderText("Wpisz odpowiedź...")
            self.answer_stack.setCurrentWidget(self.code_input)
        elif task_type == "multiple_choice":
            self.option_select.addItems(self.current_task.options)
            self.answer_stack.setCurrentWidget(self.option_select)
        elif task_type == "reorder":
            options_copy = self.current_task.options[:]
            random.shuffle(options_copy)
            self.reorder_list.addItems(options_copy)
            self.answer_stack.setCurrentWidget(self.reorder_list)

    def check_answer(self):
        if not hasattr(self, 'current_task'):
            return

        task = self.current_task
        user_answer, correct_answer, is_correct = "", task.solution, False

        try:
            if task.type == "code_input":
                user_answer = self.code_input.toPlainText()
                is_correct = codes_match_ast(user_answer, correct_answer)
            elif task.type == "code_output":
                user_answer = self.code_input.toPlainText().strip()
                is_correct = (user_answer == correct_answer.strip())
            elif task.type == "multiple_choice":
                user_answer = self.option_select.currentText()
                is_correct = user_answer.strip().startswith(correct_answer.strip())
            elif task.type == "reorder":
                user_answer = self.reorder_list.get_code_string()
                user_lines = [line.strip() for line in user_answer.strip().splitlines()]
                correct_lines = [line.strip() for line in correct_answer.strip().splitlines()]
                is_correct = user_lines == correct_lines

        except Exception as e:
            print(f"BŁĄD podczas sprawdzania odpowiedzi: {e}")
            is_correct = False

        self.user_answers.append(
            {"question": task.question, "user_answer": user_answer, "correct_answer": correct_answer,
             "is_correct": is_correct, "type": task.type})

        if is_correct:
            self.correct_answers += 1

        self.current_index += 1
        self.load_task()

    def end_exam(self, timeout=False):
        self.countdown_timer.stop()
        elapsed_time = float(self.elapsed_timer.elapsed()) / 1000.0
        total_questions = len(self.tasks)
        self.score_percentage = (self.correct_answers / total_questions) * 100 if total_questions > 0 else 0

        self.exam_passed = (self.score_percentage >= 80) and not timeout

        self.main_window.user_progress.add_test_result(
            module_index=0,
            score=self.score_percentage,
            perfect_score=(self.correct_answers == total_questions and total_questions > 0),
            time_taken=elapsed_time
        )
        self.main_window.user_progress.check_achievements()
        self._show_results_page(timeout=timeout)

    def _show_results_page(self, previous_pass=False, timeout=False):
        if previous_pass:
            result = self.main_window.user_account.get_final_exam_result()
            if result:
                self.results_title.setText("Egzamin już zaliczony!")
                self.summary_text.setHtml(
                    f"""<div style="font-size: 18px; text-align: center; color: #E0E0E0;"><p>Twój poprzedni wynik: <strong style="color: #50fa7b;">{result['score']:.1f}%</strong>.</p><p>Data zaliczenia: {datetime.fromisoformat(result['date']).strftime('%d.%m.%Y')}</p></div>""")
                self.download_cert_button.setText("📄 Pobierz certyfikat ponownie")
                self.download_cert_button.setVisible(True)
                self.exam_passed = True
            else:
                self.results_title.setText("Błąd wczytywania wyniku!")
                self.summary_text.setText("Nie udało się wczytać danych.")
                self.download_cert_button.setVisible(False)
        else:
            required = 16
            self.summary_text.setHtml(
                generate_summary_html(self.user_answers, self.correct_answers, required_to_pass=required))

            if timeout:
                self.results_title.setText("Czas minął! Egzamin niezaliczony.")
            elif self.exam_passed:
                self.results_title.setText(f"🎉 Gratulacje! Egzamin zdany ({self.correct_answers}/{len(self.tasks)})!")
            else:
                self.results_title.setText(f"Egzamin niezaliczony ({self.correct_answers}/{len(self.tasks)}).")

            self.download_cert_button.setVisible(self.exam_passed)

        self.stack.setCurrentWidget(self.results_page)

    def download_certificate(self):
        if not getattr(self, 'exam_passed', False):
            QMessageBox.warning(self, "Błąd", "Egzamin nie został zaliczony.")
            return
        username = self.main_window.user_account.username
        date_str = datetime.now().strftime("%d.%m.%Y")
        previous_result = self.main_window.user_account.get_final_exam_result()
        score = previous_result['score'] if previous_result else self.score_percentage
        try:
            cert_path = CertificateGenerator.generate(username, f"{score:.1f}", date_str)
            QMessageBox.information(self, "Sukces", f"Certyfikat zapisano w:\n{cert_path}")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Nie udało się wygenerować certyfikatu:\n{str(e)}")

    def _prepare_exam_tasks(self):
        try:
            all_tasks = Task.load_all()
            exam_tasks = []
            for module in range(1, 6):
                module_tasks = [t for t in all_tasks if t.lesson_index == module]
                if len(module_tasks) >= 2: exam_tasks.extend(random.sample(module_tasks, 2))
            if len(exam_tasks) < 20:
                other_tasks = [t for t in all_tasks if t not in exam_tasks]
                needed = 20 - len(exam_tasks)
                if len(other_tasks) >= needed: exam_tasks.extend(random.sample(other_tasks, needed))
            random.shuffle(exam_tasks)
            return exam_tasks[:20]
        except Exception as e:
            print(f"BŁĄD KRYTYCZNY w _prepare_exam_tasks: {e}")
            QMessageBox.critical(self, "Błąd ładowania zadań", "Nie udało się przygotować zadań do egzaminu.")
            return []
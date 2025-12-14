from app.assets.test_summary_styles import generate_summary_html, format_answer

# sprawdzamy czy formatowanie kodu dziala
def test_format_answer():
    assert "<pre><code>print</code></pre>" in format_answer("print", "code_input")
    assert "<br>Opcja A" in format_answer("Opcja A", "multiple_choice")
    assert "&lt;" in format_answer("if x < 5:", "code_input")

# testujemy czy pokazuje ze zdane jak jest dobrze
def test_generate_summary_passed():
    odpowiedzi = [
        {"is_correct": True, "question": "Q1", "user_answer": "A", "correct_answer": "A", "type": "multiple_choice"}
    ]
    html = generate_summary_html(odpowiedzi, correct_answers=1, required_to_pass=1)

    assert "class=\"final-result passed\"" in html
    assert "Gratulacje" in html
    assert "Wynik: 1/1" in html

# testujemy czy pokazuje ze oblane jak jest zle
def test_generate_summary_failed():
    odpowiedzi = [
        {"is_correct": False, "question": "Q1", "user_answer": "A", "correct_answer": "B", "type": "multiple_choice"}
    ]
    html = generate_summary_html(odpowiedzi, correct_answers=0, required_to_pass=1)

    assert "class=\"final-result failed\"" in html
    assert "Test niezaliczony" in html
    assert "class=\"answer-section correct-answer\"" in html
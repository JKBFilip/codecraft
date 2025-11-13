import html

TEST_SUMMARY_STYLES = """
<style>
    body {
        font-family: "Segoe UI", sans-serif;
        background-color: #2a2a40;
        color: #f8f8f2;
        padding: 15px;
        line-height: 1.5;
    }
    h2 {
        color: #bd93f9;
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
    }
    .question-container {
        margin-bottom: 20px;
        border: 1px solid #3e3e5e;
        border-radius: 8px;
        padding: 15px;
        background: #1e1e2f;
    }
    .question-text {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    .answer-section {
        margin: 8px 0;
        padding: 10px 15px;
        border-radius: 6px;
        font-family: Consolas, 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.4;
        border-left: 4px solid;
    }
    .answer-section pre {
        margin: 5px 0;
        padding: 8px;
        background-color: #1a1a2e;
        border-radius: 4px;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    .answer-section code {
        font-family: Consolas, 'Courier New', monospace;
    }
    .user-answer {
        background: #44475a;
        border-left-color: #ffb86c;
        color: #f8f8f2;
    }
    .correct-answer {
        background: #6272a4;
        border-left-color: #50fa7b;
        color: #f8f8f2;
    }
    .status-icon {
        margin-right: 8px;
        font-weight: bold;
    }
    .correct { color: #50fa7b; }
    .incorrect { color: #ff5555; }
    .final-result {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        margin: 25px 0;
        border-radius: 8px;
        line-height: 1.6;
    }
    .passed {
        background: #283636;
        color: #50fa7b;
        border: 1px solid #50fa7b;
    }
    .failed {
        background: #443638;
        color: #ff5555;
        border: 1px solid #ff5555;
    }
    .score {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #8be9fd;
        margin: 15px 0 25px 0;
    }
</style>
"""

def generate_summary_html(user_answers, correct_answers, required_to_pass):
    html_content = TEST_SUMMARY_STYLES
    total_questions = len(user_answers)
    html_content += f"""
    <h2>Podsumowanie testu</h2>
    <div class="score">Wynik: {correct_answers}/{total_questions}</div>
    """

    for i, answer_data in enumerate(user_answers, 1):
        status_class = "correct" if answer_data.get("is_correct") else "incorrect"
        status_icon = "✓" if answer_data.get("is_correct") else "✗"
        question = answer_data.get('question', 'Brak pytania')
        user_answer = answer_data.get('user_answer', 'Brak odpowiedzi')
        correct_answer = answer_data.get('correct_answer', 'Brak poprawnej odpowiedzi')
        answer_type = answer_data.get('type', 'unknown')

        html_content += f"""
        <div class="question-container">
            <div class="question-text {status_class}">
                <span class="status-icon">{status_icon}</span> Pytanie {i}: {question}
            </div>
            <div class="answer-section user-answer">
                <strong>Twoja odpowiedź:</strong>
                {format_answer(user_answer, answer_type)}
            </div>
        """

        if not answer_data.get("is_correct"):
            html_content += f"""
            <div class="answer-section correct-answer">
                <strong>Poprawna odpowiedź:</strong>
                {format_answer(correct_answer, answer_type)}
            </div>
            """

        html_content += "</div>"

    if correct_answers >= required_to_pass:
        html_content += f"""
        <div class="final-result passed">
            🎉 Test zaliczony! Gratulacje! <br> (Wymagane minimum: {required_to_pass}/{total_questions})
        </div>
        """
    else:
        html_content += f"""
        <div class="final-result failed">
            ❌ Test niezaliczony. <br> Wymagane minimum {required_to_pass} poprawnych odpowiedzi z {total_questions}.
        </div>
        """

    return html_content

def format_answer(answer, answer_type):
    escaped_answer = html.escape(str(answer))

    if answer_type in ('code_input', 'code_output', 'reorder'):
        return f"<pre><code>{escaped_answer}</code></pre>"
    elif answer_type == 'multiple_choice':
        return f"<br>{escaped_answer}"
    else:
        return f"<br>{escaped_answer}"
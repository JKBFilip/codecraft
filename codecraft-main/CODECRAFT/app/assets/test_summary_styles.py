TEST_SUMMARY_STYLES = """
<style>
    body { 
        font-family: Arial, sans-serif;
        color: #333;
    }
    h2 { 
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .question-container {
        margin-bottom: 25px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        background: #f9f9f9;
    }
    .question-text {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        color: #2c3e50;
    }
    .answer-section {
        margin: 10px 0;
        padding: 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.5;
    }
    .user-answer {
        background: #fff8e1;
        border-left: 4px solid #ffa000;
        color: #333;
    }
    .correct-answer {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        color: #333;
    }
    .status-icon {
        margin-right: 8px;
    }
    .correct { color: #4caf50; }
    .incorrect { color: #f44336; }
    .final-result {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        margin: 20px 0;
        border-radius: 8px;
    }
    .passed {
        background: #e8f5e9;
        color: #2e7d32;
    }
    .failed {
        background: #ffebee;
        color: #c62828;
    }
    .score {
        font-size: 24px;
        color: #1e88e5;
        margin: 10px 0;
    }
</style>
"""


def generate_summary_html(user_answers, correct_answers):
    html = TEST_SUMMARY_STYLES
    html += f"""
    <h2>Podsumowanie testu</h2>
    <div class="score">Wynik: {correct_answers}/{len(user_answers)}</div>
    """

    for i, answer in enumerate(user_answers, 1):
        status_class = "correct" if answer["is_correct"] else "incorrect"
        status_icon = "✓" if answer["is_correct"] else "✗"

        html += f"""
        <div class="question-container">
            <div class="question-text {status_class}">
                <span class="status-icon">{status_icon}</span> Pytanie {i}: {answer['question']}
            </div>
            <div class="answer-section user-answer">
                <strong>Twoja odpowiedź:</strong><br>
                {format_answer(answer['user_answer'], answer['type'])}
            </div>
        """

        if not answer["is_correct"]:
            html += f"""
            <div class="answer-section correct-answer">
                <strong>Poprawna odpowiedź:</strong><br>
                {format_answer(answer['correct_answer'], answer['type'])}
            </div>
            """

        html += "</div>"

    # Final result
    if correct_answers >= 8:
        html += """
        <div class="final-result passed">
            🎉 Test zaliczony! Gratulacje!
        </div>
        """
    else:
        html += """
        <div class="final-result failed">
            ❌ Test niezaliczony. Wymagane minimum 8 poprawnych odpowiedzi.
        </div>
        """

    return html


def format_answer(answer, answer_type):
    if answer_type == 'multiple_choice':
        return f"Wybrano: {answer}"
    elif answer_type == 'reorder':
        return f"Ułożenie:\n{answer}"
    return answer
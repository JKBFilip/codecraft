## ===================================================================
## ===           STYLE PODSUMOWANIA TESTU (WERSJA CIEMNA)          ===
## ===================================================================

TEST_SUMMARY_STYLES = """
<style>
    body {
        font-family: "Segoe UI", sans-serif;
        background-color: #2a2a40; /* Ciemne tło dla podsumowania */
        color: #f8f8f2;            /* Jasny tekst */
        padding: 15px;
        line-height: 1.5; /* Lepsza czytelność */
    }
    h2 {
        color: #bd93f9; /* Fioletowy akcent dla nagłówka */
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
    }
    .question-container {
        margin-bottom: 20px;
        border: 1px solid #3e3e5e; /* Ciemniejsza ramka */
        border-radius: 8px;
        padding: 15px;
        background: #1e1e2f; /* Tło kontenera pytania */
    }
    .question-text {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    .answer-section {
        margin: 8px 0;
        padding: 10px 15px; /* Dodano padding poziomy */
        border-radius: 6px;
        font-family: Consolas, 'Courier New', monospace; /* Lepsza czcionka kodu */
        font-size: 14px;
        line-height: 1.4;
        border-left: 4px solid; /* Grubszy lewy border dla wizualnego rozróżnienia */
    }
    /* Ulepszone formatowanie dla bloków kodu */
    .answer-section pre {
        margin: 5px 0;
        padding: 8px;
        background-color: #1a1a2e; /* Nieco ciemniejsze tło dla pre */
        border-radius: 4px;
        white-space: pre-wrap; /* Zawijanie długich linii kodu */
        word-wrap: break-word;
    }
    .answer-section code {
        font-family: Consolas, 'Courier New', monospace;
    }
    .user-answer {
        background: #44475a; /* Ciemnoszary dla odpowiedzi użytkownika */
        border-left-color: #ffb86c; /* Pomarańczowy akcent */
        color: #f8f8f2;
    }
    .correct-answer {
        background: #6272a4; /* Niebieskoszary dla poprawnej odpowiedzi */
        border-left-color: #50fa7b; /* Zielony akcent */
        color: #f8f8f2;
    }
    .status-icon {
        margin-right: 8px;
        font-weight: bold;
    }
    .correct { color: #50fa7b; } /* Zielony dla poprawnego statusu */
    .incorrect { color: #ff5555; } /* Czerwony dla niepoprawnego statusu */
    .final-result {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        padding: 15px;
        margin: 25px 0;
        border-radius: 8px;
        line-height: 1.6; /* Dodano interlinię dla lepszej czytelności */
    }
    .passed {
        background: #283636; /* Ciemna zieleń dla zaliczonego */
        color: #50fa7b;      /* Jasnozielony tekst */
        border: 1px solid #50fa7b;
    }
    .failed {
        background: #443638; /* Ciemna czerwień dla niezaliczonego */
        color: #ff5555;      /* Jasnoczerwony tekst */
        border: 1px solid #ff5555;
    }
    .score {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #8be9fd; /* Jasnoniebieski dla wyniku */
        margin: 15px 0 25px 0; /* Zwiększono dolny margines */
    }
</style>
"""

## ===================================================================
## ===           ULEPSZONA FUNKCJA GENEROWANIA PODSUMOWANIA        ===
## ===================================================================

def generate_summary_html(user_answers, correct_answers, required_to_pass):
    """Generuje HTML podsumowania testu, uwzględniając próg zdawalności."""
    html = TEST_SUMMARY_STYLES
    total_questions = len(user_answers)
    html += f"""
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

        html += f"""
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
            html += f"""
            <div class="answer-section correct-answer">
                <strong>Poprawna odpowiedź:</strong>
                {format_answer(correct_answer, answer_type)}
            </div>
            """

        html += "</div>" # Koniec question-container

    # Dynamiczny komunikat zaliczenia/niezaliczenia
    if correct_answers >= required_to_pass:
        html += f"""
        <div class="final-result passed">
            🎉 Test zaliczony! Gratulacje! <br> (Wymagane minimum: {required_to_pass}/{total_questions})
        </div>
        """
    else:
        html += f"""
        <div class="final-result failed">
            ❌ Test niezaliczony. <br> Wymagane minimum {required_to_pass} poprawnych odpowiedzi z {total_questions}.
        </div>
        """

    return html

## ===================================================================
## ===              ULEPSZONA FUNKCJA FORMATOWANIA ODPOWIEDZI      ===
## ===================================================================

def format_answer(answer, answer_type):
    """Formatuje odpowiedź do wyświetlenia w HTML, dbając o kod."""
    # Używamy html.escape do zabezpieczenia przed XSS i poprawnego wyświetlania < >
    import html
    escaped_answer = html.escape(str(answer))

    if answer_type in ('code_input', 'code_output', 'reorder'):
        # Kod umieszczamy w tagach <pre><code> dla poprawnego formatowania
        return f"<pre><code>{escaped_answer}</code></pre>"
    elif answer_type == 'multiple_choice':
        # Dla wielokrotnego wyboru, pokazujemy tylko odpowiedź
        return f"<br>{escaped_answer}"
    else:
        # Dla innych typów lub nieznanych, po prostu pokazujemy tekst
        return f"<br>{escaped_answer}"
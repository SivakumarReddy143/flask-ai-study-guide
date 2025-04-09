def _format_quiz_with_reveal(quiz_data):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
        <script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
        <title>Interactive Quiz</title>
    </head>
    <body>
        <div class="score-bar" id="score-bar">
            Attempted: 0 / {total} | Score: 0
        </div>
        <div class="quiz-container">
            <h2 class="quiz-title">Interactive Quiz</h2>
    """.replace("{total}", str(len(quiz_data)))

    for i, question in enumerate(quiz_data, 1):
        html += f"""
            <div class="question">
                <h3>{i}. {question['question']}</h3>
                <div class="options">
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">A. {question['options'][0]}</div>
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">B. {question['options'][1]}</div>
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">C. {question['options'][2]}</div>
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">D. {question['options'][3]}</div>
                </div>
                <button class="reveal-btn" onclick="revealAnswer(this, '{question['correct_answer']}', '{question['explanation']}')">Reveal Answer</button>
                <div class="answer-section">
                    <div class="answer-header">Correct Answer</div>
                    <div class="answer-content">
                        <div class="correct-answer">{question['correct_answer']}</div>
                        <div class="explanation">{question['explanation']}</div>
                    </div>
                </div>
            </div>
        """

    html += """
        </div>
        <script>
            function selectOption(selected, correctAnswer) {
                const options = selected.parentElement.children;
                for (let option of options) {
                    option.classList.remove('selected-correct', 'selected-incorrect');
                }
                selected.classList.add(selected.innerText.includes(correctAnswer) ? 'selected-correct' : 'selected-incorrect');
            }

            function revealAnswer(button, correctAnswer, explanation) {
                const answerSection = button.nextElementSibling;
                answerSection.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return html
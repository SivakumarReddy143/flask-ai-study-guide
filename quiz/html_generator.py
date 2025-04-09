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
            <h2 style="color: #2196f3; text-align: center; margin-bottom: 30px;">Interactive Quiz</h2>
    """.replace("{total}", str(len(quiz_data)))

    for i, question in enumerate(quiz_data, 1):
        html += f"""
            <div class="question">
                <h3>Question {i}: {question['question']}</h3>
                <div class="options">
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">A. {question['options'][0]}</div>
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">B. {question['options'][1]}</div>
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">C. {question['options'][2]}</div>
                    <div class="option" onclick="selectOption(this, '{question['correct_answer']}')">D. {question['options'][3]}</div>
                </div>
                <button class="reveal-btn" onclick="revealAnswer(this, '{question['correct_answer']}', '{question['explanation']}')">Reveal Answer</button>
                <div class="answer-section">
                    <div class="answer-header">Correct Answer:</div>
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
                // Logic to handle option selection
            }
            function revealAnswer(button, correctAnswer, explanation) {
                // Logic to reveal the answer
            }
        </script>
    </body>
    </html>
    """
    return html
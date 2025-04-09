from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize ChatGroq with your API key and desired model
chat = ChatGroq(api_key=GROQ_API_KEY, model="gemma2-9b-it", temperature=1)  # Change model if needed

def generate_quiz(topic: str, difficulty: str, num_questions: int):
    prompt = f"""
Generate a quiz with {num_questions} multiple-choice questions on the topic "{topic}".
Difficulty level: {difficulty}.

For each question, provide:
- A question string.
- Four options labeled A, B, C, and D.
- The correct answer (the full text of one option).
- A brief explanation.

Return the quiz as a list of Python dictionaries in the following JSON format:

[
    {{
        "question": "What is ...?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option C",
        "explanation": "Explanation for why Option C is correct."
    }},
    ...
]

Only return the list in valid JSON format.
"""
    try:
        response = chat([HumanMessage(content=prompt)])
        quiz_data = eval(response.content)  # For simplicity, using eval() to parse the JSON-like string.
        return quiz_data
    except Exception as e:
        return [{
            "question": "Failed to generate quiz data.",
            "options": ["N/A", "N/A", "N/A", "N/A"],
            "correct_answer": "N/A",
            "explanation": str(e)
        }]
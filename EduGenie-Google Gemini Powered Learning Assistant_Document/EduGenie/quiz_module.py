"""
Quiz Module for EduGenie
Generates MCQ quizzes using Google Gemini API.
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-3.8-flash")


def clean_json_response(response_text: str) -> str:
    """
    Cleans the Gemini response to extract valid JSON.
    Handles cases where JSON is wrapped in Markdown code blocks.
    """
    cleaned = re.sub(r"```json\s*", "", response_text)
    cleaned = re.sub(r"```\s*", "", cleaned)
    cleaned = cleaned.strip()
    return cleaned


def generate_quiz(text: str) -> dict:
    """
    Generates exactly 3 MCQ questions based on the given topic or passage.
    """
    try:
        prompt = f"""You are EduGenie, a friendly AI learning assistant for students.
Generate exactly 3 multiple-choice questions based on the following topic or passage.

Each question must have:
- question: the question text
- options: exactly 4 options (A, B, C, D)
- correct_answer: the correct option text
- explanation: a short explanation of why the answer is correct

Return ONLY valid JSON in this exact format:
[
  {{
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "...",
    "explanation": "..."
  }}
]

Topic or passage: {text}"""

        response = model.generate_content(prompt)
        cleaned = clean_json_response(response.text)
        quiz_data = json.loads(cleaned)

        # Validate the structure
        if not isinstance(quiz_data, list) or len(quiz_data) != 3:
            return {"error": "Invalid quiz format received. Please try again."}

        for q in quiz_data:
            if not all(key in q for key in ["question", "options", "correct_answer", "explanation"]):
                return {"error": "Invalid quiz format received. Please try again."}
            if len(q["options"]) != 4:
                return {"error": "Invalid quiz format received. Please try again."}

        return {"quiz": quiz_data}

    except json.JSONDecodeError:
        return {"error": "Failed to parse quiz data. Please try again."}
    except Exception as e:
        return {"error": "Sorry, something went wrong while generating the quiz. Please try again."}

"""
Q&A Module for EduGenie
Handles answering student questions using Google Gemini API.
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-3.8-flash")


def answer_question(question: str) -> str:
    """
    Takes a student's question and returns an AI-generated answer.
    """
    try:
        prompt = f"""You are EduGenie, a friendly AI learning assistant for students.
Answer the following question accurately and concisely.
Use headings or bullet points when useful.
Avoid unnecessary information.
Make it easy for a student to understand.

Question: {question}"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return "Sorry, something went wrong while generating the answer. Please try again."
"""
Summary Module for EduGenie
Summarizes long educational text using Google Gemini API.
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


def summarize_text(text: str) -> str:
    """
    Takes a long educational paragraph and returns a concise summary.
    """
    try:
        prompt = f"""You are EduGenie, a friendly AI learning assistant for students.
Summarize the following educational text.

Provide:
- A short summary (2-3 sentences)
- Main points (as bullet points)
- Important concepts (as bullet points)

Retain important information while removing unnecessary repetition.

Text to summarize:
{text}"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return "Sorry, something went wrong while generating the summary. Please try again."

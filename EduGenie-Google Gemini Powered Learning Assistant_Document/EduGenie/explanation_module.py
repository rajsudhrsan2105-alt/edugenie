"""
Explanation Module for EduGenie
Explains difficult topics in simple language using Google Gemini API.
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


def explain_topic(topic: str) -> str:
    """
    Takes a topic and returns a simple, step-by-step explanation.
    """
    try:
        prompt = f"""You are EduGenie, a friendly AI learning assistant for students.
Explain the following topic in simple language.

Requirements:
- Assume the user is a student
- Start with a simple definition
- Explain step-by-step
- Give a simple example
- Use bullet points where useful
- Avoid unnecessarily technical language
- End with a short key-points section

Topic: {topic}"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return "Sorry, something went wrong while generating the explanation. Please try again."

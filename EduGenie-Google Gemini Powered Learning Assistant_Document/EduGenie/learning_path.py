"""
Learning Path Module for EduGenie
Generates personalized learning roadmaps using Google Gemini API.
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


def get_learning_recommendations(topic: str) -> str:
    """
    Takes a topic and generates a structured learning roadmap.
    """
    try:
        prompt = f"""You are EduGenie, a friendly AI learning assistant for students.
Create a structured learning roadmap for the following topic.

The roadmap must include:
1. Beginner level - topics and skills to start with
2. Intermediate level - what to learn next
3. Advanced level - mastery topics
4. Recommended order of learning
5. Approximate learning timeline (weeks/months)
6. Suggested resources (books, websites, courses)
7. Practice/project suggestions

Keep it practical and student-friendly.

Topic: {topic}"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return "Sorry, something went wrong while generating the learning path. Please try again."

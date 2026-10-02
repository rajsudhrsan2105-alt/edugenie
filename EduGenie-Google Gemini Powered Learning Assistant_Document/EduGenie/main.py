"""
EduGenie - Google Gemini Powered Learning Assistant
Main FastAPI application file.
Author: Rajsudharsan
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

# Import modules
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

# Initialize FastAPI app
app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")


# Pydantic Request Models
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="The text or topic input")


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/qa")
async def qa_endpoint(request: QuestionRequest):
    """Handle Q&A requests."""
    if not request.question.strip():
        return {"error": "Please enter a question."}
    answer = answer_question(request.question.strip())
    return {"answer": answer}


@app.post("/explain")
async def explain_endpoint(request: TextRequest):
    """Handle topic explanation requests."""
    if not request.text.strip():
        return {"error": "Please enter a topic to explain."}
    explanation = explain_topic(request.text.strip())
    return {"explanation": explanation}


@app.post("/quiz")
async def quiz_endpoint(request: TextRequest):
    """Handle quiz generation requests."""
    if not request.text.strip():
        return {"error": "Please enter a topic or passage for the quiz."}
    result = generate_quiz(request.text.strip())
    return result


@app.post("/summarize")
async def summarize_endpoint(request: TextRequest):
    """Handle text summarization requests."""
    if not request.text.strip():
        return {"error": "Please enter text to summarize."}
    summary = summarize_text(request.text.strip())
    return {"summary": summary}


@app.post("/learn/recommendations")
async def learn_endpoint(request: TextRequest):
    """Handle learning path requests."""
    if not request.text.strip():
        return {"error": "Please enter a topic to create a learning path."}
    roadmap = get_learning_recommendations(request.text.strip())
    return {"roadmap": roadmap}

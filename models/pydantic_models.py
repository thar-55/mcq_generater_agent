from pydantic import BaseModel, Field
from typing import List

class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str

class QuizOutput(BaseModel):
    description: str
    questions: List[MCQ]

from pydantic import BaseModel, Field, model_validator
from typing import List

class MCQ(BaseModel):
    question: str = Field(description="The MCQ question.")
    options: List[str] = Field(description="List of options for the MCQ.")
    answer: str = Field(description="The correct answer to the MCQ.")
    explanation: str = Field(description="Explanation for the correct answer.")

class QuizOutput(BaseModel):
    description: str = Field(description="Description of the quiz.")
    questions: List[MCQ] = Field(description="List of MCQ questions.")

    # Example of a model validator (replaces @root_validator)
    @model_validator(mode="after")
    def validate_quiz(self) -> "QuizOutput":
        if not self.questions:
            raise ValueError("At least one question is required.")
        return self

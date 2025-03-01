from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from models.pydantic_models import QuizOutput, MCQ

def generate_mcq_quiz(field: str, topics: list, difficulty: str, num_questions: int) -> QuizOutput:
    # Initialize LLM
    llm = OpenAI(api_key="sk-proj-aLk4mDveiPaL2h4PW40PT3BlbkFJomHOTOUvg2RdhwlCttOV")

    # Define prompt
    mcq_prompt = PromptTemplate(
        input_variables=["field", "topics", "difficulty", "num_questions"],
        template="Generate {num_questions} {difficulty} MCQ questions for the field of {field} on the topics: {topics}. Each question should have 4 options, a correct answer, and an explanation."
    )

    # Create chain
    mcq_chain = LLMChain(llm=llm, prompt=mcq_prompt)

    # Run chain
    quiz_text = mcq_chain.run(field=field, topics=", ".join(topics), difficulty=difficulty, num_questions=num_questions)

    # Parse quiz_text into QuizOutput (this is a placeholder; you'll need to implement parsing logic)
    quiz_output = QuizOutput(
        description=f"{difficulty} MCQ Quiz on {field}",
        questions=[
            MCQ(
                question="Sample Question",
                options=["Option 1", "Option 2", "Option 3", "Option 4"],
                answer="Option 1",
                explanation="This is the correct answer because..."
            )
        ]
    )
    return quiz_output

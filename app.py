import streamlit as st
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.llms import OpenAI
import pdfkit
import json
from pydantic import BaseModel, Field
from typing import List

# Define Pydantic Models
class TopicRequest(BaseModel):
    field: str = Field(..., title="Field of Study")

class TopicResponse(BaseModel):
    topics: List[str] = Field(..., title="List of Topics")

class MCQRequest(BaseModel):
    field: str
    topics: List[str]
    difficulty: str
    num_questions: int

class MCQResponse(BaseModel):
    questions: List[dict]

class PDFRequest(BaseModel):
    mcq_data: MCQResponse

# Initialize LLM
llm = OpenAI(temperature=0.7)

# Define Agent 1: Generate Popular Topics
def generate_topics(request: TopicRequest) -> TopicResponse:
    prompt = f"What are the top 5 most popular topics in {request.field}?"
    response = llm(prompt)
    return TopicResponse(topics=response.split("\n"))

topic_tool = Tool(name="Topic Generator", func=generate_topics, description="Generates top 5 topics for a given field.")

# Define Agent 2: Generate MCQ Quiz
def generate_mcq(request: MCQRequest) -> MCQResponse:
    prompt = f"Generate {request.num_questions} MCQs for {request.field} on topics {request.topics} with {request.difficulty} difficulty. Include explanations."
    response = llm(prompt)
    return MCQResponse(**json.loads(response))

mcq_tool = Tool(name="MCQ Generator", func=generate_mcq, description="Generates an MCQ quiz based on user input.")

# Define Agent 3: Convert MCQ to PDF
def generate_pdf(request: PDFRequest) -> str:
    pdf_content = """
    <html>
    <head><title>MCQ Exam</title></head>
    <body>
    <h1>Exam Description</h1>
    <p>Generated MCQ exam.</p>
    <h2>Questions</h2>
    """
    for i, q in enumerate(request.mcq_data.questions):
        pdf_content += f"<p><b>Q{i+1}:</b> {q['question']}</p>"
        for j, option in enumerate(q['options']):
            pdf_content += f"<p>{chr(65+j)}. {option}</p>"
    pdf_content += "<h2>Answers & Explanations</h2>"
    for i, q in enumerate(request.mcq_data.questions):
        pdf_content += f"<p><b>Q{i+1}:</b> {q['answer']} - {q['explanation']}</p>"
    pdf_content += "</body></html>"
    pdfkit.from_string(pdf_content, "mcq_exam.pdf")
    return "mcq_exam.pdf"

pdf_tool = Tool(name="PDF Generator", func=generate_pdf, description="Converts MCQ quiz to PDF.")

# Initialize Agents
agent = initialize_agent([topic_tool, mcq_tool, pdf_tool], llm, agent_type="planning")

# Streamlit UI
st.title("AI-Powered MCQ Generator")

if "step" not in st.session_state:
    st.session_state["step"] = 1

if st.session_state["step"] == 1:
    field = st.text_input("Enter your field of study:")
    if st.button("Next"):
        request = TopicRequest(field=field)
        st.session_state["field"] = field
        st.session_state["topics"] = agent.run("Topic Generator", request)
        st.session_state["step"] = 2

if st.session_state["step"] == 2:
    st.write("Select topics:")
    selected_topics = st.multiselect("", st.session_state["topics"].topics)
    custom_topic = st.text_input("Or add a custom topic:")
    if st.button("Next"):
        st.session_state["selected_topics"] = selected_topics + ([custom_topic] if custom_topic else [])
        st.session_state["step"] = 3

if st.session_state["step"] == 3:
    difficulty = st.selectbox("Select difficulty:", ["Easy", "Medium", "Hard"])
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=50, value=10)
    if st.button("Generate Quiz"):
        request = MCQRequest(
            field=st.session_state["field"], 
            topics=st.session_state["selected_topics"], 
            difficulty=difficulty, 
            num_questions=num_questions
        )
        st.session_state["mcq_quiz"] = agent.run("MCQ Generator", request)
        st.session_state["step"] = 4

if st.session_state["step"] == 4:
    st.write("Generated MCQ Quiz:")
    st.json(st.session_state["mcq_quiz"].dict())
    if st.button("Download PDF"):
        request = PDFRequest(mcq_data=st.session_state["mcq_quiz"])
        pdf_path = agent.run("PDF Generator", request)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="mcq_exam.pdf", mime="application/pdf")

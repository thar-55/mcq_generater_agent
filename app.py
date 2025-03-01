import streamlit as st
from agents.topic_generator import generate_topics
from agents.mcq_generator import generate_mcq_quiz
from agents.pdf_converter import generate_pdf
from models.pydantic_models import QuizOutput

# Streamlit App
st.title("AI-Powered MCQ Generator")

# Step 1: Field Input
field = st.text_input("Enter your field of study:")

if field:
    # Step 2: Generate Topics
    st.write("Generating popular topics...")
    topics_output = generate_topics(field)
    topics_list = topics_output.split(", ")

    # Display topics and allow custom input
    selected_topics = st.multiselect("Select topics or add your own:", topics_list)
    custom_topic = st.text_input("Add a custom topic:")
    if custom_topic:
        selected_topics.append(custom_topic)

    if selected_topics:
        # Step 3: Difficulty and Number of Questions
        difficulty = st.selectbox("Select difficulty:", ["Easy", "Medium", "Hard"])
        num_questions = st.number_input("Number of questions:", min_value=1, max_value=50, value=10)

        if st.button("Generate Quiz"):
            # Step 4: Generate MCQ Quiz
            quiz_output = generate_mcq_quiz(field, selected_topics, difficulty, num_questions)
            st.write("Quiz Generated!")

            # Step 5: Convert to PDF
            if st.button("Download PDF"):
                generate_pdf(quiz_output, "quiz.pdf")
                st.write("PDF generated and ready for download.")

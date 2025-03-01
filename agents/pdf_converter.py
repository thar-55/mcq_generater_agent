from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from models.pydantic_models import QuizOutput

def generate_pdf(quiz: QuizOutput, filename: str):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Add description
    c.drawString(50, 750, quiz.description)
    y = 730

    # Add questions
    for i, mcq in enumerate(quiz.questions):
        c.drawString(50, y, f"Q{i+1}: {mcq.question}")
        y -= 20
        for option in mcq.options:
            c.drawString(70, y, option)
            y -= 15
        y -= 10

    # Add answers and explanations
    c.drawString(50, y, "Answers and Explanations:")
    y -= 20
    for i, mcq in enumerate(quiz.questions):
        c.drawString(50, y, f"Q{i+1}: {mcq.answer} - {mcq.explanation}")
        y -= 20

    c.save()

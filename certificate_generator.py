from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_certificate(name, course, date, output_filename):
    # Create a new PDF canvas
    c = canvas.Canvas(output_filename, pagesize=letter)

    # Certificate content
    title = "Certificate of Completion"
    certificate_text = f"This certificate is awarded to {name} for completing the course {course}."
    date_text = f"Date: {date}"

    # Draw the certificate content on the canvas
    c.setFont("Helvetica-Bold", 30)
    c.drawString(150, 600, title)

    c.setFont("Helvetica", 20)
    c.drawString(100, 500, certificate_text)

    c.setFont("Helvetica", 14)
    c.drawString(100, 400, date_text)

    # Save the canvas to the PDF file
    c.save()

if __name__ == "__main__":
    # Replace the following variables with the desired content
    recipient_name = "John Doe"
    course_name = "Introduction to Python"
    completion_date = "July 19, 2023"
    output_file = "certificate.pdf"

    generate_certificate(recipient_name, course_name, completion_date, output_file)

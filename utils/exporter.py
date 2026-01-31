from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import datetime


def generate_pdf(score, matched, missing, summary, suggestions):

    os.makedirs("data", exist_ok=True)

    filename = f"data/report_{int(datetime.datetime.now().timestamp())}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    w, h = A4

    y = h - 40

    def write(text):
        nonlocal y
        c.drawString(40, y, text)
        y -= 18

        if y < 40:
            c.showPage()
            y = h - 40

    write("AI Resume Analyzer Report")
    write("=" * 50)

    write(f"Score: {score}%")
    write("")

    write("Matched Skills:")
    for s in matched:
        write(f"- {s}")

    write("")
    write("Missing Skills:")
    for s in missing:
        write(f"- {s}")

    write("")
    write("Summary:")
    write(summary)

    write("")
    write("Suggestions:")
    for s in suggestions:
        write(f"- {s}")

    c.save()

    return filename

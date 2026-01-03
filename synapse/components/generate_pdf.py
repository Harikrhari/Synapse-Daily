import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch


class GeneratePDF:
    def __init__(self):
        os.makedirs(f"data/NewsPaper/{datetime.now().strftime('%d-%m-%Y')}", exist_ok=True)
        self.canvas_obj = canvas.Canvas(f"data/NewsPaper/{datetime.now().strftime('%d-%m-%Y')}/Synapse {datetime.now().strftime('%d-%m-%Y')}.pdf", pagesize=A4)
        self.canvas_obj.setTitle(f"Synapse | {datetime.now().strftime('%d %B %Y')}")
        self.canvas_obj.setAuthor("Hema Kalyan")

    def coverpage(self):
        self.canvas_obj.drawImage("artifacts/cover.png", 0, 0, A4[0], A4[1])
        self.canvas_obj.setFont("Times-Roman", 20)
        self.canvas_obj.setFillColorRGB(0.48, 0.29, 0.21)  # #7A4A35

        y = (1950 - 170) * A4[1] / 3508
        self.canvas_obj.drawCentredString(A4[0]/2, y, datetime.now().strftime("%B %d, %Y"))
    
    def innerpage(self, title, content):
        self.canvas_obj.showPage()
        self.canvas_obj.drawImage("artifacts/background.png", 0, 0, A4[0], A4[1])
        styles = getSampleStyleSheet()
        title_para = Paragraph(f"<b>{title}</b>", styles["Heading1"])
        body_para = Paragraph(content, styles["Normal"])
        x = 60
        y = A4[1] - 80
        w = A4[0] - 120
        tw, th = title_para.wrap(w, A4[1])
        title_para.drawOn(self.canvas_obj, x, y - th)
        bw, bh = body_para.wrap(w, A4[1])
        body_para.drawOn(self.canvas_obj, x, y - th - 20 - bh)

    def save_pdf(self):
        self.canvas_obj.save()

if __name__ == "__main__":
    pdf = GeneratePDF()
    pdf.coverpage()
    pdf.innerpage("Google AI Overviews Raise Health Concerns", "Google’s AI summaries were found to provide misleading medical advice...")
    pdf.innerpage("Why Accuracy in AI Matters", "As AI systems increasingly influence decisions, accuracy and accountability become critical.")
    pdf.save_pdf()
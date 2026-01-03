import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from synapse.config.config import SynapseConfig
from reportlab.platypus import Paragraph
from synapse.utils.logger import get_logger
from reportlab.lib.styles import getSampleStyleSheet

logger = get_logger(__name__)

class GeneratePDF:
    def __init__(self, date):
        logger.info("PDF Generation Initiated")
        self.output_dir = SynapseConfig.OUTPUT_DIR
        self.date = datetime.strptime(date, "%Y-%m-%d")
        os.makedirs(f"{self.output_dir}/{self.date.strftime('%d-%m-%Y')}", exist_ok=True)
        try:
            self.canvas_obj = canvas.Canvas(f"{self.output_dir}/{self.date.strftime('%d-%m-%Y')}/Synapse {self.date.strftime('%d-%m-%Y')}.pdf", pagesize=A4)
            self.canvas_obj.setTitle(f"Synapse | {self.date.strftime('%d %B %Y')}")
            self.canvas_obj.setAuthor("Hema Kalyan")
        except Exception as e:
            logger.error(f"Failed to Initiate PDF: {str(e)}")
            raise

    def coverpage(self):
        try:
            self.canvas_obj.drawImage("artifacts/cover.png", 0, 0, A4[0], A4[1])
            self.canvas_obj.setFont("Times-Roman", 20)
            self.canvas_obj.setFillColorRGB(0.48, 0.29, 0.21)
            y = (1950 - 170) * A4[1] / 3508
            self.canvas_obj.drawCentredString(A4[0]/2, y, self.date.strftime("%B %d, %Y"))
            logger.info("Cover Page Created")
        except Exception as e:
            logger.error(f"Failed to Create Cover Page: {str(e)}")
            raise
    
    def innerpage(self, title, content):
        try:
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
            logger.info("Inner Page Created")
        except Exception as e:
            logger.error(f"Failed to Create Inner Page: {str(e)}")
            raise

    def save_pdf(self):
        try:
            self.canvas_obj.save()
            logger.info("PDF Saved")
        except Exception as e:
            logger.error(f"Failed to Save PDF: {str(e)}")
            raise
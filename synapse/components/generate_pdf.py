import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, PageBreak, NextPageTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from synapse.config.config import SynapseConfig
from synapse.utils.logger import get_logger

logger = get_logger(__name__)

class GeneratePDF:
    def __init__(self, date):
        self.date_obj = datetime.strptime(date, "%Y-%m-%d")
        self.output_dir = SynapseConfig.OUTPUT_DIR
        os.makedirs(f"{self.output_dir}/{self.date_obj.strftime('%d-%m-%Y')}", exist_ok=True)
        self.filename = f"{self.output_dir}/{self.date_obj.strftime('%d-%m-%Y')}/Synapse {self.date_obj.strftime('%d-%m-%Y')}.pdf"
        self.story = []
        
        
        self.styles = getSampleStyleSheet()

    def _draw_cover(self, canvas, doc):
        canvas.saveState()
        try:
            # Draw cover image
            # Check if file exists to avoid error if missing in test env
            if os.path.exists("artifacts/cover.png"):
                canvas.drawImage("artifacts/cover.png", 0, 0, A4[0], A4[1])
            
            # Draw Date
            canvas.setFont("Times-Roman", 20)
            canvas.setFillColorRGB(0.48, 0.29, 0.21)
            y = (1950 - 170) * A4[1] / 3508
            canvas.drawCentredString(A4[0]/2, y, self.date_obj.strftime("%B %d, %Y"))
        except Exception as e:
            logger.error(f"Error drawing cover: {e}")
        canvas.restoreState()

    def _draw_inner(self, canvas, doc):
        canvas.saveState()
        try:
            if os.path.exists("artifacts/background.png"):
                canvas.drawImage("artifacts/background.png", 0, 0, A4[0], A4[1])
        except Exception as e:
            logger.error(f"Error drawing background: {e}")
        canvas.restoreState()

    def coverpage(self):
        # Implicitly starts with first template (cover)
        # Switch to 'inner' template for subsequent pages
        self.story.append(NextPageTemplate('inner'))
        # Spacer was causing LayoutError because it was larger than the frame
        self.story.append(PageBreak())
        logger.info("Added Cover Page to story")

    def innerpage(self, title, content):
        # Add Title
        self.story.append(Paragraph(f"<b>{title}</b>", self.styles["Heading1"]))
        self.story.append(Spacer(1, 20))
        
        # Add Content
        # ReportLab Paragraph handles text wrapping automatically.
        # We need to convert newlines to <br/> for line breaks to be respected if needed.
        if content:
            processed_content = content.replace("\n", "<br/>")
            self.story.append(Paragraph(processed_content, self.styles["Normal"]))
        
        # Start next article on new page
        self.story.append(PageBreak())
        logger.info(f"Added Inner Page section: {title}")

    def save_pdf(self):
        try:
            doc = BaseDocTemplate(self.filename, pagesize=A4)
            doc.title = f"Synapse | {self.date_obj.strftime('%d %B %Y')}"
            doc.author = "Hema Kalyan"
            doc.subject = f"News for {self.date_obj.strftime('%d %B %Y')}"
            doc.creator = "Synapse Weekly"
            
            # Text Frame configuration
            frame_x = 60
            frame_y = 80
            frame_w = A4[0] - 120
            frame_h = A4[1] - 160 
            
            text_frame = Frame(frame_x, frame_y, frame_w, frame_h, id='normal', showBoundary=0)
            
            # Define Templates
            # 'cover' is the first one added, so it's the default start.
            cover_template = PageTemplate(id='cover', frames=[text_frame], onPage=self._draw_cover)
            inner_template = PageTemplate(id='inner', frames=[text_frame], onPage=self._draw_inner)
            
            doc.addPageTemplates([cover_template, inner_template])
            
            doc.build(self.story)
            logger.info(f"PDF Saved to {self.filename}")
        except Exception as e:
            logger.error(f"Failed to save PDF: {e}")
            raise
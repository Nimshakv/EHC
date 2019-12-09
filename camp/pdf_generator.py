from operator import itemgetter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
import os
from camp_reg import settings


class PdfGenerate:
    def __init__(self):
        # styles
        self.styles = getSampleStyleSheet()
        self.styleN = self.styles['Normal']
        self.styleN.wordWrap = 'CJK'
        self.styleH = self.styles['Heading1']
        self.styleH.alignment = TA_RIGHT
        self.styleH.fontName = 'Courier-Bold'
        self.styleH.fontSize = 13
        self.styleH.charSpace = 5
        self.styleH2 = self.styles['Heading2']
        self.styleH2.textColor = 'Red'
        self.styleH3 = self.styles['Heading3']
        self.styleH4 = self.styles['Heading4']
        self.story = []

    def AddLogo(self):
        # logo
        image = os.path.join(settings.BASE_DIR, 'static/images/ehc.gif')
        img = Image(image, width=200, height=150)

        # first heading
        h_list = [[Paragraph("Emirates Heritage Club", self.styleH), img, ""]]
        h_table = Table(h_list)
        h_table.setStyle(TableStyle([
            # ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGNMENT', (0, 0), (0, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        self.story.append(h_table)

    def AddTable(self, students, camp):
        # student list table
        colWidths = [50, 50, 50, 60, 50, 50, 50, 50, 50, 50, 50, 50, 50, 92]

        st_list = [[Paragraph("Name", self.styleH4), Paragraph("School", self.styleH4), Paragraph("Grade", self.styleH4),
                    Paragraph("Date Of Birth", self.styleH4), Paragraph("Contact Number", self.styleH4),
                    Paragraph("Student Email", self.styleH4),
                    Paragraph("Parent Name", self.styleH4), Paragraph("Address", self.styleH4),
                    Paragraph("Parent Mobile 1", self.styleH4),
                    Paragraph("Parent Mobile 2", self.styleH4), Paragraph("Parent Work Address", self.styleH4),
                    Paragraph("Parent work Mobile", self.styleH4),
                    Paragraph("Parent Email", self.styleH4), Paragraph("Student Photo", self.styleH4)]]
        for st in students:
            I = Image(st.picture)
            I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
            I.drawWidth = 1.25 * inch
            temp = [Paragraph(st.name, self.styleN), Paragraph(st.school, self.styleN), Paragraph(st.grade, self.styleN),
                    st.dob, Paragraph(st.contact, self.styleN), Paragraph(st.email, self.styleN),
                    Paragraph(st.parent.user.username, self.styleN), Paragraph(st.parent.address, self.styleN),
                    Paragraph(st.parent.mobile_1, self.styleN), Paragraph(st.parent.mobile_2, self.styleN),
                    Paragraph(st.parent.work_address, self.styleN), Paragraph(st.parent.work_mobile, self.styleN),
                    Paragraph(st.parent.email, self.styleN), I
                    ]
            st_list.append(temp)

        self.story.append(Paragraph(camp, self.styleH2))
        self.story.append(Paragraph(f'{len(st_list) - 1} Students', self.styleH3))

        t = Table(st_list, colWidths=colWidths)
        t.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        self.story.append(t)
        self.story.append(Spacer(1, 0.25 * inch))

    def AddResume(self, student):

        img = Image(student.picture, width=100, height=100)
        p = f"Name: {student.name} <br/>" \
            f"Gender: {student.gender} <br/>" \
            f"Camp: {student.camp} <br/>" \
            f"School: {student.school} <br/>" \
            f"Grade: {student.grade} <br/>" \
            f"Date Of Birth: {student.dob} <br/>" \
            f"Mobile Number: {student.contact} <br/>" \
            f"Email: {student.email} <br/>" \
            f"Parent Name: {student.parent.user.username} <br/>" \
            f"Address: {student.parent.address} <br/>" \
            f"Parent Mobile 1: {student.parent.mobile_1} <br/>" \
            f"Parent Mobile 2: {student.parent.mobile_2} <br/>" \
            f"Work Address: {student.parent.work_address} <br/>" \
            f"Work Mobile: {student.parent.work_mobile} <br/>" \
            f"Parent Email: {student.parent.email} <br/>" \
            f""

        para = Paragraph(p, style=self.styleN)
        h_list = [[img, para]]
        h_table = Table(h_list)
        h_table.setStyle(TableStyle([
            # ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
            # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (0, 0), 'TOP'),
            ('VALIGN', (-1, -1), (-1, -1), 'MIDDLE'),
        ]))



        self.story.append(h_table)



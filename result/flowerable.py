# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 22:12:31 2019

@author: AdeolaOlalekan
"""
#from .models import SESSION
import datetime
import os
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import SimpleDocTemplate,Paragraph, Spacer, Table#, BaseDocTemplate#, TableStyle 
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import io
from django.http import FileResponse
from result.utils import session
session = session()


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 11)
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawCentredString(4 *inch, .25*inch, text)
    canvas.drawString(6.8 * inch, 0.5 * inch, '/'+str(Class)+'/'+str(sheet))
    canvas.drawRightString(6.8 * inch, 0.5 * inch, tutor)
    canvas.drawString(0.5 * inch, 0.5 * inch, 'https://uqhs.herokuapp.com/'+str(datetime.datetime.today())+'/: {}'.format(session))
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.drawCentredString(2.5 * inch, 1.25 * inch, 'UMUL_QURA HIGH SCHOOL MARK_SHEETS')
    canvas.restoreState()

def logo(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 11)
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawCentredString(4 *inch, .25*inch, text)
    canvas.drawString(6.8 * inch, 0.5 * inch, '/'+str(Class)+'/'+str(sheet))
    canvas.drawRightString(6.8 * inch, 0.5 * inch, tutor)
    canvas.drawString(0.5 * inch, 0.5 * inch, 'https://uqhs.herokuapp.com/'+str(datetime.datetime.today())+'/: {}'.format(session))
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.drawImage(doc.watermark,83,760,width=68,height=57,mask='auto')
    canvas.drawCentredString(2.5 * inch, 1.25 * inch, 'UMUL_QURA HIGH SCHOOL MARK_SHEETS')
    #canvas.restoreState()


def broadsheet(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 11)
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawCentredString(5.75 *inch, .25*inch, text)
    canvas.drawString(8.3 * inch, 0.5 * inch, '/'+str(Class)+'/'+str(sheet))
    canvas.drawRightString(8.3 * inch, 0.5 * inch, tutor)
    canvas.drawString(0.5 * inch, 0.5 * inch, 'https://uqhs.herokuapp.com/'+str(datetime.datetime.today())+'/: {}'.format(session))
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.drawCentredString(2.5 * inch, 1.25 * inch, 'UMUL_QURA HIGH SCHOOL MARK_SHEETS')
    canvas.restoreState()

def logo2(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 11)
    page_num = canvas.getPageNumber()
    text = "Page #%s" % page_num
    canvas.drawCentredString(5.75 *inch, .25*inch, text)
    canvas.drawString(8.3 * inch, 0.5 * inch, '/'+str(Class)+'/'+str(sheet))
    canvas.drawRightString(8.3 * inch, 0.5 * inch, tutor)
    canvas.drawString(0.5 * inch, 0.5 * inch, 'https://uqhs.herokuapp.com/'+str(datetime.datetime.today())+'/: {}'.format(session))
    canvas.setStrokeGray(0.90)
    canvas.setFillGray(0.90)
    canvas.drawImage(doc.watermark,83,500,width=68,height=57,mask='auto')
    canvas.drawCentredString(2.5 * inch, 1.25 * inch, 'UMUL_QURA HIGH SCHOOL MARK_SHEETS')
    
    
    
def building(request, xy):
    global tutor, Class, sheet
    data = xy#broadsheet_data(request)
    elements = []
    styles = getSampleStyleSheet()
    #styleNormal = styles['Normal']
    title_style = styles['Heading1']
    title_style.alignment = 1#centered right 2 left 0
    title_style3 = styles['Heading3']
    title_style3.alignment = 1
    title_style4 = styles['Heading4']
    title_style4.alignment = 1
    title_style2 = styles['Heading5']
    title_style2.alignment = 1
    # PDF Text - Content
    Sum, mean, counts, Class, term, headers, sheet, tutor = data[1]
    elements.append(Paragraph('UMMUL-QURQH HIGH SCHOOL', title_style))
    elements.append(Paragraph('Arowona Bus-Stop, Akanran Road, Ibadan-Oyo state.', title_style3))
    elements.append(Paragraph('ummulqura@marktoob.com, ummulqr@yahoo.com', title_style4))
    elements.append(Paragraph('08053776177, 07042412052', title_style4))
    elements.append(Paragraph(sheet, title_style))
        
    #]# [(start_column, start_row), (end_column, end_row)]
    pdf_buffer = io.BytesIO()
    if sheet == 'BROADSHEET':
        x = [x*counts+x for x in range(4) if x !=0]
        t=Table(data[0],style=[
                    ('BOX',(0,0),(1,-1),2,colors.red),
                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ('FONTSIZE', (0, 0), (0, 2), 8),
                    ('GRID',(0,1),(17,counts),2,colors.green),#1st
                    ('GRID',(0,counts+2),(17,counts*2),2,colors.blue),#2nd
                    ('GRID',(0,counts*2+3),(17,counts*3+2),2,colors.red),#3rd
                    ('GRID',(0,counts*3+5),(17,-1),2,colors.khaki),#4th
                    ('BACKGROUND',(0,0),(17,0),colors.limegreen),#1st
                    ('BACKGROUND',(0,x[0]),(17,x[0]),colors.orange),#2nd
                    ('BACKGROUND',(0,x[1]),(17,x[1]),colors.lavender),#3rd
                    ('BACKGROUND', (0, x[2]), (17, x[2]), colors.pink),#4th
                    ('BACKGROUND', (1, 1), (1, -1), colors.lavender),#student_name
                    ('BACKGROUND', (14, 1), (17, -1), colors.orange),#Annual
                    ('BOX',(0,0),(-1,-1),2,colors.black),
                    ('GRID',(0,0),(-1,-1),0.5,colors.black),
                    ('VALIGN',(3,0),(3,0),'BOTTOM'),
                    ('BACKGROUND',(5,0),(5,-1),colors.khaki),#Arb
                    ('BACKGROUND',(9,0),(9,-1),colors.khaki),#Arb
                    ('BACKGROUND',(13,0),(13,-1),colors.khaki),#Arb
                    ('ALIGN',(3,1),(3,1),'CENTER'),
                    ('BACKGROUND',(14,1),(17,3),colors.beige),#1st 3
                    ('ALIGN',(3,2),(3,2),'LEFT'),
                    ])
        elements.append(t)
        elements.append(Spacer(inch, .25 * inch))
        elements.append(Paragraph('Teacher-in-charge:- {}'.format(tutor+' '+'---'+' '+'Sign: {}'.format('_____________')+'Date: {}'.format('________________')), title_style4))
        elements.append(Paragraph('No of students Examined: {}'.format(counts)+' '+'---'+' '+str('Total Scores: {}'.format(Sum)+' '+'---'+' '+'Average: {}'.format(mean)+'%'), title_style4))
        elements.append(Paragraph('Approved by: {}'.format('_________________________________')+'  '+'Sign: {}'.format('__________'+'Date: {}'.format('_________')), title_style4))

        archivo_pdf = SimpleDocTemplate(pdf_buffer, pagesize=(landscape(letter)), rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        archivo_pdf.watermark = os.path.join(settings.MEDIA_ROOT, 'static/result/iiro.jpg')
        archivo_pdf.title = "{Class}.pdf".format(Class=str(Class))
        archivo_pdf.build(elements, onFirstPage=logo2, onLaterPages=broadsheet)
    else:#]# [(start_column, start_row), (end_column, end_row)]
        if term == '3rd Term'+' MarkSheet' and len(headers) != 9:
            t=Table(data[0],style=[
                        
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('BACKGROUND', (1, 1), (1, -1), colors.lavender),
                        ('BACKGROUND',(0,0),(13,0),colors.limegreen),#1st
                        ('BACKGROUND',(12,1),(-1,-1),colors.orange),#1st
                        ('BACKGROUND',(5,1),(11,-1),colors.grey),#1st
                        ('BACKGROUND',(2,1),(4,-1),colors.khaki),#1st
                        ('BACKGROUND',(0,1),(0,-1),colors.limegreen),#1st
                        ])
        else:
            t=Table(data[0],style=[
                        ('BOX',(0,0),(-1,-1),2,colors.black),
                        ('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('BACKGROUND', (1, 1), (1, -1), colors.lavender),
                        ('BACKGROUND',(0,0),(9,0),colors.limegreen),#1st
                        ('BACKGROUND',(8,1),(-1,-1),colors.orange),#1st
                        ('BACKGROUND',(5,1),(7,-1),colors.grey),#1st
                        ('BACKGROUND',(2,1),(4,-1),colors.khaki),#1st
                        ('BACKGROUND',(0,1),(0,-1),colors.limegreen),#1st
                        ])
        elements.append(t)
        elements.append(Spacer(inch, .25 * inch))
        elements.append(Paragraph('Teacher-in-charge:- {}'.format(tutor+' '+'---'+' '+'Sign: {}'.format('_____________')+'Date: {}'.format('________________')), title_style4))
        elements.append(Paragraph('No of students Examined: {}'.format(counts)+' '+'---'+' '+str('Total Scores: {}'.format(Sum)+' '+'---'+' '+'Average: {}'.format(mean)+'%'), title_style4))
        elements.append(Paragraph('Approved by: {}'.format('_________________________________')+'  '+'Sign: {}'.format('__________'+'Date: {}'.format('_________')), title_style4))
        archivo_pdf = SimpleDocTemplate(pdf_buffer, pagesize=(A4), rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        archivo_pdf.watermark = os.path.join(settings.MEDIA_ROOT, 'static/result/iiro.jpg')
        archivo_pdf.title = "{Class}.pdf".format(Class=str(Class))
        archivo_pdf.build(elements, onFirstPage=logo, onLaterPages=add_page_number)
        #archivo_pdf.showPage()
    
    pdf_buffer.seek(0)
    return FileResponse(pdf_buffer, as_attachment=True, filename=str(Class)+'.pdf')






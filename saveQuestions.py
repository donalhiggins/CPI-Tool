import os
import json
import io

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import numpy as np
import pandas as pd


class saveQuestions():

    questionLoc = {(0, 0, 0) : (104.4, 507.5), (0, 0, 1) : (104.4, 495.5), (0, 1, 0) : (166.5, 484.5), (0, 1, 1) : (166.5, 472.5),
             (0, 2, 0) : (467.4, 498), (0, 2, 1) : (467.4, 486.5), (0, 3, 0) : (467.4, 464), (0, 3, 1) : (467.4, 452.5),
             (0, 4, 0) : (467.4, 430.7), (0, 4, 1) : (467.4, 417), (0, 5, 0) : (667.5, 428.7), (0, 5, 1) : (667.5, 417.5),
             (0, 6, 0) : (529.5, 404), (0, 6, 1) : (529, 394),
             (1, 0, 0) : (104.8, 414.8), (1, 0, 1) : (104.8, 403.8), (1, 1, 0) : (166.3, 392), (1, 1, 1) : (166.3, 380.5),
             (2, 0, 0) : (111, 336.7), (2, 0, 1) : (111, 325.8), (2, 1, 0) : (217.5, 307.4), (2, 1, 1) : (217.5, 296.4),
             (3, 0, 0) : (103.5, 274), (3, 0, 1) : (103.5, 263), (3, 1, 0) : (169, 251), (3, 1, 1) : (169, 240.5),
             (4, 0, 0) : (104, 218), (4, 0, 1) : (104, 207),
             (5, 0, 0) : (104, 175), (5, 0, 1) : (104, 164), (5, 1, 0) : (272.5, 155), (5, 1, 1) : (272.5, 144),
             (6, 0, 0) : (104, 123), (6, 0, 1) : (104, 110), (6, 1, 0) : (272, 95), (6, 1, 1) : (272, 84),
             (7, 0, 0) : (464, 357.5), (7, 0, 1) : (464, 346.8), (7, 1, 0) : (647, 348.3), (7, 1, 1) : (647, 337.8),
             (8, 0, 0) : (463, 317.5), (8, 0, 1) : (463, 306.8), (8, 1, 0) : (524.3, 298), (8, 1, 1) : (524.3, 287.5),
             (9, 0, 0) : (463.5, 253.5), (9, 0, 1) : (463.5, 242.8), (9, 1, 0) : (524.3, 234), (9, 1, 1) : (524.3, 223.5),
             (10, 0, 0) : (464, 197), (10, 0, 1) : (464, 187), (10, 1, 0) : (653, 189), (10, 1, 1) : (653, 178.5),
             (11, 0, 0) : (466.2, 134.3), (11, 0, 1) : (466.2, 123.8),
             (12, 0, 0) : (466.2, 87), (12, 0, 1) : (466.2, 76.5),
             (13, 0, 0) : (149, 35), (13, 0, 1) : (149, 24), (14, 0, 0) : (376, 40), (14, 0, 1) : (376, 29),
             (14, 1, 0) : (573, 28), (14, 1, 1) : (573, 17)}

    def __init__(self):
        self.progress = pd.DataFrame(columns=['Map Number', 'Map', 'Question Number', 'Question', 'Answer', 'Flag', 'Critical'])
        self.skipped = pd.DataFrame(columns=['SMap Number', 'SQuestion Number', 'SQuestion', 'SFlag'])

    def addQuestion(self, mapnum, map, questnum, question, ans, flg=np.nan, crit=np.nan):
        self.progress = self.progress.append({'Map Number' : mapnum, 'Map' : map, 
                                              'Question Number' : questnum, 'Question' : question,
                                              'Answer' : ans, 'Flag' : flg,
                                              'Critical' : crit},
                                               ignore_index=True)

    def addSkip(self, questnum, mapnum, quest, flg):
        self.skipped = self.skipped.append({'SMap Number' : mapnum, 'SQuestion Number' : questnum, 'SQuestion' : quest, 'SFlag' : flg}, ignore_index=True)

    def resumeLastQuestion(self):
        return (self.progress['Map Number'].iloc[-1], self.progress['Question Number'].iloc[-1], self.progress['Answer'].iloc[-1])
    
    def skipList(self):
        temp = []
        for index, rows in self.skipped.iterrows():
            temp1 = [int(rows[0]), int(rows[1])]
            temp.append(temp1)
        return temp

    def flagList(self):
        temp = []
        for index, rows in self.progress.iterrows():
            if not np.isnan(rows['Flag']):
                temp.append([rows['Question'], rows['Flag']])
        for index, rows in self.skipped.iterrows(): 
            if rows['SFlag'] != '':
                temp.append([rows['SQuestion'], rows['SFlag']])
        return temp
    
    def critList(self):
        temp = []
        for index, rows in self.progress.iterrows():
            if type(rows['Critical']) is str:
                temp.append([rows['Question'], rows['Critical']])
        return temp

    def readData(self, file):
        self.progress = pd.read_csv(f'Reports/{file}/{file}.cpi')
        self.skipped = self.progress[['SMap Number', 'SQuestion Number', 'SQuestion', 'SFlag']]
        self.skipped = self.skipped[self.skipped['SQuestion Number'].notnull()]
        self.progress = self.progress.drop(['SMap Number', 'SQuestion Number', 'SQuestion', 'SFlag'], axis=1)
        self.progress = self.progress[self.progress['Question'].notna()]
        self.progress[['Map Number', 'Question Number']] = self.progress[['Map Number', 'Question Number']].astype('int')

    def addFlag(self, flglst):
        self.progress.loc[self.progress['Question'] == flglst[0], ['Flag']] = flglst[1]

    def addCrit(self, critlst):
        self.progress.loc[self.progress['Question'] == critlst[0], ['Critical']] = critlst[1]
        
    def mergeFlgCrit(self, flglst, critlst):
        for i in flglst:
            temp = i[0]
            self.progress.loc[self.progress['Question'] == temp, ['Flag']] = i[1]
        for i in critlst:
            temp = i[0]
            self.progress.loc[self.progress['Question'] == temp, ['Critical']] = i[1]

    def createSaveFile(self, name, new):
        if new:
            os.mkdir(f'Reports/{name}')
        self.progress = pd.concat([self.progress, self.skipped])
        self.progress.to_csv(f'Reports/{name}/{name}.cpi')

    def genPDF(self, name, text):
        packet = io.BytesIO()
        stringPacket = io.BytesIO()
        img = 'src/black.jpeg'
        can = canvas.Canvas(packet, pagesize=letter)
        questions = self.progress[['Map Number', 'Question Number', 'Answer']].dropna()
        for index, rows in questions.iterrows():
            ans = 0 if rows['Answer'] == 'n' else 1
            x = self.questionLoc[(rows['Map Number'], rows['Question Number'], ans)][0]
            y = self.questionLoc[(rows['Map Number'], rows['Question Number'], ans)][1]
            can.drawImage(img, x, y, width=15, height=8)
        can.save()

        packet.seek(0)

        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open('src/CPI Form.pdf', 'rb'))
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

        if text != '':
            textcan = canvas.Canvas(stringPacket, pagesize=(792, 612))
            textobj = textcan.beginText(10, 550)
            textobj.setFont('Times New Roman', 12)
            text = text.split('\n')
            for line in text:
                textobj.textLine(line)
            textcan.drawText(textobj)
            textcan.save()
            stringPacket.seek(0)
            text_page = PdfFileReader(stringPacket)
            output.addPage(text_page.getPage(0))

        outputFile = open(f'Reports/{name}/{name}.pdf', 'wb')
        output.write(outputFile)
        outputFile.close()

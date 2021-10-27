import os

import numpy as np
import pandas as pd
from PIL import Image


class saveQuestions():
    
    # TODO get image for questions and add
    # img = Image.open
    def __init__(self):
        self.progress = pd.DataFrame(columns=['Map Number', 'Map', 'Question Number', 'Question', 'Answer', 'Flag', 'Critical'])
        self.skipped = pd.DataFrame(columns=['SMap Number', 'SQuestion'])

    def addQuestion(self, mapnum, map, questnum, question, ans, flg=np.nan, crit=np.nan):
        self.progress = self.progress.append({'Map Number' : mapnum, 'Map' : map, 
                                              'Question Number' : questnum, 'Question' : question,
                                              'Answer' : ans, 'Flag' : flg,
                                              'Critical' : crit},
                                               ignore_index=True)

    def addSkip(self, quest, mapnum):
        self.skipped = self.skipped.append({'SMap Number' : mapnum, 'SQuestion' : quest}, ignore_index=True)

    def resumeLastQuestion(self):
        return (self.progress['Map Number'].iloc[-1], self.progress['Question Number'].iloc[-1], self.progress['Answer'].iloc[-1])
    
    def skipList(self):
        temp = []
        for index, rows in self.skipped.iterrows():
            temp1 = [int(rows[0]), int(rows[1])]
            temp.append(temp1)
        return temp

    def readData(self, file):
        self.progress = pd.read_csv(f'Reports/{file}/{file}.csv')
        self.skipped = self.progress[['SMap Number', 'SQuestion']]
        self.skipped = self.skipped.dropna()
        self.progress = self.progress.drop(['SMap Number', 'SQuestion'], axis=1)
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
        self.progress.to_csv(f'Reports/{name}/{name}.csv')

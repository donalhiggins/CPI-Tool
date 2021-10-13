from PIL import Image
import numpy as np
import pandas as pd
import os

class saveQuestions():
    
    # TODO get image for questions and add
    # img = Image.open
    def __init__(self):
        self.progress = pd.DataFrame(columns=['Map Number', 'Map', 'Question Number', 'Question', 'Answer', 'Flag', 'Critical'])
        
    def addQuestion(self, mapnum, map, questnum, question, ans, flg=np.nan, crit=np.nan):
        self.progress = self.progress.append({'Map Number' : mapnum, 'Map' : map, 
                                              'Question Number' : questnum, 'Question' : question,
                                              'Answer' : ans, 'Flag' : flg,
                                              'Critical' : crit},
                                               ignore_index=True)

    def resumeLastQuestion(self):
        return (self.progress['Map Number'].iloc[-1], self.progress['Question Number'].iloc[-1], self.progress['Answer'].iloc[-1])
    
    def readData(self, file):
        self.progress = pd.read_csv(f'Reports/{file}/{file}.csv')
    
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
        self.progress.to_csv(f'Reports/{name}/{name}.csv')



    

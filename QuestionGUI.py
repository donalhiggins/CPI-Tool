import tkinter as tk
import tkinter
from idlelib.tooltip import Hovertip
import threading
from tkinter import simpledialog

class QuestionGUI(threading.Thread):
    flags = []
    question = 'temp_question'
    info = 'temp_info'
    questionText = None
    isChange = False
    maptype = 'temp'
    answer = False
    answered = False
    critical = []

    def __init__(self):
        t1 = threading.Thread(target=self.createGUI)
        t1.start()
        

    def createGUI(self):
        #CREATE root
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.callback)
        self.logo = tk.PhotoImage(file='trigon.png')
        self.root.iconphoto(False, self.logo)
        self.root.title('CPI Tool')
        self.root.geometry('1280x720')

        #CREATE INFO BUTTON
        self.infobtn = tk.PhotoImage(file='info.png')
        self.tipbutton = tk.Button(self.root, image=self.infobtn)
        self.tip = Hovertip(self.tipbutton, self.info, hover_delay=500)

        #CREATE FLAG BUTTON
        self.flagbtn = tk.PhotoImage(file='flag.png')
        self.flagbutton = tk.Button(self.root, image=self.flagbtn, command=self.flag)

        #CREATE YES/NO BUTTONS
        self.yesbutton = tk.Button(self.root, text='Yes', font=('Times New Roman', 14), command=self.yesButton)
        self.nobutton = tk.Button(self.root, text='No', font=('Times New Roman', 14), command=self.noButton)

        #CREATE TITLE AND QUESTION
        self.mapheader = tk.Label(self.root, text=self.maptype, font=('Times New Roman', 24, 'bold'))
        self.questionText = tk.Label(self.root, text='', font=('Times New Roman', 14))

        #ARRANGE ELEMENTS
        self.mapheader.place(x=0, y=0)
        self.questionText.place(x=10, y=40)
        self.tipbutton.place(x=100, y=40)
        self.yesbutton.place(x=40, y=80)
        self.nobutton.place(x=85, y=80)
        self.flagbutton.place(x=125, y=80)

        #UPDATE GUI
        self.updateGUI()
        
        self.root.mainloop()

    def updateGUI(self):
        if self.isChange:
            self.questionText.config(text=self.question)
            self.mapheader.config(text=self.maptype)
            self.tip.text = self.info

        self.root.after(1000, self.updateGUI)

    def callback(self):
        self.root.quit()

    def flag(self):
        self.flags.append(simpledialog.askstring(title='Flag', prompt='Why?'))
        return None
        
    def yesButton(self):
        self.answer = True
        self.answered = True
        self.getAnswer()

    def noButton(self):
        self.answer = False
        self.answered = True
        self.getAnswer()

    def getAnswer(self):
        return self.answer

    def updateQuestion(self, quest, inf, mapt=maptype):
        self.isChange = True
        self.question = quest
        self.info = inf
        self.maptype = mapt

    def addCritical(self, questnum):
        self.critical.append(questnum)
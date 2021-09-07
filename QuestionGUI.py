import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
from ttkthemes import ThemedTk
import json

class QuestionGUI():
    flags = []
    critTrack = ''
    question = 'temp_question'
    info = 'temp_info'
    isChange = False
    maptype = 'temp_map'
    critical = []
    questions = {}
    maps = []
    output = 0
    mapnum = 0

    def __init__(self):
        # READS IN DICTIONARY AND LIST FOR QUESTIONS
        with open('maps_list.txt') as myFile:
            self.maps = myFile.readline().split(',')
        with open('questions_dict.txt') as myFile:
            self.questions = myFile.read()
        self.questions = json.loads(self.questions)
        self.maptype = self.maps[self.mapnum]
        self.question = self.questions[self.maptype][0][0]

        self.createGUI()

    def createGUI(self):
        # CREATE root
        self.root = ThemedTk(theme='arc')
        self.root['background'] = '#f5f6f7'
        self.logo = tk.PhotoImage(file='trigon.png')
        self.root.iconphoto(True, self.logo)
        self.root.title('CPI Tool')
        self.root.geometry('1280x720')

        # CREATE INFO BUTTON
        self.infobtn = tk.PhotoImage(file='info.png')
        self.tipbutton = ttk.Button(self.root, image=self.infobtn)
        self.tip = Hovertip(self.tipbutton, self.info, hover_delay=500)

        # CREATE FLAG BUTTON
        self.flagbtn = tk.PhotoImage(file='flag.png')
        self.flagbutton = ttk.Button(self.root,
                                     image=self.flagbtn,
                                     command=self.flagWindow)

        # CREATE YES/NO BUTTONS
        self.yesbutton = ttk.Button(self.root,
                                    text='Yes', command=self.yesButton)
        self.nobutton = ttk.Button(self.root, text='No', command=self.noButton)

        # CREATE TITLE AND QUESTION
        self.mapheader = ttk.Label(self.root,
                                   text=self.maptype,
                                   font=('Times New Roman', 24, 'bold'))
        self.questionText = ttk.Label(self.root,
                                      text=self.question, font=('Times New Roman', 14),
                                      wraplength=1200)

        # ARRANGE ELEMENTS
        self.mapheader.place(x=10, y=0)
        self.questionText.place(x=10, y=40)
        self.tipbutton.place(x=265, y=100)
        self.yesbutton.place(x=30, y=100)
        self.nobutton.place(x=115, y=100)
        self.flagbutton.place(x=210, y=100)

        # UPDATES GUI
        self.updateGUI()

        self.root.mainloop()

    def updateGUI(self):
        # CHECKS IF A CHANGE IS NEEDED AND THEN EDITS GUI
        if self.isChange:
            self.questionText.config(text=self.question)
            self.mapheader.config(text=self.maptype)
            self.tip.text = self.info    
            # IF HITS CRITICAL / OK GOES TO NEXT MAP   
            if not isinstance(self.output, int):
                if self.mapnum == 14:
                    print(self.flags)
                self.addCritical()
                self.mapnum += 1
                self.maptype = self.maps[self.mapnum]
                self.output = 0
                self.question = self.questions[self.maptype][0][0]
            else:
                self.critTrack = self.question

        self.root.after(100, self.updateGUI)

    def flagWindow(self):
        self.window = tk.Toplevel(self.root)
        self.entry = tk.StringVar()
        self.window.title('Flag')
        ttk.Label(self.window, text='Why did you flag this?',
                  font=('Times New Roman', 14)).pack()
        ttk.Entry(self.window, textvariable=self.entry).pack()
        ttk.Button(self.window, text='Ok', command=self.closeFlagWindow).pack()

    def closeFlagWindow(self):
        self.flags.append(self.entry.get())
        self.window.destroy()

    def yesButton(self):
        self.isChange = True
        self.output = self.questions[self.maptype][self.output][1][1]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]
        
    def noButton(self):
        self.isChange = True
        self.output = self.questions[self.maptype][self.output][1][0]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]

    def updateQuestion(self, quest, inf, mapt):
        self.isChange = True
        self.question = quest
        self.info = inf
        self.maptype = mapt

    def addCritical(self):
        if self.output == 'Critical':
            self.critical.append(self.critTrack)

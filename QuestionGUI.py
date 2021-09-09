import tkinter as tk
from tkinter import ttk
from tkinter.constants import LEFT, RIGHT, TOP
from idlelib.tooltip import Hovertip
from ttkthemes import ThemedTk
import json
from PIL import ImageTk, Image

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
    skippedQuestions = []
    isSkip = False
    endString = ''
    testName = ''

    def __init__(self):
        # READS IN DICTIONARY AND LIST FOR QUESTIONS
        with open('maps_list.txt') as myFile:
            self.maps = myFile.readline().split(',')
        with open('questions_dict.txt') as myFile:
            self.questions = myFile.read()
        self.questions = json.loads(self.questions)
        self.maptype = self.maps[self.mapnum]
        self.question = self.questions[self.maptype][0][0]
        
        # CREATES root AND WELCOME WIDGETS
        self.root = ThemedTk(theme='arc')
        self.name = tk.StringVar()
        self.welcome = ttk.Label(self.root, text='Trigon Cyber CPI Tool', font=('Times New Roman', 30, 'bold'))
        self.startbutton = ttk.Button(self.root, text='Start', command=self.createGUI)
        self.enterName = ttk.Label(self.root, text='Enter the name of the utility you are testing.', font=('Times New Roman', 18))
        self.nameBox = ttk.Entry(self.root, textvariable=self.name)
        self.bigPhoto = ImageTk.PhotoImage(Image.open('bigtrigon.jpeg'))
        self.biglogo = ttk.Label(self.root, image=self.bigPhoto)
        self.startPage()
    
    def startPage(self):
        # DECORATES root WITH WELCOME WIDGETS
        self.root['background'] = '#f5f6f7'
        self.logo = tk.PhotoImage(file='trigon.png')
        self.root.iconphoto(True, self.logo)
        self.root.title('CPI Tool')
        self.root.geometry('1280x720')
        self.welcome.grid(row=0,column=0)
        self.enterName.grid(row=1,column=0)
        self.nameBox.grid(row=2,column=0)
        self.startbutton.grid(row=3,column=0)
        self.biglogo.grid(row=4,column=0)
        self.root.mainloop()

    def createGUI(self):
        # REMOVE START SCREEN
        self.testName = self.name.get()
        self.welcome.destroy()
        self.startbutton.destroy()
        self.biglogo.destroy()
        self.enterName.destroy()
        self.nameBox.destroy()

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
                                   font=('Times New Roman', 30, 'bold'))
        self.questionText = ttk.Label(self.root,
                                      text=self.question, font=('Times New Roman', 16),
                                      wraplength=1200)

        # ARRANGE ELEMENTS 
        self.mapheader.grid(row=0, column=0, pady=10, padx=5, columnspan=1000, sticky=tk.N+tk.S+tk.W+tk.E)
        self.questionText.grid(row=1, column=0, pady=10, padx=10, columnspan=1000, rowspan=2, sticky=tk.N+tk.S+tk.W+tk.E)
        self.tipbutton.grid(row=3, column=3, padx=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.yesbutton.grid(row=3, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        self.nobutton.grid(row=3, column=1, padx=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.flagbutton.grid(row=3, column=2, sticky=tk.N+tk.S+tk.W+tk.E)

        # UPDATES GUI
        self.updateGUI()

    def updateGUI(self):
        try:
            # CHECKS IF A CHANGE IS NEEDED AND THEN EDITS GUI
            if self.isChange:
                self.questionText.config(text=self.question)
                self.mapheader.config(text=self.maptype)
                self.tip.text = self.info    
                # IF HITS CRITICAL / OK GOES TO NEXT MAP AND SKIPS IF NEEDED
                if not isinstance(self.output, int) or self.isSkip:
                    if self.mapnum == 14:
                        if len(self.skippedQuestions) == 0:
                            self.endBox()
                        else:
                            self.endBox()
                    else:
                        self.addCritical()
                        self.mapnum += 1
                        self.maptype = self.maps[self.mapnum]
                        self.output = 0
                        self.question = self.questions[self.maptype][0][0]
                        self.isSkip = False
                else:
                    self.critTrack = self.question
        except tk.TclError:
            self.file = open(self.testName, 'w')
            self.file.write(self.endString)

        self.root.after(100, self.updateGUI)

    def flagWindow(self):
        self.window = tk.Toplevel(self.root, bg='#f5f6f7')
        self.entry = tk.StringVar()
        self.window.title('Flag')
        ttk.Label(self.window, text='Why did you flag this?',
                  font=('Times New Roman', 14)).pack()
        ttk.Entry(self.window, textvariable=self.entry).pack(side=TOP)
        ttk.Button(self.window, text='Skip', command=self.skip).pack(side=RIGHT)
        ttk.Button(self.window, text='Ok', command=self.closeFlagWindow).pack(side=LEFT)

    def closeFlagWindow(self):
        self.flags.append([self.question, self.entry.get()])
        self.window.destroy()

    def critWindow(self):
        self.window = tk.Toplevel(self.root, bg='#f5f6f7')
        self.entry = tk.StringVar()
        self.window.title('Critical')
        ttk.Label(self.window, text=('Why was this critical? Question: ' + self.critTrack),
                  font=('Times New Roman', 14)).pack()
        ttk.Entry(self.window, textvariable=self.entry).pack()
        ttk.Button(self.window, text='Ok', command=self.closeCritWindow).pack()
        self.root.wait_window(self.window)

    def skip(self):
        self.flags.append([self.question, self.entry.get()])
        self.skippedQuestions.append([self.mapnum, self.output])
        self.isChange = True
        self.isSkip = True
        self.window.destroy()

    def closeCritWindow(self):
        self.critical.append([self.critTrack, self.entry.get()])
        self.window.destroy()

    def addCritical(self):
        if self.output == 'Critical':
            self.critWindow()

    def yesButton(self):
        self.isChange = True
        if isinstance(self.output, int):
            self.output = self.questions[self.maptype][self.output][1][1]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]
        
    def noButton(self):
        self.isChange = True
        if isinstance(self.output, int):
            self.output = self.questions[self.maptype][self.output][1][0]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]

    def parseInfo(self):
        self.endString = 'Flagged Questions:\n'
        for i in self.flags:
            self.endString = self.endString + i[0] + ' : ' + i[1] + '\n'
        self.endString = self.endString + '\nCritical Questions:\n'
        for i in self.critical:
            self.endString = self.endString + i[0] + ' : ' + i[1] + '\n'
        self.testName = "Results/" + self.testName.replace(' ', '_') + '.txt'

    def endBox(self):
        self.root.destroy()
        self.end = ThemedTk(theme='arc').title('End Screen')
        self.parseInfo()
        self.TextBox = ttk.Label(self.end, text=self.endString, font=('Times New Roman', 16)).pack()
        self.file = open(self.testName, 'x')
        self.file.write(self.endString)

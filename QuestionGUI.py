import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter.constants import LEFT, RIGHT, TOP

from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk
from ttkthemes import ThemedTk

from saveQuestions import saveQuestions


class QuestionGUI():
    save = saveQuestions()
    answer = ''
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
    skippedQuest = False
    isSkip = False
    skipCount = 0
    endString = ''
    testName = ''
    saveFile = ''
    fromSave = False
    isNew = False

    def __init__(self):
        # READS IN DICTIONARY AND LIST FOR QUESTIONS
        with open('maps_list.txt', encoding='utf8') as myFile:
            self.maps = myFile.readline().split(',')
        with open('questions_dict.txt', encoding='utf8') as myFile:
            self.questions = myFile.read()
        self.questions = json.loads(self.questions)
        self.maptype = self.maps[self.mapnum]
        self.question = self.questions[self.maptype][0][0]
        self.info = self.questions[self.maptype][0][2]
        self.info = self.wrapinfo(self.info)

        # CREATES LIST OF POSSBILE FILES TO RESUME
        self.savedFiles = os.listdir('Reports/')
        
        # CREATES root AND WELCOME WIDGETS
        self.root = ThemedTk(theme='arc')
        self.name = tk.StringVar()
        self.welcome = ttk.Label(self.root, text='Trigon Cyber CPI Tool',
                                 font=('Times New Roman', 30, 'bold'))
        self.startbutton = ttk.Button(self.root,
                                      text='Start', command=self.startQuestions)
        self.enterName = ttk.Label(self.root,
                                   text='Enter the name of the utility you are testing.',
                                   font=('Times New Roman', 18))
        self.nameBox = ttk.Entry(self.root, textvariable=self.name)
        self.bigPhoto = ImageTk.PhotoImage(Image.open('bigtrigon.jpeg'))
        self.biglogo = ttk.Label(self.root, image=self.bigPhoto)
        self.instructionButton = ttk.Button(self.root,
                                            text='Help',
                                            command=self.displayHelp)
        self.DropDown = tk.StringVar(self.root)
        self.DropDown.set('Select a save')
        self.savedFiles.insert(0, 'Select a save')
        self.savedFiles.append('Select a save')
        
        self.savedList = ttk.OptionMenu(self.root, self.DropDown, *self.savedFiles)
        self.startPage()

    def startPage(self):
            
        # DECORATES root WITH WELCOME WIDGETS
        self.root['background'] = '#f5f6f7'
        self.logo = tk.PhotoImage(file='trigon.png')
        self.root.iconphoto(True, self.logo)
        self.root.title('CPI Tool')
        self.root.geometry('1280x720')

        self.welcome.grid(row=0, column=0)
        self.enterName.grid(row=1, column=0)
        self.nameBox.grid(row=2, column=0)
        self.startbutton.grid(row=3, column=0)
        self.biglogo.grid(row=4, column=0)
        self.instructionButton.grid(row=3, column=1)
        self.savedList.grid(row=3,  column=2)
        self.root.mainloop()

    def displayHelp(self):
        # CREATE TOPLEVEL WINDOW
        self.helpWindow = tk.Toplevel(self.root, bg='#f5f6f7')

        # CREATE WIDGETS
        self.instructionLabel = ttk.Label(self.helpWindow,
                                        text='Instructions',
                                        font=('Times New Roman', 24))

        # TODO FILL OUT INSTRUCTIONS WITH THE INFO NEEDED
        self.instructions = ttk.Label(self.helpWindow,
                                      text='The CPI Tool is used to fill out the CPI form. For this ... cont') 
        self.back = ttk.Button(self.helpWindow,
                               text='Back',
                               command=self.helpWindow.destroy)

        self.instructionLabel.grid(row=0, column=0)
        self.instructions.grid(row=1, column=0)
        self.back.grid(row=2, column=0)

    def startQuestions(self):
        # REMOVE START SCREEN
        self.saveFile = self.DropDown.get()
        self.testName = self.name.get()
        self.welcome.destroy()
        self.startbutton.destroy()
        self.biglogo.destroy()
        self.enterName.destroy()
        self.nameBox.destroy()
        self.instructionButton.destroy()
        self.checkSave()

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

        # CREATE PAUSE/EXIT BUTTON
        self.pauseButton = ttk.Button(self.root,
                                      text='Pause', command=self.pause)

        # CREATE TITLE AND QUESTION
        self.mapheader = ttk.Label(self.root,
                                   text=self.maptype,
                                   font=('Times New Roman', 30, 'bold'))
        self.questionText = ttk.Label(self.root,
                                      text=self.question,
                                      font=('Times New Roman', 16),
                                      wraplength=1200)

        # ARRANGE ELEMENTS
        self.mapheader.grid(row=0, column=0,
                            pady=10, padx=5,
                            columnspan=1000, sticky=tk.N+tk.S+tk.W+tk.E)
        self.questionText.grid(row=1, column=0,
                               pady=10, padx=10,
                               columnspan=1000, rowspan=2,
                               sticky=tk.N+tk.S+tk.W+tk.E)
        self.tipbutton.grid(row=3, column=2,
                            sticky=tk.N+tk.S+tk.W+tk.E)
        self.yesbutton.grid(row=3, column=0,
                            sticky=tk.N+tk.S+tk.W+tk.E)
        self.nobutton.grid(row=3, column=1,
                           padx=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.flagbutton.grid(row=3, column=3,
                             padx=5, sticky=tk.N+tk.S+tk.W+tk.E)
        self.pauseButton.grid(row=3, column=4,
                              sticky=tk.N+tk.S+tk.W+tk.E)

        # UPDATES GUI
        self.updateGUI()

    def checkSave(self):
        # CHECKS IF A SAVE FILE IS SELECTED
        if self.saveFile != 'Select a save':
            # READS IN SAVE FILE
            self.save.readData(self.saveFile)
            temp = self.save.resumeLastQuestion()
            self.testName = self.saveFile
            self.mapnum = temp[0]
            self.maptype = self.maps[self.mapnum]
            self.question = self.questions[self.maptype][temp[1]][0]
            self.info = self.questions[self.maptype][temp[1]][2]
            self.info = self.wrapinfo(self.info)
            self.isNew = True
            self.isChange = True
            # UPDATES TO NEXT QUESTION
            if temp[2] == 'y' and isinstance(self.questions[self.maptype][temp[1]][1][0], int):
                self.output = self.questions[self.maptype][temp[1]][1][1]
            elif temp[2] == 'n' and isinstance(self.questions[self.maptype][temp[1]][1][1], int):
                self.output = self.questions[self.maptype][temp[1]][1][0]
            else:
                self.output = temp[2]
            if isinstance(self.output, int):
                self.question = self.questions[self.maptype][self.output][0]
                self.info = self.questions[self.maptype][self.output][2]
                self.info = self.wrapinfo(self.info)
            self.fromSave = True if isinstance(self.output, int) else False
            self.skippedQuestions = self.save.skipList()
            self.flags = self.save.flagList()
            self.critical = self.save.critList()
            print(self.critical)
            self.isChange = True

    def updateGUI(self):
        try:
            # CHECKS IF A CHANGE IS NEEDED AND THEN EDITS GUI
            if self.isChange:
                if self.skippedQuest:
                    self.questionText.config(text=self.question)
                    self.mapheader.config(text='Skipped: ' + self.maptype)
                    self.tip.text = self.info
                else:
                    self.questionText.config(text=self.question)
                    self.mapheader.config(text=self.maptype)
                    self.tip.text = self.info
                    self.save.mergeFlgCrit(self.flags, self.critical)
                # IF HITS CRITICAL / OK GOES TO NEXT MAP AND SKIPS IF NEEDED
                if (not isinstance(self.output, int) or self.isSkip) and not self.fromSave:
                    if self.mapnum == 14:
                        if len(self.skippedQuestions) == self.skipCount:
                            self.endBox()
                        else:
                            self.skippedQuest = True
                            self.doSkipped()
                    else:
                        if self.skippedQuest:
                            try:
                                self.addCritical()
                                self.skipCount += 1
                                self.mapnum = self.skippedQuestions[self.skipCount][0]
                                self.output = self.skippedQuestions[self.skipCount][1]
                                self.maptype = self.maps[self.mapnum]
                                self.question = self.questions[self.maptype][0][0]
                                self.info = self.questions[self.maptype][0][2]
                                self.info = self.wrapinfo(self.info)
                            except IndexError:
                                self.endBox()
                        else:
                            self.addCritical()
                            self.mapnum += 1
                            self.maptype = self.maps[self.mapnum]
                            self.output = 0
                            self.question = self.questions[self.maptype][0][0]
                            self.info = self.questions[self.maptype][0][2]
                            self.info = self.wrapinfo(self.info)
                            self.isSkip = False
                            if not self.isNew and len(self.skippedQuestions) > 0 and self.mapnum == self.skippedQuestions[-1][0]:
                                self.mapnum += 1
                                self.maptype = self.maps[self.mapnum]
                                self.question = self.questions[self.maptype][0][0]
                                self.info = self.questions[self.maptype][0][2]
                                self.info = self.wrapinfo(self.info)
                else:
                    self.critTrack = self.question
        except tk.TclError:
            self.file = open(self.testName, 'w')
            self.file.write(self.endString)

        self.root.after(17, self.updateGUI)

    def flagWindow(self):
        self.window = tk.Toplevel(self.root, bg='#f5f6f7')
        self.entry = tk.StringVar()
        self.window.title('Flag')
        ttk.Label(self.window, text='Why did you flag this?',
                  font=('Times New Roman', 14)).pack()
        ttk.Entry(self.window, textvariable=self.entry).pack(side=TOP)
        ttk.Button(self.window, text='Skip',
                   command=self.skip).pack(side=RIGHT)
        ttk.Button(self.window, text='Ok',
                   command=self.closeFlagWindow).pack(side=LEFT)

    def closeFlagWindow(self):
        self.flags.append([self.question, self.entry.get()])
        self.save.addFlag([self.question, self.entry.get()])
        self.window.destroy()

    def critWindow(self):
        self.window = tk.Toplevel(self.root, bg='#f5f6f7')
        self.entry = tk.StringVar()
        self.window.title('Critical')
        ttk.Label(self.window,
                  text=('Why was this critical? Question: ' + self.critTrack),
                  font=('Times New Roman', 14)).pack()
        ttk.Entry(self.window, textvariable=self.entry).pack()
        ttk.Button(self.window, text='Ok', command=self.closeCritWindow).pack()
        self.root.wait_window(self.window)

    def skip(self):
        self.flags.append([self.question, self.entry.get()])
        self.save.addSkip(self.output, self.mapnum, self.question, self.entry.get())
        self.skippedQuestions.append([self.mapnum, self.output])
        self.isChange = True
        self.isSkip = True
        self.window.destroy()

    def doSkipped(self):
        self.flagbutton.destroy()
        self.mapnum = self.skippedQuestions[self.skipCount][0]
        self.output = self.skippedQuestions[self.skipCount][1]
        self.maptype = self.maps[self.mapnum]
        self.question = self.questions[self.maptype][self.output][0]
        self.info = self.questions[self.maptype][self.output][2]
        self.info = self.wrapinfo(self.info)
        self.questionText.config(text=self.question)
        self.mapheader.config(text='Skipped: ' + self.maptype)
        self.tip.text = self.info

    def closeCritWindow(self):
        self.save.addCrit([self.critTrack, self.entry.get()])
        self.critical.append([self.critTrack, self.entry.get()])
        self.window.destroy()

    def addCritical(self):
        if self.output == 'Critical':
            self.critWindow()
    
    def yesButton(self):
        self.answer = 'y'
        self.isChange = True
        self.fromSave = False
        self.save.addQuestion(self.mapnum, self.maptype, self.output, self.question, self.answer)

        if isinstance(self.output, int):
            self.output = self.questions[self.maptype][self.output][1][1]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]
            self.info = self.questions[self.maptype][self.output][2]
            self.info = self.wrapinfo(self.info)

    def noButton(self):
        self.answer = 'n'
        self.isChange = True
        self.fromSave = False
        self.save.addQuestion(self.mapnum, self.maptype, self.output, self.question, self.answer)
        if isinstance(self.output, int):
            self.output = self.questions[self.maptype][self.output][1][0]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]
            self.info = self.questions[self.maptype][self.output][2]
            self.info = self.wrapinfo(self.info)

    def parseInfo(self):
        self.endString = 'Flagged Questions:\n'
        for i in self.flags:
            self.endString = self.endString + i[0] + ' : ' + i[1] + '\n'
        self.endString = self.endString + '\nCritical Questions:\n'
        for i in self.critical:
            self.endString = self.endString + i[0] + ' : ' + i[1] + '\n'
        self.testNameFile = "Reports/" + self.testName.replace(' ', '_')  + '/' + self.testName.replace(' ', '_') + '.txt'

    def endBox(self):
        self.root.destroy()
        self.end = ThemedTk(theme='arc')
        self.end.title('End')
        self.save.createSaveFile(self.testName, not self.isNew)
        self.parseInfo()
        print(self.endString)
        self.save.genPDF(self.testName, self.endString)
        ttk.Label(self.end, text=self.endString,
                  font=('Times New Roman', 16)).pack()
        
        self.file = open(self.testNameFile, 'x')
        self.file.write(self.endString)
        self.end.mainloop()

    def pause(self):
        self.save.createSaveFile(self.testName, not self.isNew)
        check = tk.Toplevel(self.root, bg='#f5f6f7')
        ttk.Label(check, text='Are you sure you want to exit?',
                  font=('Times New Roman', 16)).pack(side=TOP)
        ttk.Button(check, text='Yes', command=self.root.destroy).pack(side=LEFT)
        ttk.Button(check, text='No', command=check.destroy).pack(side=RIGHT)

    def wrapinfo(self, txt):
        if txt.find('\n') > -1:
            return txt
        temp = txt.split(' ')
        cnt = 0
        length = len(temp)
        output = ''
        if length < 15:
            return txt
        while length >= 15:
            cnt += 1
            output += ' '.join(temp[15 * (cnt - 1):15 * cnt]) + '\n'
            length -= 15
        if len(temp) % 15 != 0:
            output += ' '.join(temp[cnt * 15:])
        return output

import json
import os
import sys
import tkinter as tk
from tkinter import BOTTOM, ttk
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
    mapNum = 0
    skippedQuestions = []
    skippedQuest = False
    isSkip = False
    skipCount = 0
    endString = ''
    testName = ''
    assessmentName = ''
    saveFile = ''
    fromSave = False
    isNew = False
    assessmentNumber = 0
    waitForRestartAnswer = False
    waitForCritAnswer = False
    resumedAndNeedsRestart = False
    alreadyLoadedSave = False

    def __init__(self):
        # READS IN MAPS_LIST.TXT TO GET ALL THE MAPS
        with open('src/maps_list.txt', encoding='utf8') as myFile:
            self.maps = myFile.readline().split(',')
        
        # READS IN QUESTIONS_DICT.TXT TO GET ALL QUESTIONS
        with open('src/questions_dict.txt', encoding='utf8') as myFile:
            self.questions = myFile.read()
        # LOADS QUESTIONS INTO A DICTIONARY
        self.questions = json.loads(self.questions)

        # SETS INITAL VALUES FOR VARIABLES USING DATA READ IN FROM LIST
        self.maptype = self.maps[self.mapNum]
        self.question = self.questions[self.maptype][0][0]
        self.info = self.questions[self.maptype][0][2]
        self.info = self.wrapinfo(self.info)

        # CREATES LIST OF POSSIBILE FILES TO RESUME
        self.savedFiles = os.listdir('Reports/')

        # DEFINE A TEMP VAR TO ITERATE AND DELETE FILES FROM SAVED FILES LIST
        temp = list(self.savedFiles)
        # CLEANS LIST OF POSSIBILE FILES TO ONLY FILES THAT WE CAN RESUME FROM
        for i in range(len(self.savedFiles)):
            if os.path.isfile(f'Reports/{temp[i]}'):
                self.savedFiles.remove(temp[i])
        
        # DEFINE A TEMP VAR TO HOLD THE VALID SAVE FILES
        temp = []
        # DELETES ALL FOLDERS THAT DO NOT CONTAIN .CPI FILES
        for i in range(len(self.savedFiles)):
            for file in os.listdir(f'Reports/{self.savedFiles[i]}'):
                if file.endswith('.cpi'):
                    temp.append(self.savedFiles[i])
        self.savedFiles = temp

        # CREATES root AND WELCOME WIDGETS
        self.root = ThemedTk(theme='arc')
        self.buttons = tk.Frame(self.root)
        self.name = tk.StringVar()
        self.partName = tk.StringVar()
        
        self.welcome = ttk.Label(self.root, text='Trigon Cyber CPI Tool',
                                 font=('Times New Roman', 30, 'bold'))
        
        self.startbutton = ttk.Button(self.buttons,
                                      text='Start', command=self.startQuestions)

        self.enterName = ttk.Label(self.root,
                                   text='Enter the name of the utility you are testing.',
                                   font=('Times New Roman', 18))
        self.nameBox = ttk.Entry(self.root, textvariable=self.name)

        self.partNameLabel = ttk.Label(self.root,
                                       text='Enter the name of the part you are testing.',
                                       font=('Times New Roman', 18))
        self.partNameBox = ttk.Entry(self.root, textvariable=self.partName)

        self.bigPhoto = ImageTk.PhotoImage(Image.open('src/bigtrigon.jpeg'))
        self.biglogo = ttk.Label(self.root, image=self.bigPhoto)

        self.instructionButton = ttk.Button(self.buttons,
                                            text='Help',
                                            command=self.displayHelp)

        self.DropDown = tk.StringVar(self.buttons)
        self.DropDown.set('Select a save')
        self.savedFiles.insert(0, 'Select a save')
        self.savedFiles.append('Select a save')

        self.savedList = ttk.OptionMenu(self.buttons, self.DropDown, *self.savedFiles)
        self.startPage()

    def startPage(self):

        # DECORATES root WITH WELCOME WIDGETS
        self.root['background'] = '#f5f6f7'
        self.logo = tk.PhotoImage(file='src/trigon.png')
        self.root.iconphoto(True, self.logo)
        self.root.title('CPI Tool')
        self.root.geometry('1000x550')

        self.welcome.grid(row=0, column=0)
        self.enterName.grid(row=1, column=0)
        self.nameBox.grid(row=2, column=0)
        self.partNameLabel.grid(row=3, column=0)
        self.partNameBox.grid(row=4, column=0)
        self.startbutton.grid(row=0, column=0)
        self.biglogo.grid(row=6, column=0)
        self.instructionButton.grid(row=0, column=1)
        self.savedList.grid(row=0,  column=2)
        self.buttons.grid(row=5, column=0, columnspan=5)
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
                                      font=('Times New Roman', 16),
                                      text='The Critical Program Information (CPI) Tool is used to help fill out the CPI form.\n\nStart:\nThe CPI Tool asks for a name for the utility that you are testing. It uses this name to create the save file and data for your tool. You may also look at the drop-down menu to select\nany previously saved files.\n\nQuestions:\nWhen you select the start button the tool will prompt you with questions.\n\nButtons:\nThe yes and no buttons will let you answer yes and no to the questions.\nThe info button will display information that is useful pertaining to the current question that you are on.\nThe flag button presents you with two options and a dialogue box. The dialogue box allows you to add notes to any question you would like. If you want to just add notes and go back to\nthe question you can press the ‘Ok’ button in the box. The skip button will add the notes and push the current question and the rest of the current question map that you are on to the\nend of the program.\nThe pause button will save your progress for you to continue later.\n\nCritical:\nWhen you land on a ‘critical’ the program will prompt you to enter why you believe it was critical. This will be stored and entered in the final report.\n\nReport:\nAll reports generated will be saved in the ‘Reports’ folder in the working directory. Inside the folder there will be folders with the names of the utilities that you have tested. These folders\nwill hold a ‘.cpi’ file as a save file and when you finish with a report a pdf with the questions that you answered as well as the notes that you entered will be generated.') 
        self.back = ttk.Button(self.helpWindow,
                               text='Back',
                               command=self.helpWindow.destroy)

        self.instructionLabel.grid(row=0, column=0)
        self.instructions.grid(row=1, column=0, pady=10, padx=10)
        self.back.grid(row=2, column=0, pady=10)

    def startQuestions(self):
        # ADDS ONE TO ASSESSMENT NUMBER WHENEVER A NEW ASSESSMENT IS STARTED
        self.assessmentNumber += 1

        self.isChange = False

        # GETS INPUTS FROM START SCREEN
        self.saveFile = self.DropDown.get()
        self.testName = self.name.get()
        self.assessmentName = self.partName.get()
        self.partName.set('')

        if self.saveFile == 'Select a save' and self.testName == '':
            return

        # REMOVE START SCREEN
        self.welcome.destroy()
        self.startbutton.destroy()
        self.biglogo.destroy()
        self.enterName.destroy()
        self.nameBox.destroy()
        self.partNameLabel.destroy()
        self.partNameBox.destroy()
        self.instructionButton.destroy()
        self.buttons.destroy()

        # PREVENTS FROM CHECKING SAVE AFTER STARTING
        if not self.alreadyLoadedSave:
            self.checkSave()

        # CREATE INFO BUTTON
        self.infobtn = tk.PhotoImage(file='src/info.png')
        self.tipbutton = ttk.Button(self.root, image=self.infobtn)
        self.tip = Hovertip(self.tipbutton, self.info, hover_delay=500)

        # CREATE FLAG BUTTON
        self.flagbtn = tk.PhotoImage(file='src/flag.png')
        self.flagbutton = ttk.Button(self.root,
                                     image=self.flagbtn,
                                     command=self.flagWindow)

        # CREATE YES/NO BUTTONS
        self.yesbutton = ttk.Button(self.root,
                                    text='Yes', command=self.yesButton)
        self.nobutton = ttk.Button(self.root, text='No', command=self.noButton)

        # CREATE PAUSE BUTTON
        self.pausebutton = ttk.Button(self.root,
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
        self.pausebutton.grid(row=3, column=4,
                              sticky=tk.N+tk.S+tk.W+tk.E)

        # UPDATES GUI
        self.updateGUI()

    def checkSave(self):
        # CHECKS IF A SAVE FILE IS SELECTED
        if self.saveFile != 'Select a save':
            # READS IN SAVE FILE
            self.save.readData(self.saveFile)
            temp = self.save.resumeLastQuestion()
            
            self.alreadyLoadedSave = True
            self.testName = self.saveFile
            self.mapNum = temp[0]
            self.maptype = self.maps[self.mapNum]
            self.question = self.questions[self.maptype][temp[1]][0]
            self.info = self.questions[self.maptype][temp[1]][2]
            self.info = self.wrapinfo(self.info)
            self.isNew = True
            self.isChange = True
            # CHECKS IF FINSISHED WITH LAST ASSESSMENT AND STARTS NEW ONE IF SO
            if temp[0] == 14 and ((temp[1] == 0 and temp[2] == 'y') or (temp[1] == 1)):
                self.resumedAndNeedsRestart = True

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
            self.isChange = True

    def updateGUI(self):
        try:
            # CHECKS IF RESUMED FROM SAVE AND NEEDS TO RESTART
            if self.resumedAndNeedsRestart:
                self.resumedAndNeedsRestart = False
                self.waitForRestartAnswer = True
                self.restartScreen()
                
            # CHECKS IF A CHANGE IS NEEDED AND THEN EDITS GUI
            if self.isChange and not self.waitForRestartAnswer:
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
                    if self.mapNum == 14:
                        # IF FINISHED WITH ALL SKIPPED QUESTIONS DONE
                        if len(self.skippedQuestions) == self.skipCount:
                            self.restartScreen()
                            self.waitForRestartAnswer = True
                        else:
                            self.skippedQuest = True
                            self.doSkipped()
                    else:
                        if self.skippedQuest:
                            try:
                                self.addCritical()
                                self.skipCount += 1
                                self.mapNum = self.skippedQuestions[self.skipCount][0]
                                self.output = self.skippedQuestions[self.skipCount][1]
                                self.maptype = self.maps[self.mapNum]
                                self.question = self.questions[self.maptype][0][0]
                                self.info = self.questions[self.maptype][0][2]
                                self.info = self.wrapinfo(self.info)
                            except IndexError:
                                self.restartScreen()
                                self.waitForRestartAnswer = True

                        elif not self.waitForCritAnswer:
                            self.addCritical()
                            self.mapNum += 1
                            self.maptype = self.maps[self.mapNum]
                            self.output = 0
                            self.question = self.questions[self.maptype][0][0]
                            self.info = self.questions[self.maptype][0][2]
                            self.info = self.wrapinfo(self.info)
                            self.isSkip = False
                            self.waitForCritAnswer = False
                            if not self.isNew and len(self.skippedQuestions) > 0 and self.mapNum == self.skippedQuestions[-1][0]:
                                self.mapNum += 1
                                self.maptype = self.maps[self.mapNum]
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

        # CHECKS IF DOING SKIPPED QUESTIONS, IF SO NO SKIP BUTTON IS CREATED
        if self.skippedQuest:
            ttk.Button(self.window, text='Ok',
                   command=self.closeFlagWindow).pack(side=BOTTOM)
        else:
            ttk.Button(self.window, text='Ok',
                       command=self.closeFlagWindow).pack(side=LEFT)
            ttk.Button(self.window, text='Skip',
                       command=self.skip).pack(side=RIGHT)


    def closeFlagWindow(self):
        self.flags.append([self.assessmentNumber, self.question, self.entry.get()])
        self.window.destroy()

    def critWindow(self):
        self.criticalWindow = tk.Toplevel(self.root, bg='#f5f6f7')
        self.entry = tk.StringVar()
        self.criticalWindow.title('Critical')
        ttk.Label(self.criticalWindow,
                  text=('Why was this critical? Question: ' + self.critTrack),
                  font=('Times New Roman', 14)).pack()
        ttk.Entry(self.criticalWindow, textvariable=self.entry).pack()
        ttk.Button(self.criticalWindow, text='Ok', command=self.closeCritWindow).pack()
        self.waitForCritAnswer = True
        self.root.wait_window(self.criticalWindow)

    def skip(self):
        self.flags.append([self.assessmentNumber, self.question, self.entry.get()])
        self.save.addSkip(self.output, self.mapNum, self.question, self.entry.get())
        self.skippedQuestions.append([self.mapNum, self.output])
        self.isChange = True
        self.isSkip = True
        self.window.destroy()

    def doSkipped(self):
        self.mapNum = self.skippedQuestions[self.skipCount][0]
        self.output = self.skippedQuestions[self.skipCount][1]
        self.maptype = self.maps[self.mapNum]
        self.question = self.questions[self.maptype][self.output][0]
        self.info = self.questions[self.maptype][self.output][2]
        self.info = self.wrapinfo(self.info)
        self.questionText.config(text=self.question)
        self.mapheader.config(text='Skipped: ' + self.maptype)
        self.tip.text = self.info

    def closeCritWindow(self):
        self.save.addCrit([self.critTrack, self.entry.get()])
        self.critical.append([self.critTrack, self.entry.get()])
        self.criticalWindow.destroy()

    def addCritical(self):
        if self.output == 'Critical':
            self.critWindow()
    
    def yesButton(self):
        self.answer = 'y'
        self.isChange = True
        self.fromSave = False
        self.save.addQuestion(self.mapNum, self.maptype, self.output, self.question, self.answer, self.assessmentName, self.assessmentNumber)

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
        self.save.addQuestion(self.mapNum, self.maptype, self.output, self.question, self.answer, self.assessmentName, self.assessmentNumber)
        if isinstance(self.output, int):
            self.output = self.questions[self.maptype][self.output][1][0]
        if isinstance(self.output, int):
            self.question = self.questions[self.maptype][self.output][0]
            self.info = self.questions[self.maptype][self.output][2]
            self.info = self.wrapinfo(self.info)

    def endBox(self):
        for after_id in self.root.tk.eval('after info').split():
            self.root.after_cancel(after_id)

        self.root.destroy()
        self.end = ThemedTk(theme='arc')
        self.end.title('End')
        self.save.createSaveFile(self.testName, not self.isNew)
        self.save.genPDF(self.testName)
        ttk.Label(self.end, text=self.endString,
                  font=('Times New Roman', 16)).pack()

        self.testNameFile = "Reports/" + self.testName.replace(' ', '_')  + '/' + self.testName.replace(' ', '_') + '.txt'
        self.file = open(self.testNameFile, 'x')
        self.file.write(self.endString)
        self.end.mainloop()

    def pauseReport(self):
        for after_id in self.root.tk.eval('after info').split():
            self.root.after_cancel(after_id)

        self.root.destroy()
        self.save.createSaveFile(self.testName, not self.isNew)

    def restartScreen(self):
        # REMOVE ALL OLD WIDGETS
        self.yesbutton.grid_forget()
        self.nobutton.grid_forget()
        self.pausebutton.grid_forget()
        self.tipbutton.grid_forget()
        self.flagbutton.grid_forget()
        self.mapheader.grid_forget()
        self.questionText.grid_forget()

        # CREATE NEW WIDGETS
        self.restartLabel = ttk.Label(self.root, text='Did you need to do another CPI assessment?',
                  font=('Times New Roman', 20))
        self.restartYes = ttk.Button(self.root, text='Yes', command=self.restart)
        self.restartNo = ttk.Button(self.root, text='No', command=self.endBox)
        self.restartName = ttk.Entry(self.root, textvariable=self.partName)

        # ARRANGE RESTART SCREEN
        self.restartLabel.grid(row=0, column=0, columnspan=2)
        self.restartYes.grid(row=2, column=0)
        self.restartNo.grid(row=2, column=1)
        self.restartName.grid(row=1, column=0, columnspan=2)

    def restart(self):
        # RESET SKIPPED VARIABLES
        self.skippedQuest = False
        self.waitForRestartAnswer = False
        self.isSkip = False
        self.skippedQuestions = []
        self.skipCount = 0

        # GET NEW ASSESSMENT NAME AND RESET PARTNAME
        self.assessmentName = self.partName.get()
        self.partName.set('')

        # REMOVE ALL OLD WIDGETS
        self.restartLabel.destroy()
        self.restartYes.destroy()
        self.restartNo.destroy()
        self.restartName.destroy()

        # RESET ALL VARIABLES
        self.mapNum = 0
        self.maptype = self.maps[self.mapNum]
        self.question = self.questions[self.maptype][0][0]
        self.info = self.questions[self.maptype][0][2]
        self.info = self.wrapinfo(self.info)
        self.output = 0

        self.startQuestions()

    def pause(self):
        check = tk.Toplevel(self.root, bg='#f5f6f7')
        ttk.Label(check, text='Are you sure you want to exit?',
                  font=('Times New Roman', 16)).pack(side=TOP)
        ttk.Button(check, text='Yes', command=self.pauseReport).pack(side=LEFT)
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

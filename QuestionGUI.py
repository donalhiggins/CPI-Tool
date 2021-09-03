import tkinter as tk
from tkinter import ttk
from idlelib.tooltip import Hovertip
import threading
from ttkthemes import ThemedTk


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
        # CREATE root
        self.root = ThemedTk(theme='arc')
        self.root['background'] = '#f5f6f7'
        self.root.protocol('WM_DELETE_WINDOW', self.callback)
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
                                      text='', font=('Times New Roman', 14),
                                      wraplength=1200)

        # ARRANGE ELEMENTS
        self.mapheader.place(x=10, y=0)
        self.questionText.place(x=10, y=40)
        self.tipbutton.place(x=265, y=100)
        self.yesbutton.place(x=30, y=100)
        self.nobutton.place(x=115, y=100)
        self.flagbutton.place(x=210, y=100)

        # UPDATE GUI
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
        self.answer = True
        self.answered = True
        self.getAnswer()

    def noButton(self):
        self.answer = False
        self.answered = True
        self.getAnswer()

    def getAnswer(self):
        return self.answer

    def updateQuestion(self, quest, inf, mapt):
        self.isChange = True
        self.question = quest
        self.info = inf
        self.maptype = mapt

    def addCritical(self, questnum):
        self.critical.append(questnum)

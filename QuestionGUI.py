import tkinter as tk
from idlelib.tooltip import Hovertip
import threading


class QuestionGUI(threading.Thread):
    flags = []
    question = "temp_question"
    info = "temp_info"
    questionText = None
    isChange = False

    def __init__(self):
        t1 = threading.Thread(target=self.createGUI)
        t1.start()
        

    def createGUI(self):
        #CREATE root
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.logo = tk.PhotoImage(file='trigon.png')
        self.root.iconphoto(False, self.logo)
        self.root.title("!!!TEMP!!!")
        self.root.geometry("1280x720")

        #CREATE INFO BUTTON
        self.infobtn = tk.PhotoImage(file='info.png')
        self.tipbutton = tk.Button(self.root, image=self.infobtn)
        self.tip = Hovertip(self.tipbutton, self.info, hover_delay=500)

        #CREATE FLAG BUTTON
        self.flagbtn = tk.PhotoImage(file='flag.png')
        self.flagbutton = tk.Button(self.root, image=self.flagbtn, command=self.flag())

        #CREATE YES/NO BUTTONS
        self.yesbutton = tk.Button(self.root, text='Yes', font=('Times New Roman', 14), command=self.yesButton())
        self.nobutton = tk.Button(self.root, text='No', font=('Times New Roman', 14), command=self.noButton())

        #CREATE TITLE AND QUESTION
        self.header = tk.Label(self.root, text='!!!TEMP!!!', font=('Times New Roman', 24, 'bold'))
        self.questionText = tk.Label(self.root, text='aaaaa', font=('Times New Roman', 14))

        #ARRANGE ELEMENTS
        self.header.grid(row=0, column=0)
        self.questionText.grid(row=8, column=5)
        self.tipbutton.grid(row=8, column=10)
        self.yesbutton.grid(row=25, column=15)
        self.nobutton.grid(row=25, column=35)
        self.flagbutton.grid(row=30, column=40)

        #UPDATE GUI
        self.updateGUI()
        
        self.root.mainloop()

    def updateGUI(self):
        if self.isChange:
            self.questionText.config(text=self.question)
            self.tip.text = self.info

        self.root.after(1000, self.updateGUI)

    def callback(self):
        self.root.quit()

    def flag(self):
        return None

    def yesButton(self):
        return True

    def noButton(self):
        return False

    def updateQuestion(self, quest, inf):
        self.isChange = True
        self.question = quest
        self.info = inf
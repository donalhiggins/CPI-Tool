from QuestionGUI import QuestionGUI
from time import sleep
import json


def main():
    with open('maps_list.txt') as myFile:
        maps = myFile.readline().split(',')
    with open('questions_dict.txt') as myFile:
        questions = myFile.read()
    questions = json.loads(questions)

    window = QuestionGUI()

    tempquestion = ''
    for i in range(len(maps)):
        output = 0
        while(isinstance(output, int)):
            sleep(0.05)
            window.updateQuestion(questions[maps[i]][output][0], 'temp', maps[i])

            if(window.answer and window.answered):
                if(isinstance(questions[maps[i]][output][1][1], int)):
                    tempquestion = questions[maps[i]][questions[maps[i]][output][1][1]][0]

                output = questions[maps[i]][output][1][1]
                window.answered = False

            elif(not window.answer and window.answered):
                if(isinstance(questions[maps[i]][output][1][0], int)):
                    tempquestion = questions[maps[i]][questions[maps[i]][output][1][0]][0]

                output = questions[maps[i]][output][1][0]
                window.answered = False

        if(output == 'Critical'):
            window.addCritical(tempquestion)
            tempquestion = ''


if __name__ == "__main__":
    main()

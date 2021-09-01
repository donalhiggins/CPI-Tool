from QuestionGUI import QuestionGUI

def main():
    maps = ['1. Concepts Map', '2. Materials Map',
     '3. Design of Components/Subsystems/Systems Map', '4. Manufacturing Process Map',
      '5. Integration of Components/Subsytems/Systems Map', '6. Operational Interface Process Map',
       '7. Operational Concept Map']
    questions = {maps[0] : [['Is the concept in the public domain', [2, 1]], ['Are other countries/organziations pursuing?', [3, 4]],
     ['Does the concept provide us an Enhanced Capability?', ['Ok', 'Critical']], ['Would divulging it cause Public Outcry or Diplomatic Harm?', ['Ok', 'Critical']],
     ['Has a demostrator been developed by another country/organization?', [5, 6]], ['Have we developed a demonstrator?', ['Ok', 'Critical']],
     ['Is our conceptual approach markedly different?', ['Ok', 'Critical']]]}
    
    window = QuestionGUI()
    output = 0
    tempquestion = ''
    window.updateQuestion('test', 'test', maps[0])

    while(isinstance(output, int)):
        window.updateQuestion(questions[maps[0]][output][0], 'temp')

        if(window.answer and window.answered):
            if(not isinstance(questions[maps[0]][output][1][1], int)):
                tempquestion = questions[maps[0]][output][1][1]
            output = questions[maps[0]][output][1][1]
            window.answered = False
        elif(not window.answer and window.answered):
            if(not isinstance(questions[maps[0]][output][1][0], int)):
                tempquestion = questions[maps[0]][output][1][0]
            output = questions[maps[0]][output][1][0]
            window.answered = False

    window.addCritical(tempquestion)
    print(window.critical)
    


    

if __name__ == "__main__":
    main()
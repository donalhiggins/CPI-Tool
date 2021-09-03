from QuestionGUI import QuestionGUI
from time import sleep

def main():
    maps = ['1. Concepts Map', '2. Materials Map',
     '3.1 Design of Components/Subsystems/Systems Map', '3.2 Design of Components/Subsystems/Systems Map',
     '3.3 Design of Components/Subsystems/Systems Map', '3.4 Design of Components/Subsystems/Systems Map',
     '3.5 Design of Components/Subsystems/Systems Map', '4.1 Manufacturing Process Map',
     '4.2 Manufacturing Process Map', '5.1 Integration of Components/Subsytems/Systems Map',
     '5.2 Integration of Components/Subsytems/Systems Map', '6.1 Operational Interface Process Map',
     '6.2 Operational Interface Process Map', '7.1 Operational Concept Map',
     '7.2 Operational Concept Map']
     
    questions = {maps[0] : [['Is the concept in the public domain?', [2, 1]], ['Are other countries/organziations pursuing?', [3, 4]],
     ['Does the concept provide us an Enhanced Capability?', ['Ok', 'Critical']], ['Would divulging it cause Public Outcry or Diplomatic Harm?', ['Ok', 'Critical']],
     ['Has a demostrator been developed by another country/organization?', [5, 6]], ['Have we developed a demonstrator?', ['Ok', 'Critical']],
     ['Is our conceptual approach markedly different?', ['Ok', 'Critical']]],
     maps[1] : [['Are innovative materials/computer languages employed?', ['Ok', 1]], ['Do these materials provide an enhanced capability?', ['Ok', 'Critical']]],
     maps[2] : [['Have the COTS/GOTS been uniquely modified?', ['Ok', 1]], ['Does the modification provide us an enhanced capability?', ['No', 'Critical']]],
     maps[3] : [['Does this design enable adversary to defeat, copy, counter or reverse engineer the technology or capability?', ['Ok', 1]],
     ['Does the item\'s function and/or capability depend on this design?', ['Ok', 'Critical']]],
     maps[4] : [['Does this design depend on specific intelligence products?', ['Ok', 'Critical']]],
     maps[5] : [['Was the system designed to specifically exploit a known adversary vulnerability?', ['Ok', 1]],
     ['Would divulging cause concern from allies or enable countermeasure development?', ['Ok', 'Critical']]],
     maps[6] : [['Would the information resulting from modeling/simulation or test/evaluation reveal enhanced system performance?', ['Ok', 1]],
     ['Would that information allow an adversary to defeat, copy, counter or reverse engineer the technology or capability?', ['Ok', 'Critical']]],
     maps[7] : [['Are manufacturing/fabrication/coding processes standard/well known?', [1, 'Ok']], ['Does the process provide an enhanced capability?', ['Ok', 'Critical']]],
     maps[8] : [['Do manufacturing/fabrication/coding proccesses require or reveal unique tooling or materials?', ['Ok', 1]],
     ['Do the tooling or materials provide an enhanced capability?', ['Ok', 'Critical']]],
     maps[9] : [['Are the COTS/GOTS integrated in a unique way?', ['Ok', 1]], ['Does integration provide an enhanced capability?', ['Ok', 'Critical']]],
     maps[10] : [['Does integration of non-COTS/GOTS components refelect widely known methods?', [1, 'Ok']], ['Does the deviation provide an enhanced capability?', ['Ok', 'Critical']]],
     maps[11] : [['Would obtaining the item enable another country/organization to degrade its operational effectiveness?', ['Ok', 'Critical']]],
     maps[12] : [['Would obtaining the item reveal information that would allow another country/organization to defeat, copy, counter the or reverse engineer the system, subsystem or component technology or capability?', ['Ok', 'Critical']]],
     maps[13] : [['Would disclosure of the operational concept (just the concept) enable an adversary to counter or defeat the system capability directly?', ['Ok', 'Critical']]],
     maps[14] : [['Is the operational customer/user in the public domain?', [1, 'Ok']],
     ['Does the relationship between the system and its intended user reveal a unique operational capability specific target or mission set? i.e. tie to counter, defeat, degrade, disrupt or shorten combat life?',
     ['Ok', 'Critical']]]}
    
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
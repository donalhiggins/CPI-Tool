import os
from QuestionGUI import QuestionGUI

def main():
    ls = os.listdir()
    if 'Reports' not in ls:
        os.mkdir('Reports')
    QuestionGUI()

if __name__ == "__main__":        
    main()

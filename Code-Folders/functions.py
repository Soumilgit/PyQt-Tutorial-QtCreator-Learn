from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
from urllib.request import urlopen
import json
import pandas as pd
import random


with urlopen( "https://opentdb.com/api.php?amount=5&category=22&difficulty=hard&type=multiple") as webpage:

    data = json.loads(webpage.read().decode())
    df = pd.DataFrame(data["results"])

def preload_data(idx):

    question = df["question"][idx]
    correct = df["correct_answer"][idx]
    wrong = df["incorrect_answers"][idx]


    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
        ]


    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])

    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]


    parameters["question"].append(question)
    parameters["correct"].append(correct)

    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])


    print(parameters["correct"][-1])


parameters = {
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "correct": [],
    "score": [],
    "index": []
    }


widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": []
}


grid = QGridLayout()

def clear_widgets():

    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def clear_parameters():

    for parm in parameters:
        if parameters[parm] != []:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()

    parameters["index"].append(random.randint(0,49))
    parameters["score"].append(0)

def start_game():

    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])

    frame2()

def create_buttons(answer, l_margin, r_margin):

    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(

        "*{margin-left: " + str(l_margin) +"px;"+
        "margin-right: " + str(r_margin) +"px;"+
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 10px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )
    button.clicked.connect(lambda x: is_correct(button))
    return button

def is_correct(btn):

    if btn.text() == parameters["correct"][-1]:



        temp_score = parameters["score"][-1]
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)


        parameters["index"].pop()
        parameters["index"].append(random.randint(0,49))

        preload_data(parameters["index"][-1])


        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])

        if parameters["score"][-1] == 100:

            clear_widgets()
            frame3()
    else:

        clear_widgets()
        frame4()


def frame1():
    clear_widgets()

    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 60px;")
    widgets["logo"].append(logo)


    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#BC006C';
            border-radius: 15px;
            font-size: 20px;
            color: 'white';
            padding: 25px 0;
            margin: 60px 80px;
        }
        *:hover{
            background: '#BC006C';
        }
        '''
    )

    button.clicked.connect(start_game)
    widgets["button"].append(button)


    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)



def frame2():

    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        '''
        font-size: 20px;
        color: 'white';
        padding: 10px 10px;
        margin: 18px 80px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 15px;
        '''
    )
    widgets["score"].append(score)


    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        '''
        font-family: 'shanti';
        font-size: 15px;
        color: 'white';
        padding: 15px;
        '''
    )
    widgets["question"].append(question)


    button1 = create_buttons(parameters["answer1"][-1], 35, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 35)
    button3 = create_buttons(parameters["answer3"][-1], 35, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 35)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)


    image = QPixmap("logo_bottom.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 15px; margin-bottom: 20px;")
    widgets["logo"].append(logo)


    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)
    grid.addWidget(widgets["logo"][-1], 4, 0, 1,2)



def frame3():

    message = QLabel("Congradulations! \n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 15px; color: 'white'; margin: 60px 0px;"
        )
    widgets["message"].append(message)


    score = QLabel("60")
    score.setStyleSheet("font-size: 60px; color: #8FC740; margin: 0 25px 0px 25px;")
    widgets["score"].append(score)


    message2 = QLabel("OK. Now go back to WORK.")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 20px; color: 'white'; margin-top:0px; margin-bottom:25px;"
        )
    widgets["message2"].append(message2)


    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#BC006C'; padding:15px 0px; border: 1px solid '#BC006C'; color: 'white'; font-family: 'Arial'; font-size: 15px; border-radius: 20px; margin: 10px 100px;} *:hover{background:'#ff1b9e';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)


    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:15px; margin-bottom: 10px;"
    )
    widgets["logo"].append(logo)


    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)


def frame4():

    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 15px; color: 'white'; margin: 25px 5px; padding:20px;"
        )
    widgets["message"].append(message)


    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 60px; color: white; margin: 0 25px 0px 25px;")
    widgets["score"].append(score)


    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 15px 0px;
            background: '#BC006C';
            color: 'white';
            font-family: 'Arial';
            font-size: 25px;
            border-radius: 20px;
            margin: 10px 30px;
        }
        *:hover{
            background: '#ff1b9e';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)


    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:25px;"
    )
    widgets["logo"].append(logo)


    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)

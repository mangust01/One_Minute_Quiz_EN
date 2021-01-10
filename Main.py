# encoding: utf-8
import sys

import time

import random

from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # isStarted = 1 if <RETURN>  or <ENTER> keys were pressed
        self.isStarted = False
        # For checking current answer. Was current it right or wrong
        self.rightAnswer = ''
        # For six random answers array
        self.six_answers = []
        # For six random answers shuffled array
        self.shuffled_answers = []
        # Your quiz score
        self.sumScore = 0
        # What event-key was pressed. The lastPressed allows us to exclude twice click same button
        self.lastPressed = None
        # Number of the pressed button
        self.lastChosenAnswer = None
        # State of the quiz timer
        self.isGameTimerStarted = False
        # Number of the game timer ticks
        self.count = 0
        # String for a text label
        self.remainingTimeText = ''
        # String for a text labeling at end of the quiz
        self.learning_list = ''
        # Need to add wrong answer in the learning_list string
        self.lastWord = ''

        # This is for the initial warning, questions and list of wrong answers
        self.text_label = QLabel()
        self.text_label.setFont(QFont('Courier New', 30, QFont.Bold))
        self.text_label.setStyleSheet('color: #b5e853; padding : 0px;')
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setText("Press <ENTER>/<RETURN> to start one minute quiz\n\n Use <1> - <6> keys to answer multiple-choice quiz")

        # To show current score status
        self.score_label = QLabel()
        self.score_label.setFont(QFont('Courier New', 14, QFont.Bold))
        self.score_label.setMaximumHeight(50)
        self.score_label.setStyleSheet('color: #ffc107; margin-right: 30px; margin-top: 0px; margin-bottom: 0px;')
        self.score_label.setAlignment(QtCore.Qt.AlignRight)
        self.score_label.setText("")

        # To show remaining time
        self.timer_label = QLabel()
        self.timer_label.setFont(QFont('Courier New', 14, QFont.Bold))
        self.timer_label.setMaximumHeight(50)
        self.timer_label.setStyleSheet('color: #ffc107; margin-right: 30px; margin-top: 0px; margin-bottom: 0px;')
        self.timer_label.setAlignment(QtCore.Qt.AlignRight)
        self.timer_label.setText("")

        # Button 1
        self.answer_button_1 = QPushButton("")
        self.answer_button_1.setFont(QFont('Courier New', 20))
        self.answer_button_1.setStyleSheet('border-radius: 10px; background-color : #ff7a18; color : white; padding : 20px; margin-right: 30px; margin-left: 30px; margin-top: 50px; margin-bottom: 2px;')
        self.answer_button_1.clicked.connect(lambda: self.update_question())

        # Button 2
        self.answer_button_2 = QPushButton("")
        self.answer_button_2.setFont(QFont('Courier New', 20))
        self.answer_button_2.setStyleSheet('border-radius: 10px; background-color : #ff7a18; color : white; padding : 20px; margin-right: 30px; margin-left: 30px; margin-top: 5px; margin-bottom: 2px;')
        self.answer_button_2.clicked.connect(lambda: self.update_question())

        # Button 3
        self.answer_button_3 = QPushButton("")
        self.answer_button_3.setFont(QFont('Courier New', 20))
        self.answer_button_3.setStyleSheet('border-radius: 10px; background-color : #ff7a18; color : white; padding : 20px; margin-right: 30px; margin-left: 30px; margin-top: 5px; margin-bottom: 2px;')
        self.answer_button_3.clicked.connect(lambda: self.update_question())

        # Button 4
        self.answer_button_4 = QPushButton("")
        self.answer_button_4.setFont(QFont('Courier New', 20))
        self.answer_button_4.setStyleSheet('border-radius: 10px; background-color : #ff7a18; color : white; padding : 20px; margin-right: 30px; margin-left: 30px; margin-top: 5px; margin-bottom: 2px;')
        self.answer_button_4.clicked.connect(lambda: self.update_question())

        # Button 5
        self.answer_button_5 = QPushButton("")
        self.answer_button_5.setFont(QFont('Courier New', 20))
        self.answer_button_5.setStyleSheet('border-radius: 10px; background-color : #ff7a18; color : white; padding : 20px; margin-right: 30px; margin-left: 30px; margin-top: 5px; margin-bottom: 2px;')
        self.answer_button_5.clicked.connect(lambda: self.update_question())

        # Button 6
        self.answer_button_6 = QPushButton("")
        self.answer_button_6.setFont(QFont('Courier New', 20))
        self.answer_button_6.setStyleSheet('border-radius: 10px; background-color : #ff7a18; color : white; padding : 20px; margin-right: 30px; margin-left: 30px; margin-top: 5px; margin-bottom: 30px;')
        self.answer_button_6.clicked.connect(lambda: self.update_question())

        # Window properties
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.setGeometry(600, 250, 600, 600)
        self.setWindowTitle("One minute quiz")
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Initial layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text_label)
        self.setLayout(self.layout)

        self.dark_palette = QPalette()
        self.dark_palette.setColor(QPalette.Window, QColor(46, 47, 48))
        self.setPalette(self.dark_palette)
        self.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        self.showMaximized()

        # Main quiz timer
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.showTime)

        # To exclude twice click same button
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clear_pressed)

    # Servicing the main quiz timer. This function runs every 100ms.
    def showTime(self):

        # checking if flag is true
        if self.isGameTimerStarted:
            # incrementing the counter
            self.count -= 1

            # timer is completed
            if self.count == 0:
                # making flag false
                self.isGameTimerStarted = False
                # setting text to the label
                self.timer_label.setText("Press <ESC> to quit")
                self.answer_button_1.setEnabled(False)
                self.answer_button_2.setEnabled(False)
                self.answer_button_3.setEnabled(False)
                self.answer_button_4.setEnabled(False)
                self.answer_button_5.setEnabled(False)
                self.answer_button_6.setEnabled(False)
                self.layout.removeWidget(self.answer_button_1)
                self.answer_button_1.hide()
                self.layout.removeWidget(self.answer_button_2)
                self.answer_button_2.hide()
                self.layout.removeWidget(self.answer_button_3)
                self.answer_button_3.hide()
                self.layout.removeWidget(self.answer_button_4)
                self.answer_button_4.hide()
                self.layout.removeWidget(self.answer_button_5)
                self.answer_button_5.hide()
                self.layout.removeWidget(self.answer_button_6)
                self.answer_button_6.hide()
                self.text_label.setFont(QFont('Courier New', 12))
                self.text_label.setText(str("TIME IS OVER!\n"))
                if self.learning_list:
                    #self.text_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
                    self.text_label.setWordWrap(True)
                    self.text_label.setText(str("TIME IS OVER!\nREMEMBER:\n\n" + self.learning_list))

        if self.isGameTimerStarted:
            # getting text from count
            self.remainingTimeText = str(self.count / 10) + " s"

            # showing text
            self.timer_label.setText(self.remainingTimeText)

    def clear_pressed(self):
        self.lastPressed = None

    # Overriding the method of the class QWidget to process keyboard events
    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.save_progress()
            close = QMessageBox.question(self,
                                         "QUIT?",
                                         "Are you sure want to STOP and EXIT?",
                                         QMessageBox.Yes | QMessageBox.No)

            if close == QMessageBox.Yes:
                sys.exit()
            else:
                pass

        if (((event.key() == Qt.Key_Return) or (event.key() == Qt.Key_Enter)) and (not(self.isStarted))):
            # Additional GUI elements after start
            self.layout.addWidget(self.score_label)
            self.layout.addWidget(self.timer_label)
            self.answer_button_1.setEnabled(False)
            self.answer_button_2.setEnabled(False)
            self.answer_button_3.setEnabled(False)
            self.answer_button_4.setEnabled(False)
            self.answer_button_5.setEnabled(False)
            self.answer_button_6.setEnabled(False)
            self.layout.addWidget(self.answer_button_1)
            self.layout.addWidget(self.answer_button_2)
            self.layout.addWidget(self.answer_button_3)
            self.layout.addWidget(self.answer_button_4)
            self.layout.addWidget(self.answer_button_5)
            self.layout.addWidget(self.answer_button_6)
            score_text = "Your score is: " + str(self.sumScore)
            self.game_timer.start(100)
            self.count = 60 * 10
            self.isGameTimerStarted = True
            self.timer_label.setText(str(self.game_timer.remainingTime()))
            self.isStarted = True
            time.sleep(0.1)
            self.update_question()
            self.lastPressed = event.key()

        if (event.key() == Qt.Key_1 and (self.isStarted) and (self.count != 0)):
            self.lastChosenAnswer = 1
            if not(self.timer.isActive()):
                self.six_answers = []
                self.update_question()
                self.answer_button_1.animateClick(50)
                self.lastPressed = event.key()
            if self.timer.isActive():
                if self.lastPressed == event.key():
                    #print('Double')
                    time.sleep(0.2)
                    self.timer.stop()
            else:
                self.timer.start(100)

        if (event.key() == Qt.Key_2 and (self.isStarted) and (self.count != 0)):
            self.lastChosenAnswer = 2
            if not (self.timer.isActive()):
                self.six_answers = []
                self.update_question()
                self.answer_button_2.animateClick(50)
                self.lastPressed = event.key()
            if self.timer.isActive():
                if self.lastPressed == event.key():
                    # print('Double')
                    time.sleep(0.2)
                    self.timer.stop()
            else:
                self.timer.start(100)

        if (event.key() == Qt.Key_3 and (self.isStarted) and (self.count != 0)):
            self.lastChosenAnswer = 3
            if not (self.timer.isActive()):
                self.six_answers = []
                self.update_question()
                self.answer_button_3.animateClick(50)
                self.lastPressed = event.key()
            if self.timer.isActive():
                if self.lastPressed == event.key():
                    # print('Double')
                    time.sleep(0.2)
                    self.timer.stop()
            else:
                self.timer.start(100)

        if (event.key() == Qt.Key_4 and (self.isStarted) and (self.count != 0)):
            self.lastChosenAnswer = 4
            if not (self.timer.isActive()):
                self.six_answers = []
                self.update_question()
                self.answer_button_4.animateClick(50)
                self.lastPressed = event.key()
            if self.timer.isActive():
                if self.lastPressed == event.key():
                    # print('Double')
                    time.sleep(0.2)
                    self.timer.stop()
            else:
                self.timer.start(100)

        if (event.key() == Qt.Key_5 and (self.isStarted) and (self.count != 0)):
            self.lastChosenAnswer = 5
            if not (self.timer.isActive()):
                self.six_answers = []
                self.update_question()
                self.answer_button_5.animateClick(50)
                self.lastPressed = event.key()
            if self.timer.isActive():
                if self.lastPressed == event.key():
                    # print('Double')
                    time.sleep(0.2)
                    self.timer.stop()
            else:
                self.timer.start(100)

        if (event.key() == Qt.Key_6 and (self.isStarted) and (self.count != 0)):
            if not (self.timer.isActive()):
                self.lastChosenAnswer = 6
                self.six_answers = []
                self.update_question()
                self.answer_button_6.animateClick(50)
                self.lastPressed = event.key()
            if self.timer.isActive():
                if self.lastPressed == event.key():
                    # print('Double')
                    time.sleep(0.2)
                    self.timer.stop()
            else:
                self.timer.start(100)

    #def closeEvent(self, event):

    def save_progress(self):
        # There is no action here in this release
        print("Your progress has been saved")

    # Main proccess funcrion. It is called everytime the button is pressed
    def update_question(self):
        if not (self.timer.isActive()):
            if ((self.rightAnswer != "") and (self.shuffled_answers[self.lastChosenAnswer-1] == self.rightAnswer)):
                self.sumScore += 1
                #print("YOUR SCORE IS: ", self.sumScore)
            else:
                if (self.rightAnswer != ""):
                    lineToLearn = str(self.lastWord) + "\n"
                    self.learning_list += lineToLearn
            #print("\n", self.rightAnswer)
            #print(self.shuffled_answers)
            #print(self.lastChosenAnswer)
            lines = 0;
            with open('Vocabulary.txt', 'r', encoding="utf-8") as f:
                list_of_all_lines = []
                for row in f:
                    list_of_all_lines.append(row[0:-1])
                    lines += 1
                current_word = list_of_all_lines[random.randint(0, lines-1)]
                self.lastWord = current_word
                self.rightAnswer = current_word.split(' - ')[1]
                self.six_answers.append(self.rightAnswer)
                for answer in range(1, 6):
                    self.six_answers.append(list_of_all_lines[random.randint(0, lines-1)].split(' - ')[1])
                #print(self.six_answers)
                random.shuffle(self.six_answers)
            self.shuffled_answers = self.six_answers
            #print(self.rightAnswer)
            #print(current_word.split(' - ')[0])
            #rint(shuffled_answers)

            # Updating answers
            self.text_label.setFont(QFont('Courier New', 35, QFont.Bold))
            self.text_label.setStyleSheet('background-color: #201c29; color: white; border: 2px solid #555555; margin-top: 50px; margin-right: 30px; margin-left: 30px;')
            self.text_label.setText(str(current_word.split(' - ')[0]))
            self.answer_button_1.setText(str(self.shuffled_answers[0]))
            self.answer_button_1.setIcon(QIcon("1.svg"))
            self.answer_button_1.setIconSize(QSize(50, 50))
            self.answer_button_2.setText(str(self.shuffled_answers[1]))
            self.answer_button_2.setIcon(QIcon("2.svg"))
            self.answer_button_2.setIconSize(QSize(50, 50))
            self.answer_button_3.setText(str(self.shuffled_answers[2]))
            self.answer_button_3.setIcon(QIcon("3.svg"))
            self.answer_button_3.setIconSize(QSize(50, 50))
            self.answer_button_4.setText(str(self.shuffled_answers[3]))
            self.answer_button_4.setIcon(QIcon("4.svg"))
            self.answer_button_4.setIconSize(QSize(50, 50))
            self.answer_button_5.setText(str(self.shuffled_answers[4]))
            self.answer_button_5.setIcon(QIcon("5.svg"))
            self.answer_button_5.setIconSize(QSize(50, 50))
            self.answer_button_6.setText(str(self.shuffled_answers[5]))
            self.answer_button_6.setIcon(QIcon("6.svg"))
            self.answer_button_6.setIconSize(QSize(50, 50))
            score_text = "Your score: " + str(self.sumScore)
            self.score_label.setText(score_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
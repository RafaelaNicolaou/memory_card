#create a memory card application
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *

class Question:
    def __init__(self, question, answer, options):
        self.question = question
        self.answer = answer
        self.options = options

    def checkAnswer(self, ans):
        return self.answer == ans

class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Label
        self.label = QLabel("Which nationality")
        font = self.label.font()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_label = QVBoxLayout()
        self.layout_label.addWidget(self.label)

        # GroupBoxes
        self.question_groupBox = QGroupBox("Answer options")
        self.radioLayout()

        self.answer_groupBox = QGroupBox("Test Results")
        self.resultLayout()
    
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.rb1)
        self.buttonGroup.addButton(self.rb2)
        self.buttonGroup.addButton(self.rb3)
        self.buttonGroup.addButton(self.rb4)
        # Button
        self.button = QPushButton("Answer")
        self.layout_button = QVBoxLayout()
        self.layout_button.addWidget(self.button)

        #Prepare window layout
        self.layout_card = QVBoxLayout()
        self.layout_card.addLayout(self.layout_label)
        self.layout_card.addWidget(self.question_groupBox)
        self.layout_card.addWidget(self.answer_groupBox)
        self.layout_card.addLayout(self.layout_button)

        self.setLayout(self.layout_card)

        self.total = 0
        self.correct = 0
        self.score = 0

    def startTest(self, list_q):
        self.question_list = list_q
        #self.next_question = -1

        self.nextQuestion()

    def radioLayout(self):
        #Prepare radio widgets
        self.rb1 = QRadioButton("Enets")
        self.rb2 = QRadioButton("Smurfs")
        self.rb3 = QRadioButton("Chulyms")
        self.rb4 = QRadioButton("Aleuts")

        self.radio_layout = QHBoxLayout()
        Layout_ans2 = QVBoxLayout()
        Layout_ans3 = QVBoxLayout()

        Layout_ans2.addWidget(self.rb1)
        Layout_ans2.addWidget(self.rb2)
        Layout_ans3.addWidget(self.rb3)
        Layout_ans3.addWidget(self.rb4)
        self.radio_layout.addLayout(Layout_ans2)
        self.radio_layout.addLayout(Layout_ans3)

        self.question_groupBox.setLayout(self.radio_layout)

    def resultLayout(self):
        self.correct_label = QLabel()
        self.true_false = QLabel()
        self.score_label = QLabel()

        Layout_ans4 = QHBoxLayout()
        Layout_ans5 = QHBoxLayout()
        Layout_ans6 = QVBoxLayout()
        
        Layout_ans5.addWidget(self.true_false)
        Layout_ans5.addWidget(self.score_label, Qt.AlignHCenter)
        
        Layout_ans4.addWidget(self.correct_label)
        #Layout_ans4.addWidget(Incorrect)
        
        Layout_ans6.addLayout(Layout_ans5)
        Layout_ans6.addLayout(Layout_ans4)

        self.answer_groupBox.setLayout(Layout_ans6)

    def showResult(self):
        
        #GroupBox
        self.answer_groupBox.show()
        self.question_groupBox.hide()
        
        #SetLabels
        self.correct_label.setText(self.q_object.answer)
        self.true_false.setText(self.result)
        self.score_label.setText(f", Correct answers: ({self.correct}/{self.total}) Score(out of 100): {self.score:.2f}%")
        
        #Button
        #To avoid double hit we need to disconnect it first
        try: self.button.clicked.disconnect() 
        except Exception: pass

        self.button.setText("Next question")
        self.button.clicked.connect(self.nextQuestion)

    def ask(self):
        print("Function:ask!")
        
        self.q_object = self.question_list[self.next_question]
        self.label.setText(self.q_object.question)

       # self.right_ans = self.answer_list[self.next_question][0]
        ans_list = self.q_object.options #[right_answer, wrong1, wrong2, wrong3]
        shuffle(ans_list)

        self.answer_groupBox.hide()
        self.question_groupBox.show()

        self.rb1.setText(ans_list[0])
        self.rb2.setText(ans_list[1])
        self.rb3.setText(ans_list[2])
        self.rb4.setText(ans_list[3])

        try: self.button.clicked.disconnect() 
        except Exception: pass
        self.button.setText("Answer")
        self.button.clicked.connect(self.checkAnswer)

        self.buttonGroup.setExclusive(False)
        self.rb1.setChecked(False)
        self.rb2.setChecked(False)
        self.rb3.setChecked(False)
        self.rb4.setChecked(False)
        self.buttonGroup.setExclusive(True)

    def checkAnswer(self):
        print("Function:checkAnswer!")
        if self.rb1.isChecked():
            print(self.rb1.text())
            radio = self.rb1

        elif self.rb2.isChecked():
            print(self.rb2.text())
            radio = self.rb2

        elif self.rb3.isChecked():
            print(self.rb3.text())
            radio = self.rb3

        elif self.rb4.isChecked():
            print(self.rb4.text())
            radio = self.rb4

        if self.q_object.checkAnswer(radio.text()):
            self.result = "True"
            self.correct += 1
        else:
            self.result = "False"

        #Copute Score
        self.computeRating()

        #Show Results
        self.showResult()
    
    def computeRating(self):
        self.score = (self.correct/self.total)*100

    def nextQuestion(self):
        self.next_question = randint(0, len(self.question_list) -1)
        self.total += 1

        # if self.next_question > len(self.question_list)-1:
        #     self.next_question = 0

        self.ask()



app = QApplication([])
window = Window()
window.show()
list_q = [
    Question("Which nationality does not exist?", "Smurfs",["Smurfs", "Enets", "Chulyms", "Aleuts"]),
    Question("The national language of Brazil?", "Portuguese",["Portuguese", "Spanish", "Italian", "Brazilian"]),
    Question("From what material are the clouds made?", "fog",["fog", "metal", "aluminioum", "glass"]),
    Question("when was covit started?", "2019",["2019", "1981", "2000", "2020"])
]
window.startTest(list_q)
app.exec()


        # self.question_list = [
        #     "Which nationality does not exist?", 
        #     "The national language of Brazil?", 
        #     "From what material are the clouds made?", 
        #     "when was covit started?", 
        #     "where was covit started?", 
        #     "How many questions did you answer so far?", 
        #     "Am I tired?", 
        #     "what color do I like?", 
        #     "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 
        #     "Love you!"
        #     ]
        # self.answer_list = [
        #     ["Smurfs", "Enets", "Chulyms", "Aleuts"], 
        #     ["Portuguese", "Spanish", "Italian", "Brazilian"],
        #     ["fog", "metal", "aluminioum", "glass"],
        #     ["2019", "1981", "2000", "2020"],
        #     ["China", "Frence", "Spain", "America"],
        #     ["5", "4", "6","7"],
        #     ["yes", "yes", "yes", "yes"],
        #     ["pink", "red", "yellow", "blue"],
        #     ["AAAAAAAA...", "??????", "yes", "no"],
        #     ["Me too", "i hate you", "i love your quiz", "i hate your quiz"]
        #     ]
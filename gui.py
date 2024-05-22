import sys
from PyQt5.QtWidgets import  QPushButton, QLabel, QLineEdit, QSlider, QSpinBox, QDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QApplication, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt
from time import localtime
from re import match

YEAR = int(localtime()[0])

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.oldest = None
        self.totalHeight = 0
        self.numberMales = 0
        self.numberFemales = 0
        self.souls = []


        self.initUI()


    def initUI(self):

        buttonHeight = QPushButton(self, text= "Total height")
        buttonHeight.clicked.connect(self.commandHeight)

        buttonOldest = QPushButton(self, text= "Oldest")
        buttonOldest.clicked.connect(self.commandOldest)

        buttonGenders = QPushButton(self, text= "Gender ratio")
        buttonGenders.clicked.connect(self.commandGenders)

        buttonNames = QPushButton(self, text= "Names")
        buttonNames.clicked.connect(self.commandNames)
        
        buttonAdd = QPushButton(self, text= "ADD")
        buttonAdd.clicked.connect(self.__add)


        lines = QVBoxLayout()
        
        line1 = QHBoxLayout()
        line1.addWidget(buttonHeight)
        line1.addWidget(buttonOldest)
        line1.addWidget(buttonGenders)
        line1.addWidget(buttonNames)
        lines.addLayout(line1)

        line2 = QHBoxLayout()
        line2.addWidget(buttonAdd)
        lines.addLayout(line2)

        self.setLayout(lines)
        self.resize(400, 90)
        self.center()
        self.setWindowTitle('Commands')

        self.show()
    
    def __add(self):
        self.form = QDialog()
        self.form.setWindowTitle('From')
        vbox = QVBoxLayout()

        self.nameForm = QLineEdit()
        vbox.addWidget(QLabel("Name"))
        vbox.addWidget(self.nameForm)
        vbox.addStretch(1)


        self.genderForm = QSlider(Qt.Orientation.Horizontal)
        genderFormBox = QHBoxLayout()
        genderFormBox.addWidget(QLabel(" Female "))
        genderFormBox.addWidget(self.genderForm)
        genderFormBox.addWidget(QLabel("  Male  "))
        self.genderForm.setMaximum(100)
        self.genderForm.setMinimum(0)
        self.genderForm.setValue(50)
        vbox.addWidget(QLabel("Gender"))
        vbox.addLayout(genderFormBox)
        vbox.addStretch(1) 
        
        self.ageForm = QSpinBox()
        self.ageForm.setMinimum(1907)
        self.ageForm.setMaximum(YEAR)
        self.ageForm.setValue(YEAR)
        vbox.addWidget(QLabel("Birthyear"))
        vbox.addWidget(self.ageForm)
        vbox.addStretch(1)

        self.heightText = QLabel("Height: 0")
        self.heightForm = QSlider(Qt.Orientation.Horizontal)
        self.heightForm.setMinimum(0)
        self.heightForm.setMaximum(300)
        self.heightForm.valueChanged.connect(self.__height_changed)
        vbox.addWidget(self.heightText)
        vbox.addWidget(self.heightForm)
        vbox.addStretch(1)

        self.emailForm = QLineEdit()
        vbox.addWidget(QLabel("Email"))
        
        vbox.addWidget(self.emailForm)
        vbox.addStretch(1)

        buttonSubmit = QPushButton("Submit")
        buttonSubmit.clicked.connect(self.__submit)
        vbox.addWidget(buttonSubmit)


        self.form.setLayout(vbox)
        
        self.form.exec_()


    def commandHeight(self): 
        answer = QMessageBox(self)
        answer.setWindowTitle("Total height")
        answer.setText(f'Total height is {sum([i.height for i in self.souls])}')
        answer.show()
        return answer.exec_
    
    def commandOldest(self):
        if len(self.souls) == 0: QMessageBox().warning(self, "Error", "There aren't any persons"); return
        maxAge = -1
        for i in self.souls:
            if i.age > maxAge: oldest = i

        answer = QMessageBox(self)
        answer.setWindowTitle("Oldest")
        answer.setText(f"The oldest person is {oldest.name}\n{oldest.age} years old")
        answer.show()
        return answer.exec_
    
    
    def commandGenders(self):
        males = 0.0
        females = 0.0
        for i in self.souls:
            males += i.gender
            females += 1 - i.gender

        answer = QMessageBox(self)
        answer.setWindowTitle("Genders")
        answer.setText(f'There are:\n{males} males\n{females} females')
        answer.show()
        return answer.exec_

    
    def commandNames(self): 
        msg = ""
        for i in self.souls:
            msg += f'{i.name}\t{i.email}\n'
            # msg += i.name
            # msg += '\t'
            # msg += i.email
        answer = QMessageBox(self)
        answer.setWindowTitle("Names")
        answer.setText(msg[:-1])
        answer.show()
        return answer.exec_
            

    def __height_changed(self, _h): self.heightText.setText("Height: "+ str(_h))
    def __submit(self): 
        if match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.emailForm.text()): 
            self.souls.append(Soul(
                self.nameForm.text(), 
                self.genderForm.value() / 100, 
                YEAR - self.ageForm.value(), 
                self.heightForm.value(), 
                self.emailForm.text()
                ))
            self.form.close()
        else:
            QMessageBox().warning(self.form, "Error", "Invalid email")

    def center(self):
        # Получаем геометрию окна
        qr = self.frameGeometry()
        # Получаем разрешение экрана и определяем центр экрана
        cp = QDesktopWidget().availableGeometry().center()
        # Перемещаем центр окна в центр экрана
        qr.moveCenter(cp)
        # Устанавливаем верхний левый угол окна в соответствующую позицию
        self.move(qr.topLeft())

class Soul:
    def __init__(self, _name, _gender, _age, _height, _email) -> None:
        self.name = str(_name)
        self.gender = float(_gender)
        self.age = int(_age)
        self.height = int(_height)
        self.email = str(_email)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())

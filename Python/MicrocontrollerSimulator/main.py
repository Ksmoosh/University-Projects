import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QTextEdit, QMessageBox, \
    QRadioButton, QLabel, QLineEdit, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from numpy import binary_repr
import json


class Register:
    def __init__(self, name):
        self.name = name
        self.valueDecimal = 0
        self.valueNH = binary_repr(0, 8)
        self.valueNL = binary_repr(0, 8)


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Microcontroller Simulator'
        self.left = 200
        self.top = 300
        self.width = 800
        self.height = 400
        self.initUI()

        self.registers = [Register('AX'), Register('BX'), Register('CX'), Register('DX')]

        self.step = 0
        self.wyraz_num = 0
        self.commands = []
        for c in range(12):
            self.commands.append([])
            for i in range(3):
                self.commands[c].append('')

    def initUI(self):
        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 200)
        self.textbox.setDisabled(True)
        self.textbox.setStyleSheet('background-color: white; color: black')

        # Create textbox line numeration
        self.labelLinenumeration = QLabel(("<font color=\"black\">1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br></font>"), self)
        self.labelLinenumeration.move(2, 26)
        self.labelLinenumeration.resize(16, 200)

        self.mood_button_group = QButtonGroup()

        # Create command's radio buttons with a label

        self.labelcommands = QLabel("Rozkazy: ", self)
        self.buttonMOV = QRadioButton("MOV", self)                  # 1
        self.buttonADD = QRadioButton("ADD", self)                  # 2
        self.buttonSUB = QRadioButton("SUB", self)                  # 3

        self.mood_button_group.addButton(self.buttonMOV, 1)
        self.mood_button_group.addButton(self.buttonADD, 2)
        self.mood_button_group.addButton(self.buttonSUB, 3)

        self.labelcommands.move(305, 23)
        self.buttonMOV.move(315, 50)
        self.buttonADD.move(315, 70)
        self.buttonSUB.move(315, 90)

        # Create register's radio buttons with a label

        self.labelregisters = QLabel("Rejestry: ", self)
        self.buttonAX = QRadioButton("AX", self)
        self.buttonBX = QRadioButton("BX", self)
        self.buttonCX = QRadioButton("CX", self)
        self.buttonDX = QRadioButton("DX", self)

        self.mood_button_group.addButton(self.buttonAX, 4)
        self.mood_button_group.addButton(self.buttonBX, 5)
        self.mood_button_group.addButton(self.buttonCX, 6)
        self.mood_button_group.addButton(self.buttonDX, 7)

        self.labelregisters.move(395, 23)
        self.buttonAX.move(405, 50)
        self.buttonBX.move(405, 70)
        self.buttonCX.move(405, 90)
        self.buttonDX.move(405, 110)

        # Buttons and labels for adding number to the command in the textbox

        self.labelinsertnumber = QLabel("Podaj liczbę z \nprzedziału <0, 65535>: ", self)
        self.buttonInsertnumber = QRadioButton("Liczba", self)
        self.textInsertNumber = QLineEdit(self)

        self.mood_button_group.addButton(self.buttonInsertnumber, 8)

        self.textInsertNumber.resize(100, 20)
        self.labelinsertnumber.resize(150, 31)

        self.labelinsertnumber.move(495, 80)
        self.buttonInsertnumber.move(495, 50)
        self.textInsertNumber.move(650, 94)

        # Create button for inserting values from check buttons to the textbox
        self.buttonInsert = QPushButton('Wprowadź', self)
        self.buttonInsert.move(490, 180)
        self.buttonInsert.clicked.connect(self.insert_word)

        # Create button for deleting words from textbox
        self.buttonDelete = QPushButton('Usuń', self)
        self.buttonDelete.move(390, 180)
        self.buttonDelete.clicked.connect(self.delete_word)

        # Create label for errors
        self.labelErrors = QLabel("", self)
        self.labelErrors.setStyleSheet('color: red')
        self.labelErrors.resize(200, 30)
        self.labelErrors.move(390, 150)

        # Create button for saving to a file
        self.buttonSave = QPushButton('Zapisz', self)
        self.buttonSave.move(590, 360)
        self.buttonSave.clicked.connect(self.save_file)
        self.buttonSave.setIcon(QIcon("save.png"))

        # Create button for saving to a file
        self.buttonLoad = QPushButton('Wczytaj', self)
        self.buttonLoad.move(690, 360)
        self.buttonLoad.clicked.connect(self.load_file)
        self.buttonLoad.setIcon(QIcon("load.png"))

        # Create button for running the compiler
        self.buttonRun = QPushButton('Kompiluj', self)
        self.buttonRun.move(85, 215)
        self.buttonRun.clicked.connect(self.run)
        self.buttonRun.setIcon(QIcon("play.png"))

        # Create button for step running the compiler
        self.buttonStep = QPushButton('Praca krokowa', self)
        self.buttonStep.adjustSize()
        self.buttonStep.move(175, 215)
        self.buttonStep.clicked.connect(self.step_run)

        # Create labels for bit represenation of registers values

        self.labelAX = QLabel("AX", self)
        self.labelBX = QLabel("BX", self)
        self.labelCX = QLabel("CX", self)
        self.labelDX = QLabel("DX", self)

        self.labelNH = QLabel("NH", self)
        self.labelNL = QLabel("NL", self)

        self.labelAXNH = QLabel("00000000", self)
        self.labelBXNH = QLabel("00000000", self)
        self.labelCXNH = QLabel("00000000", self)
        self.labelDXNH = QLabel("00000000", self)

        self.labelAXNL = QLabel("00000000", self)
        self.labelBXNL = QLabel("00000000", self)
        self.labelCXNL = QLabel("00000000", self)
        self.labelDXNL = QLabel("00000000", self)

        self.labelAX.move(20, 255)
        self.labelBX.move(20, 285)
        self.labelCX.move(20, 315)
        self.labelDX.move(20, 345)

        self.labelNH.move(105, 235)
        self.labelNL.move(175, 235)

        self.labelAXNH.move(80, 255)
        self.labelBXNH.move(80, 285)
        self.labelCXNH.move(80, 315)
        self.labelDXNH.move(80, 345)

        self.labelAXNL.move(150, 255)
        self.labelBXNL.move(150, 285)
        self.labelCXNL.move(150, 315)
        self.labelDXNL.move(150, 345)

        self.show()

    def update_printed_registers(self):
        self.labelAXNH.setText(str(self.registers[0].valueNH))
        self.labelAXNL.setText(str(self.registers[0].valueNL))
        self.labelBXNH.setText(str(self.registers[1].valueNH))
        self.labelBXNL.setText(str(self.registers[1].valueNL))
        self.labelCXNH.setText(str(self.registers[2].valueNH))
        self.labelCXNL.setText(str(self.registers[2].valueNL))
        self.labelDXNH.setText(str(self.registers[3].valueNH))
        self.labelDXNL.setText(str(self.registers[3].valueNL))

        self.labelAXNH.repaint()
        self.labelBXNH.repaint()
        self.labelCXNH.repaint()
        self.labelDXNH.repaint()
        self.labelAXNL.repaint()
        self.labelBXNL.repaint()
        self.labelCXNL.repaint()
        self.labelDXNL.repaint()

    def update_registers_binary_value(self, r):
        binary = binary_repr(r.valueDecimal, 16)
        r.valueNH = binary[:8]
        r.valueNL = binary[8:16]

    def search_registers(self, r1, r2):
        if r2.isdigit():
            value = int(r2)
        else:
            for r in self.registers:
                if r.name == r2:
                    value = r.valueDecimal
                    break
        for r in self.registers:
            if r.name == r1:
                reg = r
        return reg, value

    def mov_function(self, r1, r2):
        r, value = self.search_registers(r1, r2)
        r.valueDecimal = value
        return r

    def add_function(self, r1, r2):
        r, value = self.search_registers(r1, r2)
        r.valueDecimal += value
        return r

    def sub_function(self, r1, r2):
        r, value = self.search_registers(r1, r2)
        r.valueDecimal -= value
        if r.valueDecimal < 0:
            r.valueDecimal = 0
        return r

    def check_run_valid(self):
        command_lines = 0
        for i in range(12):
            for j in range(3):
                if self.commands[i][j] == '':
                    return command_lines
                if j == 2:
                    command_lines += 1

    def clear_registers(self):
        for r in self.registers:
            r.valueDecimal = 0
            r.valueNH = binary_repr(0, 8)
            r.valueNL = binary_repr(0, 8)


    def print_colored_num_step(self, line):
        text = ""
        for i in range(12):
            if i == line:
                text += "<font color=\"red\">" + str(i + 1) + "<br></font>"
            else:
                text += "<font color=\"black\">" + str(i + 1) + "<br></font>"
        self.labelLinenumeration.setText(text)

    def print_black_num_step(self):
        text = ""
        for i in range(12):
            text += "<font color=\"black\">" + str(i + 1) + "<br></font>"
        self.labelLinenumeration.setText(text)

    def step_run(self):
        #print(self.step)
        register = 0
        if self.step == 0:
            self.clear_registers()
        valid_lines = self.check_run_valid()
        if valid_lines == 0:
            return

        if self.commands[self.step][0] == 'MOV':
            register = self.mov_function(self.commands[self.step][1], self.commands[self.step][2])
        elif self.commands[self.step][0] == 'ADD':
            register = self.add_function(self.commands[self.step][1], self.commands[self.step][2])
        elif self.commands[self.step][0] == 'SUB':
            register = self.sub_function(self.commands[self.step][1], self.commands[self.step][2])
        try:
            self.update_registers_binary_value(register)
        except Exception as e:
            print(e)

        self.print_colored_num_step(self.step)
        self.step = (self.step + 1) % valid_lines
        self.update_printed_registers()

    def run(self):
        self.step = 0
        register = 0
        self.clear_registers()
        self.print_black_num_step()
        valid_lines = self.check_run_valid()
        for i in range(valid_lines):
            if self.commands[i][0] == 'MOV':
                register = self.mov_function(self.commands[i][1], self.commands[i][2])
            elif self.commands[i][0] == 'ADD':
                register = self.add_function(self.commands[i][1], self.commands[i][2])
            elif self.commands[i][0] == 'SUB':
                register = self.sub_function(self.commands[i][1], self.commands[i][2])
            try:
                self.update_registers_binary_value(register)
            except Exception as e:
                print(e)
        self.update_printed_registers()

    def print_text(self):
        text = ''
        for i in range(12):
            for j in range(3):
                if self.commands[i][j] != '':
                    if j == 0:
                        text += self.commands[i][j] + ' '
                    if j == 1:
                        text += self.commands[i][j] + ', '
                    if j == 2:
                        try:
                            command = hex(int(self.commands[i][j]))
                            text += command + '\n'
                        except:
                            text += self.commands[i][j] + '\n'
        self.textbox.setText(text)
        self.textbox.repaint()
        self.show()

    def delete_command(self):
        for i in range(12):
            for j in range(3):
                if self.commands[i][j] == '':
                    if i == 0 and j == 0:
                        self.commands[i][j] = ''
                    elif i == 0:
                        self.commands[i][j - 1] = ''
                        self.wyraz_num = (self.wyraz_num - 1) % 3
                    elif j == 0:
                        self.commands[i - 1][2] = ''
                        self.wyraz_num = (self.wyraz_num - 1) % 3
                    else:
                        self.commands[i][j - 1] = ''
                        self.wyraz_num = (self.wyraz_num - 1) % 3
                    #print(self.commands)
                    return


    @pyqtSlot()
    def delete_word(self):
        self.delete_command()
        self.print_text()

    def right_command(self, command, iter):
        if iter == 0:
            if command in ('MOV', 'ADD', 'SUB'):
                return True
        elif iter == 1:
            if command in ('AX', 'BX', 'CX', 'DX'):
                command += ','
                return True
        elif iter == 2:
            if command in ('AX', 'BX', 'CX', 'DX'):
                return True
            if isinstance(command, int):
                return True

        return False

    def add_command(self, command):
        for i in range(12):
            for j in range(3):
                if self.commands[i][j] == '':
                    if self.right_command(command, j):
                        self.commands[i][j] = str(command)
                        #print(self.commands)
                        return True
                    return False

    @pyqtSlot()
    def insert_word(self):
        try:
            command_text = self.mood_button_group.checkedButton().text()
            if command_text == "Liczba":
                try:
                    number = int(self.textInsertNumber.text())
                    if 0 <= number <= 65535:
                        if self.add_command(number):
                            self.wyraz_num = (self.wyraz_num + 1) % 3
                            #print(self.wyraz_num)
                    else:
                        print("Podaj liczbę z zakresu!")
                except Exception as e:
                    print("Podaj liczbę!")

            elif command_text is not None:
                if self.add_command(command_text):
                    self.wyraz_num = (self.wyraz_num + 1) % 3
        except Exception as e:
            print(e)

        self.print_text()

    def save_file(self):
        with open('program.json', 'w') as outfile:
            json.dump(self.commands, outfile)

    def load_file(self):
        try:
            with open('program.json', 'r') as infile:
                self.commands = json.load(infile)
            self.print_text()
            self.labelErrors.setText("")
            self.labelErrors.repaint()
        except FileNotFoundError:
            self.labelErrors.setText("Nie ma takiego pliku!")
            self.labelErrors.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

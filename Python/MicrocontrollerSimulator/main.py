import appscript as appscript
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QTextEdit, QMessageBox, \
    QRadioButton, QLabel, QLineEdit, QButtonGroup, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from numpy import binary_repr
import json
from collections import deque
import sys
import os
import datetime
import platform

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
        self.stack = deque()
        self.stack_operator = [False, False]

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

        self.command_button_group = QButtonGroup()
        self.register_part_group = QButtonGroup()

        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 200)
        self.textbox.setDisabled(True)
        self.textbox.setStyleSheet('background-color: white; color: black')

        # Create textbox line numeration
        self.labelLinenumeration = QLabel(
            ("<font color=\"black\">1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br></font>"), self)
        self.labelLinenumeration.move(2, 26)
        self.labelLinenumeration.resize(16, 200)

        # Create command's radio buttons with a label

        self.labelcommands = QLabel("Rozkazy: ", self)
        self.buttonMOV = QRadioButton("MOV", self)  # 1
        self.buttonADD = QRadioButton("ADD", self)  # 2
        self.buttonSUB = QRadioButton("SUB", self)  # 3

        self.command_button_group.addButton(self.buttonMOV, 1)
        self.command_button_group.addButton(self.buttonADD, 2)
        self.command_button_group.addButton(self.buttonSUB, 3)

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

        self.labelregister_part = QLabel("Częśc rejestru: ", self)
        self.buttonNX = QRadioButton("NX", self)
        self.buttonNH = QRadioButton("NH", self)
        self.buttonNL = QRadioButton("NL", self)

        self.register_part_group.addButton(self.buttonNX, 1)
        self.register_part_group.addButton(self.buttonNH, 2)
        self.register_part_group.addButton(self.buttonNL, 3)

        self.command_button_group.addButton(self.buttonAX, 4)
        self.command_button_group.addButton(self.buttonBX, 5)
        self.command_button_group.addButton(self.buttonCX, 6)
        self.command_button_group.addButton(self.buttonDX, 7)

        self.labelregisters.move(445, 23)
        self.buttonAX.move(455, 50)
        self.buttonBX.move(455, 70)
        self.buttonCX.move(455, 90)
        self.buttonDX.move(455, 110)

        self.labelregister_part.move(445, 190)
        self.buttonNX.move(455, 210)
        self.buttonNH.move(455, 230)
        self.buttonNL.move(455, 250)

        # Buttons and labels for adding number to the command in the textbox

        self.labelinsertnumber = QLabel("Podaj liczbę z \nprzedziału <0, 65535>: ", self)
        self.buttonInsertnumber = QRadioButton("Liczba", self)
        self.textInsertNumber = QLineEdit(self)

        self.command_button_group.addButton(self.buttonInsertnumber, 8)

        self.textInsertNumber.resize(100, 20)
        self.labelinsertnumber.resize(150, 31)

        self.labelinsertnumber.move(545, 80)
        self.buttonInsertnumber.move(545, 50)
        self.textInsertNumber.move(550, 120)

        # Create button for inserting values from check buttons to the textbox
        self.buttonInsert = QPushButton('Wprowadź', self)
        self.buttonInsert.move(640, 180)
        self.buttonInsert.clicked.connect(self.insert_word)

        # Create button for deleting words from textbox
        self.buttonDelete = QPushButton('Usuń', self)
        self.buttonDelete.move(540, 180)
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

        ##############################################
        # Microcontroller interruption functions
        ##############################################

        # Create interruption radio buttons with a label and dropdown menu

        self.labelInterruption = QLabel("Przerwania: ", self)
        self.buttonDropdown = QRadioButton("INT", self)
        self.int_dropdown = QComboBox(self)

        self.command_button_group.addButton(self.buttonDropdown, 9)

        self.int_dropdown.addItem("INT0")
        self.int_dropdown.addItem("INT1")
        self.int_dropdown.addItem("INT2")
        self.int_dropdown.addItem("INT3")
        self.int_dropdown.addItem("INT6")
        self.int_dropdown.addItem("INT2A")
        self.int_dropdown.addItem("INT2C")
        self.int_dropdown.addItem("INT30")
        self.int_dropdown.addItem("INT49")
        self.int_dropdown.addItem("INTED")

        self.labelInterruption.move(305, 140)
        self.buttonDropdown.move(315, 160)
        self.int_dropdown.move(330, 160)

        # Create stack handling radio buttons

        self.labelStack = QLabel("Obsługa stosu: ", self)
        self.buttonPush = QRadioButton("PUSH", self)
        self.buttonPop = QRadioButton("POP", self)

        self.command_button_group.addButton(self.buttonPush, 10)
        self.command_button_group.addButton(self.buttonPop, 11)

        self.labelStack.move(305, 190)
        self.buttonPush.move(315, 210)
        self.buttonPop.move(315, 230)

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
        #print(r.valueDecimal)

    def search_registers(self, r1, r2):
        if r2.isdigit():
            value = int(r2)
        else:
            r2_copy = r2
            if r2[1] in ('H', 'L'):
                r2_copy = r2[0] + 'X'
            for r in self.registers:
                if r.name == r2_copy:
                    # if we want to use only 8 higher bits of the register
                    if r2[1] == 'H':
                        value = int(r.valueDecimal / 256)
                    # if we want to use only 8 lower bits of the register
                    elif r2[1] == 'L':
                        value = r.valueDecimal % 256
                    else:
                        value = r.valueDecimal
                    break
        for r in self.registers:
            r1_copy = r1
            if r1[1] in ('H', 'L'):
                r1_copy = r1[0] + 'X'
            if r.name == r1_copy:
                reg = r
        return reg, value

    def mov_function(self, r1, r2):
        r, value = self.search_registers(r1, r2)
        if r1[1] == 'H':
            r.valueDecimal = r.valueDecimal % 256 + value * 256
            return r
        elif r1[1] == 'L':
            r.valueDecimal = r.valueDecimal - r.valueDecimal % 256 + value
            return r
        r.valueDecimal = value
        return r

    def add_function(self, r1, r2):
        r, value = self.search_registers(r1, r2)
        if r1[1] == 'H':
            r.valueDecimal = r.valueDecimal + value * 256
            return r
        elif r1[1] == 'L':
            r.valueDecimal = r.valueDecimal + value % 256
            return r
        r.valueDecimal += value
        return r

    def sub_function(self, r1, r2):
        r, value = self.search_registers(r1, r2)
        if r1[1] == 'H':
            r.valueDecimal = r.valueDecimal - value * 256
        elif r1[1] == 'L':
            r.valueDecimal = r.valueDecimal - value % 256
        else:
            r.valueDecimal -= value
        if r.valueDecimal < 0:
            r.valueDecimal = 0
        return r

    def push_function(self, r1):
        for reg in self.registers:
            print(r1)
            if reg.name == r1:
                r = reg
                self.stack.append(reg.valueDecimal)
        return r

    def pop_function(self, r1):
        for reg in self.registers:
            if reg.name == r1:
                r = reg
                reg.valueDecimal = self.stack.pop()
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

    def int0_function(self):
        sys.exit()

    def int1_function(self):
        while 1:
            letter = input("Podaj znak do zamienienia na ASCII: ")[0]
            if 0 < ord(letter) <= 128:
                break
        self.registers[0].valueDecimal = self.registers[0].valueDecimal - \
                                         int(self.registers[0].valueNL, 2) + ord(letter)  # ord() changes to ASCII code
        self.update_registers_binary_value(self.registers[0])

    def int2_function(self):
        try:
            letter = int(self.registers[3].valueNL, 2)
        except Exception as e:
            print(e)
        if not 0 < letter <= 128:
            return
        self.registers[0].valueDecimal = self.registers[0].valueDecimal - \
                                         int(self.registers[0].valueNL, 2) + letter
        self.update_registers_binary_value(self.registers[0])
        print(chr(letter))

    def int3_function(self):
        os.system('open -a Terminal .')

    def int6_function(self):
        cmnd = input("Podaj polecenie do wpisania w konsoli: ")
        appscript.app('Terminal').do_script(cmnd)

    def int2A_function(self):
        now = datetime.datetime.now()
        # setting AL with day of the week
        self.registers[0].valueDecimal = self.registers[0].valueDecimal - \
                                         int(self.registers[0].valueNL, 2) + datetime.datetime.today().weekday()
        # setting BH with day in the month
        self.registers[1].valueDecimal = now.day * 256
        # setting BL with month in the year
        self.registers[1].valueDecimal = self.registers[1].valueDecimal + now.month
        # setting CX with current year a.d.
        self.registers[2].valueDecimal = now.year

        self.update_registers_binary_value(self.registers[0])
        self.update_registers_binary_value(self.registers[1])
        self.update_registers_binary_value(self.registers[2])

    def int2C_function(self):
        now = datetime.datetime.now()
        # setting AH with hour
        self.registers[0].valueDecimal = now.hour * 256
        # setting AL with minute
        self.registers[0].valueDecimal = self.registers[0].valueDecimal + now.minute
        # setting BH with second
        self.registers[1].valueDecimal = now.second * 256
        # setting CX with millisecond
        self.registers[1].valueDecimal = self.registers[1].valueDecimal + int(now.microsecond / 1000)

        self.update_registers_binary_value(self.registers[0])
        self.update_registers_binary_value(self.registers[1])

    def int30_function(self):
        try:
            maj, min = [platform.release().split('.')[0], platform.release().split('.')[1]]
            # setting AH with major system version (kernel version)
            self.registers[0].valueDecimal = int(maj) * 256
            # setting AL with minor system version
            self.registers[0].valueDecimal = self.registers[0].valueDecimal + int(min)
        except Exception as e:
            print(e)
            print("Wersja systemu nie nadaje się do przepisania do rejestrów!")
        self.update_registers_binary_value(self.registers[0])

    def int49_function(self):
        for i in range(4):
            self.registers[i].valueDecimal = 0
            self.update_registers_binary_value(self.registers[i])

    def intED_function(self):
        empty_arr = []
        for c in range(12):
            empty_arr.append([])
            for i in range(3):
                empty_arr[c].append('')
        with open('program.json', 'w') as outfile:
            json.dump(empty_arr, outfile)

    def commands_int_switch(self, cmnd):
        if cmnd == 'INT0':
            self.int0_function()
        elif cmnd == 'INT1':
            self.int1_function()
        elif cmnd == 'INT2':
            self.int2_function()
        elif cmnd == 'INT3':
            self.int3_function()
        elif cmnd == 'INT6':
            self.int6_function()
        elif cmnd == 'INT2A':
            self.int2A_function()
        elif cmnd == 'INT2C':
            self.int2C_function()
        elif cmnd == 'INT30':
            self.int30_function()
        elif cmnd == 'INT49':
            self.int49_function()
        elif cmnd == 'INTED':
            self.intED_function()

    def commands_switch(self, iterate):
        if self.commands[iterate][0] == 'MOV':
            register = self.mov_function(self.commands[iterate][1], self.commands[iterate][2])
        elif self.commands[iterate][0] == 'ADD':
            register = self.add_function(self.commands[iterate][1], self.commands[iterate][2])
        elif self.commands[iterate][0] == 'SUB':
            register = self.sub_function(self.commands[iterate][1], self.commands[iterate][2])
        elif self.commands[iterate][0] == 'PUSH':
            register = self.push_function(self.commands[iterate][1])
        elif self.commands[iterate][0] == 'POP':
            try:
                register = self.pop_function(self.commands[iterate][1])
            except IndexError as e:
                print(e)
                return False
        elif self.commands[iterate][0][:3] == 'INT':
            self.commands_int_switch(self.commands[iterate][0])
            return True
        try:
            self.update_registers_binary_value(register)
        except Exception as e:
            print(e)

        return True

    def step_run(self):
        if self.step == 0:
            self.clear_registers()
        valid_lines = self.check_run_valid()
        if valid_lines == 0:
            return
        if not self.commands_switch(self.step):
            return
        self.print_colored_num_step(self.step)
        self.step = (self.step + 1) % valid_lines
        self.update_printed_registers()

    def run(self):
        self.step = 0
        self.clear_registers()
        self.print_black_num_step()
        valid_lines = self.check_run_valid()
        for i in range(valid_lines):
            if not self.commands_switch(i):
                return
        self.update_printed_registers()

    def print_text(self):
        text = ''
        for i in range(12):
            for j in range(3):
                if self.commands[i][j] != '':
                    if j == 0:
                        text += self.commands[i][j] + ' '
                    elif j == 1:
                        if self.commands[i][j + 1] != 'nop':
                            text += self.commands[i][j] + ', '
                        elif self.commands[i][j] == 'nop':
                            text += ''
                        else:
                            text += self.commands[i][j] + ' '
                    elif j == 2:
                        try:
                            command = hex(int(self.commands[i][j]))
                            text += command + '\n'
                        except:
                            if self.commands[i][j] != 'nop':
                                text += self.commands[i][j] + '\n'
                            else:
                                text += '\n'
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
                        # 'nop' -> no operation
                        # enters 'if' if current command is interruption or stack operator
                        if self.commands[i - 1][2] == 'nop':
                            if self.commands[i - 1][1] == 'nop':
                                self.wyraz_num = (self.wyraz_num - 3) % 3
                                self.commands[i - 1][0] = ''
                            else:
                                self.wyraz_num = (self.wyraz_num - 2) % 3
                                self.stack_operator[0] = True
                            self.commands[i - 1][2] = ''
                            self.commands[i - 1][1] = ''
                        else:
                            self.commands[i - 1][2] = ''
                            self.wyraz_num = (self.wyraz_num - 1) % 3
                    else:
                        self.commands[i][j - 1] = ''
                        self.wyraz_num = (self.wyraz_num - 1) % 3
                        self.stack_operator = [False, False]
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
            elif command in ('PUSH', 'POP'):
                self.stack_operator[0] = True
                return True
            elif command == 'INT':
                # Handling interruption functions done in different method
                return False
        elif iter == 1:
            if self.stack_operator[0] and command in ('AX', 'BX', 'CX', 'DX'):
                self.stack_operator[1] = True
                return True
            elif not self.stack_operator[0] and \
                    command in ('AX', 'AH', 'AL', 'BX', 'BH', 'BL', 'CX', 'CH', 'CL', 'DX', 'DH', 'DL'):
                return True
            elif isinstance(command, int) and self.stack_operator[0]:
                print("Podaj rejestr!")
                return False
        elif iter == 2:
            if command in ('AX', 'AH', 'AL', 'BX', 'BH', 'BL', 'CX', 'CH', 'CL', 'DX', 'DH', 'DL'):
                return True
            if isinstance(command, int):
                return True

        return False

    def int_command(self, command, i, j):
        if j == 0 and command == 'INT':
            self.commands[i][j] = self.int_dropdown.currentText()
            return True
        return False

    def add_command(self, command):
        for i in range(12):
            for j in range(3):
                if self.commands[i][j] == '':
                    if self.right_command(command, j):
                        if self.stack_operator[1]:
                            self.commands[i][j + 1] = 'nop'
                            self.stack_operator = [False, False]
                        self.commands[i][j] = str(command)
                        #print(self.commands)
                        return True
                    elif self.int_command(command, i, j):
                        self.commands[i][j + 1] = 'nop'
                        self.commands[i][j + 2] = 'nop'
                        #print(self.commands)
                        return True
                    return False

    @pyqtSlot()
    def insert_word(self):
        try:
            command_text = self.command_button_group.checkedButton().text()
            if command_text == "Liczba":
                try:
                    number = int(self.textInsertNumber.text())
                    if 0 <= number <= 65535:
                        if self.add_command(number):
                            self.wyraz_num = (self.wyraz_num + 1) % 3
                    else:
                        print("Podaj liczbę z zakresu!")
                except Exception as e:
                    print("Podaj liczbę!")
            elif command_text in ('AX', 'BX', 'CX', 'DX'):
                try:
                    register_size = self.register_part_group.checkedButton().text()
                    command_text = command_text[0] + register_size[1]
                    if self.add_command(command_text):
                        self.wyraz_num = (self.wyraz_num + 1) % 3
                except Exception as e:
                    print(e)
            elif command_text in ('PUSH', 'POP', 'INT'):
                if self.add_command(command_text):
                    if command_text == 'INT':
                        self.wyraz_num = (self.wyraz_num + 1) % 3
                    self.wyraz_num = (self.wyraz_num + 2) % 3
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

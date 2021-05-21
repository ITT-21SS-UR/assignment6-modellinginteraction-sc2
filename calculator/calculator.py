import sys

from PyQt5 import uic, Qt, QtCore
from PyQt5.QtWidgets import QMainWindow

from calc_model import CalcModel
from config_parser import ConfigParser


# Adjusted code from Sarahs calculator assignment
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = uic.loadUi("calculator/calculator.ui", self)
        self.calc_model = CalcModel()
        self.setup_ui()

    def setup_buttons(self):
        self.window.btn0.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_0))
        self.window.btn1.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_1))
        self.window.btn2.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_2))
        self.window.btn3.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_3))
        self.window.btn4.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_4))
        self.window.btn5.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_5))
        self.window.btn6.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_6))
        self.window.btn7.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_7))
        self.window.btn8.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_8))
        self.window.btn9.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_9))

        self.window.btnPoint.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Period))
        self.window.btnPlus.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Plus))
        self.window.btnMinus.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Minus))
        self.window.btnTimes.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Asterisk))
        self.window.btnDivide.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Slash))

        self.window.btnResult.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Return))
        self.window.btnDelete.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Backspace))
        self.window.btnClear.clicked.connect(
            lambda: self.calc_model.button_pressed(QtCore.Qt.Key_Delete))

    def keyPressEvent(self, event):
        if self.calc_model.can_handle_key(event.key()):
            self.calc_model.key_pressed(event.key())
            event.accept()

        else:
            event.ignore()

    def setup_ui(self):
        # label to display the current operator (initialized empty).
        self.window.lblOperator.setText("")
        self.setup_buttons()

        # lcd panel with 15 digits to display the current number.
        self.calc_model.model_changed.connect(
            lambda: self.window.lcdNumber.display(self.calc_model.get_display_text()))
        self.calc_model.model_changed.connect(
            lambda: self.window.lblOperator.setText(self.calc_model.get_operator()))


if __name__ == '__main__':
    # config_parser = ConfigParser()  # TODO use that

    app = Qt.QApplication(sys.argv)
    window = Calculator()

    window.show()
    app.exec()

import sys

from PyQt5 import uic, Qt, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from calc_model import CalcModel

# Adjusted code from Sarahs calculator assignment
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__window = uic.loadUi("calculator/calculator.ui", self)
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())
        self.__calc_model = CalcModel()
        self.__setup_ui()

    def setup_buttons(self):
        self.__window.btn0.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_0))
        self.__window.btn1.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_1))
        self.__window.btn2.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_2))
        self.__window.btn3.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_3))
        self.__window.btn4.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_4))
        self.__window.btn5.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_5))
        self.__window.btn6.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_6))
        self.__window.btn7.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_7))
        self.__window.btn8.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_8))
        self.__window.btn9.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_9))

        self.__window.btnPoint.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Period))
        self.__window.btnPlus.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Plus))
        self.__window.btnMinus.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Minus))
        self.__window.btnTimes.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Asterisk))
        self.__window.btnDivide.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Slash))

        self.__window.btnResult.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Return))
        self.__window.btnDelete.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Backspace))
        self.__window.btnClear.clicked.connect(
            lambda: self.__calc_model.button_clicked(QtCore.Qt.Key_Delete))

    def __setup_ui(self):
        # label to display the current operator (initialized empty).
        self.__window.lblOperator.setText("")
        self.setup_buttons()

        # lcd panel with 15 digits to display the current number.
        self.__calc_model.model_changed.connect(
            lambda: self.__window.lcdNumber.display(self.__calc_model.get_display_text()))
        self.__calc_model.model_changed.connect(
            lambda: self.__window.lblOperator.setText(self.__calc_model.get_operator()))

    def keyPressEvent(self, event):
        if self.__calc_model.can_handle_key(event.key()):
            self.__calc_model.key_pressed(event.key())
            event.accept()

        else:
            event.ignore()


if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = Calculator()

    window.show()
    app.exec()

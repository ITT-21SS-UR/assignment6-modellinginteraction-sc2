import sys
from datetime import datetime
from enum import Enum

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject

from config_parser import ConfigKeys


class CalcModel(QObject):
    # input source (button, key) for proper logging
    class LoggingEntity(Enum):
        BUTTON_CLICKED = "button_clicked"
        KEY_PRESSED = "key_pressed"

    INPUT_TYPE = "input_type"
    INPUT_VALUE = "input_value"
    TIMESTAMP = "timestamp"

    model_changed = pyqtSignal()

    @staticmethod
    def __is_operator(key_code):
        return (key_code == QtCore.Qt.Key_Plus
                or key_code == QtCore.Qt.Key_Minus
                or key_code == QtCore.Qt.Key_Asterisk
                or key_code == QtCore.Qt.Key_Slash
                or key_code == QtCore.Qt.Key_Delete
                or key_code == QtCore.Qt.Key_Backspace
                or key_code == QtCore.Qt.Key_Return
                or key_code == QtCore.Qt.Key_Enter)

    @staticmethod
    def __is_digit(key_code):
        return (key_code == QtCore.Qt.Key_0
                or key_code == QtCore.Qt.Key_1
                or key_code == QtCore.Qt.Key_2
                or key_code == QtCore.Qt.Key_3
                or key_code == QtCore.Qt.Key_4
                or key_code == QtCore.Qt.Key_5
                or key_code == QtCore.Qt.Key_6
                or key_code == QtCore.Qt.Key_7
                or key_code == QtCore.Qt.Key_8
                or key_code == QtCore.Qt.Key_9)

    @staticmethod
    def __is_period(key_code):
        return (key_code == QtCore.Qt.Key_Period
                or key_code == QtCore.Qt.Key_Comma)

    @staticmethod
    def __key_code_to_text(key_code):
        if key_code == QtCore.Qt.Key_0:
            return "0"

        if key_code == QtCore.Qt.Key_1:
            return "1"

        if key_code == QtCore.Qt.Key_2:
            return "2"

        if key_code == QtCore.Qt.Key_3:
            return "3"

        if key_code == QtCore.Qt.Key_4:
            return "4"

        if key_code == QtCore.Qt.Key_5:
            return "5"

        if key_code == QtCore.Qt.Key_6:
            return "6"

        if key_code == QtCore.Qt.Key_7:
            return "7"

        if key_code == QtCore.Qt.Key_8:
            return "8"

        if key_code == QtCore.Qt.Key_9:
            return "9"

        if key_code == QtCore.Qt.Key_Plus:
            return "+"

        if key_code == QtCore.Qt.Key_Minus:
            return "-"

        if key_code == QtCore.Qt.Key_Asterisk:
            return "*"

        if key_code == QtCore.Qt.Key_Slash:
            return "/"

        if key_code == QtCore.Qt.Key_Backspace:
            return "delete"

        if key_code == QtCore.Qt.Key_Delete:
            return "clear"

        if (key_code == QtCore.Qt.Key_Return
                or key_code == QtCore.Qt.Key_Enter):
            return "="

        if CalcModel.__is_period(key_code):
            return "."

    def __init__(self, config=None):
        super().__init__()

        self.__config = config
        self.__text = ""  # current digits
        self.__formula = ""  # current formula with operators
        self.__finished = False  # indicates a finished calculation

        self.__stdout_csv_column_names()

    def __get_csv_columns(self):
        if self.__config:
            return [
                ConfigKeys.PARTICIPANT_ID.value,
                ConfigKeys.TASK.value,
                self.INPUT_TYPE,
                self.INPUT_VALUE,
                self.TIMESTAMP
            ]

        return [
            self.INPUT_TYPE,
            self.INPUT_VALUE,
            self.TIMESTAMP
        ]

    def __create_row_data(self, input_type, input_value):
        if self.__config:
            return {
                ConfigKeys.PARTICIPANT_ID.value: self.__config[ConfigKeys.PARTICIPANT_ID.value],
                ConfigKeys.TASK.value: self.__config[ConfigKeys.TASK.value],
                self.INPUT_TYPE: input_type,
                self.INPUT_VALUE: input_value,
                self.TIMESTAMP: datetime.now()
            }

        return {
            self.INPUT_TYPE: input_type,
            self.INPUT_VALUE: input_value,
            self.TIMESTAMP: datetime.now()
        }

    def __stdout_csv_column_names(self):
        for column_name in self.__get_csv_columns():
            if column_name == self.__get_csv_columns()[-1]:
                sys.stdout.write(str(column_name))
            else:
                sys.stdout.write(str(column_name) + ",")

        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def __write_to_stdout_in_csv_format(row_data):
        row_data_values = list(row_data.values())
        values_length = len(row_data_values)

        for i in range(values_length):
            value = str(row_data_values[i])

            if i == values_length - 1:
                sys.stdout.write(value)
            else:
                sys.stdout.write(value + ",")

        sys.stdout.write("\n")
        sys.stdout.flush()

    def log_input(type):
        def log_decorator(function):
            def log_function(self, to_be_logged):
                self.__write_to_stdout_in_csv_format(
                    self.__create_row_data(type.value, CalcModel.__key_code_to_text(to_be_logged)))

                function(self, to_be_logged)

            return log_function

        return log_decorator

    def __on_result_evaluated(self, result):
        self.__text = result
        self.__finished = True
        self.model_changed.emit()

    def __delete(self):
        if self.__text:
            self.__text = self.__text[:-1]
            self.model_changed.emit()

    def __clear(self):
        self.__finished = False
        self.__formula = ""
        self.__text = ""
        self.model_changed.emit()

    def __calculate(self):
        try:
            if self.__formula:
                self.__on_result_evaluated(round(eval(self.__formula), 14))
        except SyntaxError:
            self.__text = "ERR"

    def __handle_input(self, key_code):
        # if key is not allowed the input is ignored
        if not self.__is_key_allowed(key_code):
            return

        # the key code is converted to its text representation
        key_text = CalcModel.__key_code_to_text(key_code)

        if CalcModel.__is_operator(key_code):
            if key_code == QtCore.Qt.Key_Delete:
                self.__clear()

            elif key_code == QtCore.Qt.Key_Backspace:
                self.__delete()

            # before calculation the text is appended to the formula
            elif (key_code == QtCore.Qt.Key_Return
                  or key_code == QtCore.Qt.Key_Enter):
                self.__formula += self.__text
                self.__calculate()

            # this effectively changes the current operator
            elif (self.__formula
                  and not self.__text):
                self.__formula = self.__formula[:-1] + key_text

            elif self.__text:
                self.__formula += self.__text + key_text
                self.__text = ""

        else:
            self.__text += key_text

        self.model_changed.emit()

    def __is_key_allowed(self, key_code):
        if (CalcModel.__is_period(key_code)
                and ("." in self.__text)):
            return False

        return True

    @staticmethod
    def can_handle_key(key_code):
        if (CalcModel.__is_digit(key_code)
                or CalcModel.__is_operator(key_code)
                or CalcModel.__is_period(key_code)):
            return True

        return False

    @log_input(LoggingEntity.KEY_PRESSED)
    def key_pressed(self, key_code):
        if self.__finished:
            self.__clear()

        self.__handle_input(key_code)

    @log_input(LoggingEntity.BUTTON_CLICKED)
    def button_clicked(self, key_code):
        if self.__finished:
            self.__clear()

        self.__handle_input(key_code)

    def get_display_text(self):
        if not self.__text:
            return "0"

        return self.__text

    def get_operator(self):
        if not self.__formula:
            return ""

        if self.__finished:
            return "="

        return self.__formula[-1]

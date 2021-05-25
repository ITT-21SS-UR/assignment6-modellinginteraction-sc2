import os
import sys

"""
Reads a file and outputs two different predictions (standard, custom set)
for the task completion time of the calculator.

File restrictions:
    When a comment is written a # is not allowed within the comment.
    Allowed characters are k, p, b, h, m (case insensitive)
"""


# Author: Sarah
# Reviewer: Claudia


def read_file(filename):
    if len(sys.argv) < 2:
        sys.stderr.write("Please give a valid klm txt file as argument (-_-)\n")
        sys.exit(1)

    if not os.path.isfile(filename):
        sys.stderr.write("File does not exist (-_-)\n")
        sys.exit(1)

    file = open(filename, 'r')
    data = []

    # Strips at newline character
    for line in file.readlines():
        striped_line = line.strip()

        if striped_line:
            data.append(striped_line)

    return data


def clean_data(data):
    cleaned_data = []

    for i in range(0, len(data)):
        current_line = data[i]
        comment_char_pos = data[i].rfind("#")  # finds the index of the last #

        if comment_char_pos != -1:
            current_line = data[i][:comment_char_pos].strip()

        if current_line != "":
            cleaned_data.append(current_line.lower())

    return cleaned_data


def calc_klm_time_one_line(line_data):
    result_klm = 0.0
    result_experiment = 0.0
    current_number = ""

    for i in range(0, len(line_data)):
        current_line = line_data[i]
        if current_line.isdigit():
            current_number += str(current_line)

        else:
            if current_number == '':
                result_klm += get_klm_value(current_line)
                result_experiment += get_experiment_value(current_line)
            else:
                result_klm += int(current_number) * get_klm_value(current_line)
                result_experiment += int(current_number) * get_experiment_value(current_line)

            current_number = ""

    return result_klm, result_experiment


def get_klm_value(char):
    if char == 'k':
        return 0.28
    if char == 'p':
        return 1.1
    if char == 'b':
        return 0.1
    if char == 'h':
        return 0.4
    if char == 'm':
        return 1.2

    return -1


def get_experiment_value(char):
    if char == 'k':
        return 0.28
    if char == 'p':
        return 0.73
    if char == 'b':
        return 0.16
    if char == 'h':
        return 0.31
    if char == 'm':
        return 1.2  # standard value because not calculated during study

    return -1


def calc_total_klm_time(data):
    result_klm = 0.0
    result_experiment = 0.0

    for i in range(0, len(data)):
        result_klm += calc_klm_time_one_line(data[i])[0]
        result_experiment += calc_klm_time_one_line(data[i])[1]

    print("Time for standard klm: {}".format(result_klm))
    print("Time for experiment klm: {}".format(result_experiment))

    return result_klm, result_experiment


def calculate_klm_estimates():
    file_data = read_file(sys.argv[1])
    processed_data = clean_data(file_data)
    calc_total_klm_time(processed_data)


if __name__ == '__main__':
    calculate_klm_estimates()

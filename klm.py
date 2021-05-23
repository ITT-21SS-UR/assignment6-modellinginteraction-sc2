import sys

# Author: Sarah
# Reviewer: Claudia


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    count = 0
    data = []

    # Strips at newline character
    for line in lines:
        data.append(line.strip())
        count += 1

    return data


def delete_comments(data):
    cleaned_data = []

    for i in range(0, len(data)):
        comment_char_pos = data[i].rfind("#")
        current_line = data[i][:comment_char_pos].strip()

        if current_line != "":
            cleaned_data.append(current_line)

        i += 1

    return cleaned_data


def calc_klm_time_one_line(line_data):
    result_klm = 0.0
    result_experiment = 0.0
    current_number = ""

    for i in range(0, len(line_data)):
        if line_data[i].isdigit():
            current_number += str(line_data[i])

        if not line_data[i].isdigit():
            if current_number == '':
                result_klm += get_klm_value(line_data[i].lower())
                result_experiment += get_experiment_value(line_data[i].lower())
            else:
                result_klm += int(current_number) * get_klm_value(line_data[i].lower())
                result_experiment += int(current_number) * get_experiment_value(line_data[i].lower())
            current_number = ""

    return (result_klm, result_experiment)


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

    return


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

    return


def calc_total_klm_time(data):
    result_klm = 0.0
    result_experiment = 0.0

    for i in range(0, len(data)):
        result_klm += calc_klm_time_one_line(data[i].lower())[0]
        result_experiment += calc_klm_time_one_line(data[i].lower())[1]

    print("Time for standard klm: {}".format(result_klm))
    print("Time for experiment klm: {}".format(result_experiment))

    return (result_klm, result_experiment)


if __name__ == '__main__':
    file_data = read_file(sys.argv[1])
    new_data = delete_comments(file_data)

    calc_total_klm_time(new_data)

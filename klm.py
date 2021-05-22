import sys


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    count = 0
    data = []
    # Strips the newline character
    for line in lines:
        data.append(line.strip())
        count += 1

        # print("Line{}: {}".format(count, line.strip()))

    # print(data)
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
                result_klm += get_klm_value(line_data[i])
                result_experiment += get_experiment_value(line_data[i])
            else:
                result_klm += int(current_number) * get_klm_value(line_data[i])
                result_experiment += int(current_number) * get_experiment_value(line_data[i])
            current_number = ""

    return (result_klm, result_experiment)


# TODO check values
def get_klm_value(char):
    if char == 'k':
        return 0.28
    elif char == 'p':
        return 1.1
    elif char == 'b':
        return 0.1
    elif char == 'h':
        return 0.4
    elif char == 'm':
        return 1.2

    return


def get_experiment_value(char):
    if char == 'k':
        return 0.28
    elif char == 'p':
        return 0.73
    elif char == 'b':
        return 0.16
    elif char == 'h':
        return 0.31
    elif char == 'm':
        return 1.2  # standard value because not calculated during study

    return


def calc_total_klm_time(data):
    result_klm = 0.0
    result_experiment = 0.0

    for i in range(0, len(data)):
        result_klm += calc_klm_time_one_line(data[i])[0]
        result_experiment += calc_klm_time_one_line(data[i])[1]

    print("Time for stadard klm: {}".format(result_klm))
    print("Time for experiment klm: {}".format(result_experiment))

    return (result_klm, result_experiment)


if __name__ == '__main__':
    filename = sys.argv[1]
    data = read_file(filename)
    cleaned_data = delete_comments(data)

    calc_total_klm_time(cleaned_data)

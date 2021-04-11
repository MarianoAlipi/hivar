import sys


def get_file_content(filename):
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print('File does not exist')
        exit(1)
    except Exception:
        print('Unable to open file')
        exit(1)

    lines = file.read()
    file.close()
    return lines

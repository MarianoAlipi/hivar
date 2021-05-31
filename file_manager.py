import sys


def get_file_content(filename):
    # open file, handle errors
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print('File does not exist')
        exit(1)
    except Exception:
        print('Unable to open file')
        exit(1)

    # load file content and return
    lines = file.read()
    file.close()
    return lines

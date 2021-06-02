def get_file_content(filename):
    # open file, handle errors
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print('Error: file not found.\n')
        exit(1)
    except Exception as err:
        print('Error: unable to open file.\n')
        print(err)
        exit(1)

    # load file content and return
    lines = file.read()
    file.close()
    return lines

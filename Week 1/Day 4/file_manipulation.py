
def create_new_file(filename: str):
    """
    Creates a new file
    """
    with open(filename, 'x') as _:
        print(f'created file with {filename}')


def readlines_from_file(filename: str) -> None:
    """
    Reads contents from file if it exists
    Args:
        filename: full filename with extension
    """
    try:
        with open(filename, 'r') as file:
            print(file.readlines())
    except FileNotFoundError as e:
        print(f'requested file {filename} does not exist: {e}')


def append_to_file(filename: str, content: str) -> None:
    """
    append content string to a specific file
    Args:
        filename: name of the file with extension
        content: the content to write
    """
    try:
        with open(filename, 'a') as file:
            file.write(content)
    except FileNotFoundError as e:
        print(f'requested file {filename} does not exist: {e}')

def write(filename, content):
    """
    the actual writing fucntionality
    Args:
        filename: name of the file
        content: content to write
    """
    with open(filename, 'w') as file:
        file.write(content)


def write_to_file(filename: str, content: str) -> None:
    """
    writes content to a file, if the file does not exist then
    it creates a new file then writes.
    Args:
        filename: name of the file
        content: content to write
    """
    try:
        write(filename, content)
    except FileNotFoundError:
        print(f'This file {filename} does not exist')
        create_new_file(filename)
        write(filename, content)
    finally:
        print(f"written '{content}' to '{filename}'")

def write_lines_to_file(filename: str, content: list[str]):
    """
    Writes multiple lines to a file
    Args:
        filename: fullname of the file
        content: list of strings, each element denotes single line
    Raises:
        FileNotFoundError: if file (param 1) does not exist.
    """
    try:
        with open(filename, 'w') as file:
            for line in content:
                file.write(line + '\n')
    except FileNotFoundError as e:
        raise Exception(f'specified file: {filename} not found: {e}')



if __name__ == '__main__':
    # readlines_from_file('sample.txt')
    # readlines_from_file('test.txt')
    # append_to_file('test.txt', 'ghb')
    # readlines_from_file('test.txt')
    # content = {
    #     'line1',
    #     'line2',
    #     'line3',
    #     'line4'
    # }
    # write_lines_to_file(filename='new_test4.txt', content=content)
    # create_new_file('new_new_test.txt')
    write_to_file('new_test5.txt', 'Jello world')

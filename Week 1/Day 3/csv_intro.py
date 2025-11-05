import csv

def read_rows(filename: str):
    """
    Reads then prints all the rows from a csv file
    Args:
        filename: csv file to read
    """
    with open(filename, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row)


def append_rows(filename: str, content: list[dict]):
    """
    Append new rows to an existing csv file
    Args:
        filename: csv file to append to
        content: contains a list of dictionary, each dict in the list is a new row,
                 the dictionary contains column name as key and associated values as dict values
    """
    with open(filename, 'a', newline='') as csv_file:
        field_names = ['StudentID', 'Name', 'Age', 'Gender', 'Course', 'Score', 'Grade']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        for row in content:
            writer.writerow(row)

    

if __name__ == '__main__':
    filename: str = 'student_data.csv'
    read_rows(filename=filename)

    new_entries: list[dict[str, str]] = [
        {"StudentID": '10005', "Name": 'Holland', "Age": '27', "Gender":'M', "Course": 'Science', "Score": '99', "Grade": 'S'},
        {"StudentID": '10006', "Name": 'Cane', "Age": '33', "Gender": 'M', "Course": 'Math', "Score": '89', "Grade": 'A'},
    ]

    append_rows(filename=filename, content=new_entries)
    read_rows(filename=filename)
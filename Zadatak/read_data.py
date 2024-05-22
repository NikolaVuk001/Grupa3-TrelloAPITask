import json
import os


class FileReader:
    def __init__(self, directory):
        self.directory = directory

    # Printuje ime fajlova
    def print_file_names(self):
        for file in os.listdir(self.directory):
            print(file)

    # Printuje sadrzaj fajlova
    def print_file_contents(self, filename):
        with open(os.path.join(self.directory, filename), 'r') as f:
            data = json.load(f)
            print(json.dumps(data, indent=4))


def main():
    directory = 'D:\zezba'
    reader = FileReader(directory)

    reader.print_file_names()

    for file in os.listdir(directory):
        reader.print_file_contents(file)


if __name__ == '__main__':
    main()
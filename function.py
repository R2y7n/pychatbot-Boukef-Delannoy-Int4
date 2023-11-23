import os


def list_of_files(extension: object, directory: object) -> object:
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

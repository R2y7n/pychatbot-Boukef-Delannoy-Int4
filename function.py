import os
from typing import TextIO


def list_of_files(extension, directory):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def lower_case_convert(extension, directory):
    if not os.path.exists('cleaned'):
        os.makedirs('cleaned')

    text_lower = text.lower()

    file: TextIO
    with open('cleaned/' + text_lower + '.txt', 'w') as file:
        file.write(text_lower)


def retirer_ponctuation(string):
    """Retire les ponctuations d'une chaîne de caractères"""

    if not string.isalpha():
        #On retire tous les caractères avant les majuscule (65) dans la table ascii
        for i in range(65):
            if chr(i) in string:
                string = string.replace(chr(i), "")

        for i in range(91, 97):
            if chr(i) in string:
                string = string.replace(chr(i), "")

        for i in range(123, 128):
            if chr(i) in string:
                string = string.replace(chr(i), "")

        for i in range(128, 192):
            if chr(i) in string:
                string = string.replace(chr(i), "")

        if chr(8217) in string:
            string = string.replace(chr(8217), "")

    return string

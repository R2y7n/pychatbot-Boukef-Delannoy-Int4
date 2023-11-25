import os
from typing import TextIO


def list_of_files(extension, directory):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def lower_case_convert(extension, directory):
    if not os.path.exists('speeches-20231116/cleaned'):
        os.makedirs('speeches-20231116/cleaned')

    text_lower = text.lower()

    file: TextIO
    with open('cleaned/' + text_lower + '.txt', 'w') as file:
        file.write(text_lower)


def tkoff_ponctuation(string):
    """Retire les ponctuations d'une chaîne de caractères"""

    # On retire tous les caractères non alphabétiques selon la table ASCII
    for i in range(32):
        string = string.replace(chr(i), "")

    for i in range(33, 65):
        string = string.replace(chr(i), "")

    for i in range(91, 97):
        string = string.replace(chr(i), "")

    for i in range(123, 127):
        string = string.replace(chr(i), "")

    # Gestion des caractères spéciaux au-delà de la plage ASCII standard
    for i in range(128, 256):
        string = string.replace(chr(i), "")

    return string



#j'ai écris les fonctions grossièrement comme ça
def sort_files_by_extension(directory):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            extension = file.split('.')[-1]
            extension_dir = os.path.join(directory, extension)
            if not os.path.exists(extension_dir):
                os.makedirs(extension_dir)
            os.rename(os.path.join(directory, file), os.path.join(extension_dir, file))



import os
from datetime import datetime

def rename_files_with_date(directory, prefix=""):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            new_name = prefix + datetime.now().strftime("%Y%m%d_") + file
            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))

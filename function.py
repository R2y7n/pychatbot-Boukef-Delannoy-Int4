import os

def list_of_files(directory, extension):
    """create a list containing the files names"""
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def president_name(files_names):
    """create a list containing the names of the presidents"""
    president_names = []
    for file_name in files_names:
        name = ""
        character = 11
        while ord(file_name[character]) == 32 or 65 <= ord(file_name[character]) <= 90 or 97 <= ord(file_name[character]) <= 122:
            name = name + file_name[character]
            character = character + 1
        if name not in president_names:
            president_names.append(name)
    return president_names

def create_cleaned_files(directory):
    """create a cleaned repository with cleaned copies of the files of the original repository within it"""
    if not os.path.exists("cleaned"):
        os.mkdir("cleaned")
    for filename in os.listdir(directory):
        file = open("speeches\\" + filename, "r")
        cleaned_file = open("cleaned\\" + filename, "w")
        cleaned_file.write(file.read())
        file.close()
        cleaned_file.close()
    for filename in os.listdir("./cleaned"):
        if not os.path.exists("cleaned\\" + "cleaned_" + filename):
            file = open("cleaned\\" + filename, "r")
            lower_case_convert(file, filename)
            file.close()
            os.remove("cleaned\\" + filename)
            file = open("cleaned\\" + "lower_casely_cleaned_" + filename, "r")
            remove_punctuation(file, filename)
            file.close()
            os.remove("cleaned\\" + "lower_casely_cleaned_" + filename)
    return "./cleaned"

def lower_case_convert(file, filename):
    """create a copy of a file with all capital letters convert to lower case"""
    texte = file.readlines()
    lower_cased_file = open("cleaned\\" + "lower_casely_cleaned_" + filename, "w")
    for lines in texte:
        for character in lines:
            if 65 <= ord(character) <= 90:
                lower_cased_file.write(chr(ord(character) + 32))
            else:
                lower_cased_file.write(character)
    lower_cased_file.close()

def remove_punctuation(file, filename):
    """create a copy of a file without any form of punctuation of symbol"""
    texte = file.readlines()
    punctuation_removed_file = open("cleaned\\" + "cleaned_" + filename, "w")
    for lines in texte:
        for character in lines:
            if ord(character) <= 31 or 33 <= ord(character) <= 47 or 58 <= ord(character) <= 64 or 91 <= ord(character) <= 96 or 123 <= ord(character) <= 127:
                punctuation_removed_file.write(" ")
            else:
                punctuation_removed_file.write(character)
    punctuation_removed_file.close()

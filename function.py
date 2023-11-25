import os
import math

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
    """create a copy of a file without any form of punctuation, number or symbol"""
    """possibility of improvement by removing after_space variable"""
    texte = file.readlines()
    after_space = True
    punctuation_removed_file = open("cleaned\\" + "cleaned_" + filename, "w")
    for lines in texte:
        for character in lines:
            if ord(character) <= 31 or 33 <= ord(character) <= 64 or 91 <= ord(character) <= 96 or 123 <= ord(character) <= 127:
                if after_space == False:
                    punctuation_removed_file.write(" ")
                    after_space = True
            elif ord(character) <= 32:
                if after_space == False:
                    punctuation_removed_file.write(character)
                    after_space = True
            else:
                punctuation_removed_file.write(character)
                after_space = False
    punctuation_removed_file.close()

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

def words_of_file(file):
    """create a list containing the words of a file"""
    text = file.readlines()
    for line in text:
        words = line.split(" ")
    return words

def tf_of_directory(directory):
    """create a dictionary containing the different TF (Term Frequency) of the different files of the directory"""
    """when the after_space will be remove from remove_punctuation don't forget to adapt here too"""
    tf = {}
    for filename in os.listdir(directory):
        tf[filename] = {}
        file = open("cleaned\\" + filename, "r")
        words = words_of_file(file)
        file.close()
        for word in range(len(words) - 1):
            if words[word] in tf[filename].keys():
                tf[filename][words[word]] = tf[filename][words[word]] + 1
            else:
                tf[filename][words[word]] = 1
        for word in tf[filename]:
            tf[filename][word] = tf[filename][word]/(len(words) - 1)
    return tf

def idf_of_directory(tf):
    """create a dictionary containing the IDF (Inverse Document Frequency) of the directory"""
    idf = {}
    for filename in tf:
        for word in tf[filename]:
            if word in idf.keys():
                idf[word] = idf[word] + 1
            else:
                idf[word] = 1
    for word in idf.keys():
        idf[word] = math.log(len(tf)/idf[word])
    return idf

def tf_idf_of_directory(directory):
    """create a dictionary containing the TF-IDF (Term Frequency-Inverse Document Frequency) of the directory"""
    tf_idf = {}
    tf = tf_of_directory(directory)
    idf = idf_of_directory(tf)
    for filename in tf:
        tf_idf[filename] = {}
        for word in tf[filename]:
            tf_idf[filename][word] = tf[filename][word]*idf[word]
    return tf_idf

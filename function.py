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
    lower_cased_file = open("cleaned\\" + "lower_casely_cleaned_" + filename, "w", encoding = "utf-8")
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
    punctuation_removed_file = open("cleaned\\" + "cleaned_" + filename, "w", encoding = "utf-8")
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
        file = open("speeches\\" + filename, "r", encoding = "utf-8")
        cleaned_file = open("cleaned\\" + filename, "w", encoding = "utf-8")
        cleaned_file.write(file.read())
        file.close()
        cleaned_file.close()
    for filename in os.listdir("./cleaned"):
        if not os.path.exists("cleaned\\" + "cleaned_" + filename):
            file = open("cleaned\\" + filename, "r", encoding = "utf-8")
            lower_case_convert(file, filename)
            file.close()
            os.remove("cleaned\\" + filename)
            file = open("cleaned\\" + "lower_casely_cleaned_" + filename, "r", encoding = "utf-8")
            remove_punctuation(file, filename)
            file.close()
            os.remove("cleaned\\" + "lower_casely_cleaned_" + filename)
    return "./cleaned"

def words_of_file(file):
    """create a list containing the words of a file"""
    text = file.readlines()
    for line in text:
        words = line.split()
    return words

def tf_of_directory(directory):
    """create a dictionary containing the different TF (Term Frequency) of the different files of the directory"""
    """if after_space is remove from remove_punctuation don't forget to adapt here too"""
    tf = {}
    for filename in os.listdir(directory):
        tf[filename] = {}
        file = open("cleaned\\" + filename, "r", encoding = "utf-8")
        words = words_of_file(file)
        file.close()
        for word in range(len(words) - 1):
            tf[filename][words[word]] = tf[filename].get(words[word], 0) + 1
        for word in tf[filename]:
            tf[filename][word] = tf[filename][word]/(len(words) - 1)
    return tf

def idf_of_directory(tf):
    """create a dictionary containing the IDF (Inverse Document Frequency) of the directory"""
    idf = {}
    for filename in tf:
        for word in tf[filename]:
            idf[word] = idf.get(word, 0) + 1
    for word in idf.keys():
        idf[word] = math.log(len(tf)/idf[word])
    return idf

def tf_idf_of_directory(directory):
    """create a dictionary containing the TF-IDF (Term Frequency-Inverse Document Frequency) of the directory"""
    """it would probably be better for the following functions to have the TF-IDF as a matrix instead of a dictionary"""
    tf_idf = {}
    tf = tf_of_directory(directory)
    idf = idf_of_directory(tf)
    for filename in tf:
        tf_idf[filename] = {}
        for word in tf[filename]:
            tf_idf[filename][word] = tf[filename][word]*idf[word]
    return tf_idf

def tf_idf_0(tf_idf):
    """create a list containing the unimportant words"""
    """if the type of the TF-IDF is changed to matrix we could use simply a list directly instead of having to use a dictionary"""
    first_file_check = True
    for filename in tf_idf:
        for word in tf_idf[filename]:
            if first_file_check == True:
                dictionary_unimportant_words = tf_idf[filename]
            else:
                if word in dictionary_unimportant_words and tf_idf[filename][word] != 0:
                    del dictionary_unimportant_words[word]
        first_file_check = False
    unimportant_words = []
    for word in dictionary_unimportant_words:
        unimportant_words.append(word)
    return unimportant_words

def highest_tf_idf(tf_idf):
    """create a list containing the words with the highest TF-IDF"""
    """if the type of the TF-IDF is changed to matrix we could use simply a list directly instead of having to use a dictionary"""
    first_file_check = True
    dictionary_highest_tf_idf_words = {}
    for filename in tf_idf:
        for word in tf_idf[filename]:
            if first_file_check == True:
                dictionary_highest_tf_idf_words[word] = tf_idf[filename][word]
            else:
                add = False
                delete = False
                for current_highest_tf_idf_words in dictionary_highest_tf_idf_words:
                    if tf_idf[filename][word] > dictionary_highest_tf_idf_words[current_highest_tf_idf_words]:
                        delete = True
                    elif tf_idf[filename][word] == dictionary_highest_tf_idf_words[current_highest_tf_idf_words]:
                        add = True
                if delete == True:
                    dictionary_highest_tf_idf_words = {}
                    dictionary_highest_tf_idf_words[word] = tf_idf[filename][word]
                elif add == True:
                    dictionary_highest_tf_idf_words[word] = tf_idf[filename][word]
            first_file_check = False
    highest_tf_idf_words = []
    for word in dictionary_highest_tf_idf_words:
        highest_tf_idf_words.append(word)
    return highest_tf_idf_words

def groups_of_files_by_name(directory, list_of_names):
    """create a dictionary containing lists of files grouped by name of the author"""
    groups_of_files = {}
    for filename in os.listdir(directory):
        for name in list_of_names:
            if name in filename:
                if name not in groups_of_files:
                    groups_of_files[name] = [filename]
                else:
                    groups_of_files[name].append(filename)
    print(groups_of_files)
    return groups_of_files

def most_repeated_words_in_group_of_files(groups_of_files, name_of_groupe):
    """create a list containing the most repeated words in the group of file"""
    """if after_space is remove from remove_punctuation don't forget to adapt here too"""
    group_of_files = groups_of_files[name_of_groupe]
    occurrences = {}
    for filename in group_of_files:
        file = open("cleaned\\" + filename, "r", encoding = "utf-8")
        words = words_of_file(file)
        file.close()
        for word in range(len(words) - 1):
            occurrences[words[word]] = occurrences.get(words[word], 0) + 1
    most_repeated_words = []
    most_repeated_words_occurrences = 0
    for word in occurrences:
        if occurrences[word] == most_repeated_words_occurrences:
            most_repeated_words.append(word)
        elif occurrences[word] > most_repeated_words_occurrences:
            most_repeated_words_occurrences = occurrences[word]
            most_repeated_words = [word]
    return most_repeated_words

def groups_of_files_using_word(groups_of_files, names, target_word):
    """create two lists, the first one containing all the groups of files using the target word and the second one the groups of files using it the most"""
    """if after_space is remove from remove_punctuation don't forget to adapt here too"""
    occurrences_by_group_of_files = []
    for number_group_of_files in range(len(names)):
        occurrences_by_group_of_files.append(0)
        for filename in groups_of_files[names[number_group_of_files]]:
            file = open("cleaned\\" + filename, "r", encoding = "utf-8")
            words = words_of_file(file)
            file.close()
            print(words)
            for word in range(len(words) - 1):
                if words[word] == target_word:
                    occurrences_by_group_of_files[number_group_of_files] = occurrences_by_group_of_files[number_group_of_files] + 1
    groups_of_files_using_target_word = []
    most_repeated = []
    most_repeated_occurrences = 0
    for number_group_of_files in range(len(occurrences_by_group_of_files)):
        if occurrences_by_group_of_files[number_group_of_files] != 0:
            groups_of_files_using_target_word.append(names[number_group_of_files])
            if occurrences_by_group_of_files[number_group_of_files] == most_repeated_occurrences:
                most_repeated.append(names[number_group_of_files])
            elif occurrences_by_group_of_files[number_group_of_files] > most_repeated_occurrences:
                most_repeated_occurrences = occurrences_by_group_of_files[number_group_of_files]
                most_repeated = [names[number_group_of_files]]
    return groups_of_files_using_target_word, most_repeated

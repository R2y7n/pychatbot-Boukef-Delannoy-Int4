import os
import math
#we could rearrange the order of the functions here to make it more clean

"""1. Manipulation and Organisation of Files"""

def list_of_files(directory, extension):
    #create a list containing the files names
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def authors_names(files_names):
    #create a list containing the names of the authors
    list_authors_names = []
    for file_name in files_names:
        name = ""
        character = 19
        while ord(file_name[character]) == 32 or 65 <= ord(file_name[character]) <= 90 or 97 <= ord(file_name[character]) <= 122:
            name = name + file_name[character]
            character = character + 1
        if name not in list_authors_names:
            list_authors_names.append(name)
    return list_authors_names

def files_and_authors_names_by_dates(files_names, dates_of_authors):
    #sort the list containing the names of the authors by dates
    list_authors_names = authors_names(files_names)
    for tested_name in range(len(list_authors_names) - 1):
        for name in range(tested_name + 1, len(list_authors_names)):
            if dates_of_authors[list_authors_names[name]] < dates_of_authors[list_authors_names[tested_name]]:
                list_authors_names[name], list_authors_names[tested_name] = list_authors_names[tested_name], list_authors_names[name]
    sorted_files_names = []
    for name in list_authors_names:
        for filenames in files_names:
            if name in filenames:
                sorted_files_names.append(filenames)
    return sorted_files_names, list_authors_names

def words_of_file(file):
    #create a list containing the words of a file
    text = file.readlines()
    for line in text:
        words = line.split()
    return words

def create_cleaned_files(directory):
    #create a cleaned repository with cleaned copies of the files of the original repository within it
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
            remove_punctuation_and_special_character(file, filename)
            file.close()
            os.remove("cleaned\\" + "lower_casely_cleaned_" + filename)
    return "./cleaned"

"""2. Pretreatment and Cleaning of Text"""

def lower_case_convert(file, filename):
    #create a copy of a file with all capital letters convert to lower case
    texte = file.readlines()
    lower_cased_file = open("cleaned\\" + "lower_casely_cleaned_" + filename, "w", encoding = "utf-8")
    for lines in texte:
        for character in lines:
            if 65 <= ord(character) <= 90:
                lower_cased_file.write(chr(ord(character) + 32))
            else:
                lower_cased_file.write(character)
    lower_cased_file.close()

def remove_punctuation_and_special_character(file, filename):
    #create a copy of a file without any form of punctuation, number or symbol
    #possibility of improvement by removing after_space variable
    texte = file.readlines()
    after_space = True
    punctuation_removed_file = open("cleaned\\" + "cleaned_" + filename, "w", encoding = "utf-8")
    for lines in texte:
        for character in lines:
            if ord(character) <= 64 or 91 <= ord(character) <= 96 or 123 <= ord(character) <= 127:
                if after_space == False:
                    punctuation_removed_file.write(" ")
                    after_space = True
            else:
                punctuation_removed_file.write(character)
                after_space = False
    punctuation_removed_file.close()

def unimportant_words_in_files(tf_idf, groups_of_files):
    #create a list containing the unimportant words with regard to the groups of files used
    if groups_of_files == "directory":
        unimportant_words = tf_idf_0(tf_idf)
    else:
        unimportant_words = unimportant_words_by_groups(tf_idf, groups_of_files)
    if unimportant_words == []:
        return None
    return unimportant_words

def unimportant_words_by_groups(tf_idf, groups_of_files):
    #create a list containing the words used in all the groups of files
    #if the type of the TF-IDF was changed to matrix we could probably use simply a list directly instead of having to use a dictionary
    unimportant_words = []
    first_group_check = True
    for group_of_files in groups_of_files:
        still_unimportant_words = []
        for filename in groups_of_files[group_of_files]:
            if first_group_check == True:
                for word in tf_idf[filename]:
                    if word not in unimportant_words:
                        unimportant_words.append(word)
            else:
                for word in unimportant_words:
                    if word in tf_idf[filename] and word not in still_unimportant_words:
                        still_unimportant_words.append(word)
        if first_group_check == False:
            unimportant_words = still_unimportant_words
        first_group_check = False
    return unimportant_words

def most_repeated_not_unimportant_words_in_group_of_files(tf_idf, groups_of_files, name_of_group):
    #create a list containing the most repeated words in the group of files
    group_of_files = groups_of_files[name_of_group]
    occurrences = {}
    unimportant_words = unimportant_words_in_files(tf_idf, "directory")

    for filename in group_of_files:
        with open("cleaned\\" + filename, "r", encoding="utf-8") as file:
            words = words_of_file(file)
            for word in words:
                if word not in unimportant_words:
                    occurrences[word] = occurrences.get(word, 0) + 1

    if not occurrences:
        return None

    # find the most repeated word
    max_occurrences = max(occurrences.values())
    most_repeated_words = [word for word, count in occurrences.items() if count == max_occurrences]

    print(unimportant_words)
    print(most_repeated_words)

    return most_repeated_words


"""3. Analysis and Treatment of Textual Datas"""

def tf_of_files(files_names):
    #create a dictionary containing the different TF (Term Frequency) of the files
    #if after_space is remove from remove_punctuation_and_special_character don't forget to adapt here too
    tf = {}
    for filename in files_names:
        tf[filename] = {}
        file = open("cleaned\\" + filename, "r", encoding = "utf-8")
        words = words_of_file(file)
        file.close()
        for word in range(len(words)):
            tf[filename][words[word]] = tf[filename].get(words[word], 0) + 1
        for word in tf[filename]:
            tf[filename][word] = tf[filename][word]/len(words)
    return tf

def idf_of_files(tf):
    #create a dictionary containing the IDF (Inverse Document Frequency) of the files
    idf = {}
    for filename in tf:
        for word in tf[filename]:
            idf[word] = idf.get(word, 0) + 1
    for word in idf.keys():
        idf[word] = math.log10(len(tf)/idf[word])
    return idf

def tf_idf_of_files(files_names):
    #create a dictionary containing the TF-IDF (Term Frequency-Inverse Document Frequency) of the files
    #it would probably be better for the following functions to have the TF-IDF as a matrix instead of a dictionary
    tf_idf = {}
    tf = tf_of_files(files_names)
    idf = idf_of_files(tf)
    for filename in tf:
        tf_idf[filename] = {}
        for word in tf[filename]:
            tf_idf[filename][word] = tf[filename][word]*idf[word]
    return tf_idf, idf

def groups_of_files_by_name(file_names, list_of_names):
    # create a dictionary containing lists of files grouped by name of the author
    #Here's an optimized version of the function.
    return {name: [filename for filename in file_names if name in filename] for name in list_of_names}

def tf_idf_0(tf_idf):
    #create a list containing the unimportant words
    unimportant_words = []
    for filename in tf_idf:
        for word in tf_idf[filename]:
            if word not in unimportant_words and tf_idf[filename][word] == 0:
                unimportant_words.append(word)
    return unimportant_words

def highest_tf_idf(tf_idf):
    #create a list containing the words with the highest TF-IDF
    #if the type of the TF-IDF was changed to matrix we could probably use simply a list directly instead of having to use a dictionary
    #it would be cool to adapt it to do by groups of files
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
    if highest_tf_idf_words == []:
        return None
    return highest_tf_idf_words

def groups_of_files_using_word(groups_of_files, target_word):
    # Créer deux listes : une pour les groupes de fichiers utilisant le mot cible, l'autre pour ceux l'utilisant le plus
    occurrences_by_group_of_files = {}

    # Compter les occurrences du mot cible dans chaque groupe de fichiers
    for group_name, filenames in groups_of_files.items():
        count = 0
        for filename in filenames:
            with open("cleaned\\" + filename, "r", encoding="utf-8") as file:
                words = words_of_file(file)
                count += words.count(target_word)
        if count > 0:
            occurrences_by_group_of_files[group_name] = count

    if not occurrences_by_group_of_files:
        return None, None

    # Séparer les groupes utilisant le mot cible de ceux l'utilisant le plus
    groups_using_target_word = list(occurrences_by_group_of_files.keys())
    max_occurrences = max(occurrences_by_group_of_files.values())
    most_repeated = [group for group, count in occurrences_by_group_of_files.items() if count == max_occurrences]

    return groups_using_target_word, most_repeated

def first_to_use(groups_of_files, target_word):
    #return the name of the first author using the target word if there is one and None if there is none
    file_using_target_word = groups_of_files_using_word(groups_of_files, target_word)[0]
    if file_using_target_word:
        return file_using_target_word[0]
    else:
        return None

def not_unimportant_words_used_by_all_groups(tf_idf, groups_of_files):
    #create a list of all not unimportant words used by all authors
    universal_unimportant_words = unimportant_words_in_files(tf_idf, "directory")
    local_unimportant_words = unimportant_words_in_files(tf_idf, groups_of_files)
    not_unimportant_words_used_by_all = []
    for word in local_unimportant_words:
        if word not in universal_unimportant_words:
            not_unimportant_words_used_by_all.append(word)
    if not_unimportant_words_used_by_all == []:
        return None
    return not_unimportant_words_used_by_all



#question part

def lower_case_convert_question(question):
    #create a copy of the question with all capital letters convert to lower case
    lower_cased_question = ""
    for character in question:
        if 65 <= ord(character) <= 90:
            lower_cased_question = lower_cased_question + chr(ord(character) + 32)
        else:
            lower_cased_question = lower_cased_question + character
    return lower_cased_question

def remove_punctuation_and_special_character_question(question):
    #create a copy of the question without any form of punctuation, number or symbol
    #possibility of improvement by removing after_space variable
    after_space = True
    punctuation_removed_question = ""
    for character in question:
        if ord(character) <= 64 or 91 <= ord(character) <= 96 or 123 <= ord(character) <= 127:
            if after_space == False:
                punctuation_removed_question = punctuation_removed_question + " "
                after_space = True
        else:
            punctuation_removed_question = punctuation_removed_question + character
            after_space = False
    return punctuation_removed_question

def list_words_in_question(question):
    #create a list containing the words of the question
    question_words = lower_case_convert_question(question)
    question_words = remove_punctuation_and_special_character_question(question_words)
    question_words = question_words.split()
    return question_words

def words_in_question_and_corpus(question_words, tf_idf):
    #create a set containing the words that are in the question and in the corpus
    intersections_question_corpus = set()
    for filename in tf_idf:
        for word in question_words:
            if word in tf_idf[filename]:
                intersections_question_corpus.add(word)
    return intersections_question_corpus

def corpus_words_list(file_names):
    #create a list of the words in the corpus
    corpus_words = []
    for filename in file_names:
        file = open("cleaned\\" + filename, "r", encoding = "utf-8")
        file_words = words_of_file(file)
        for word in file_words:
            if word not in corpus_words:
                corpus_words.append(word)
    return corpus_words

def tf_idf_matrix_of_corpus(corpus_words, tf_idf):
    #create the TF-IDF matrix
    tf_idf_matrix = []
    file_number = 0
    for filename in tf_idf:
        tf_idf_matrix.append([])
        for word in corpus_words:
            tf_idf_matrix[file_number].append(tf_idf[filename].get(word, 0))
        file_number = file_number + 1
    return tf_idf_matrix

def tf_of_intersections_question_corpus(question_words, intersections_question_corpus):
    #create a dictionary containing the TF (Term Frequency) of the question
    #if after_space is remove from remove_punctuation_and_special_character don't forget to adapt here too
    tf_intersections_question_corpus = {}
    for word in question_words:
        if word in intersections_question_corpus:
            tf_intersections_question_corpus[word] = tf_intersections_question_corpus.get(word, 0) + 1
    for word in tf_intersections_question_corpus:
        tf_intersections_question_corpus[word] = tf_intersections_question_corpus[word]/len(question_words)
    return tf_intersections_question_corpus

def tf_idf_question_vector(question_words, intersections_question_corpus, idf):
    #create a vector for the question depending on the TF of the intersections question corpus and the IDF
    question_vector = []
    tf_intersections_question_corpus = tf_of_intersections_question_corpus(question_words, intersections_question_corpus)
    for word in idf:
        question_vector.append(tf_intersections_question_corpus.get(word, 0)*idf[word])
    return question_vector

def dot_function_of_two_vectors(vector1, vector2):
    #compute the dot product of two vectors
    dot_product = 0
    for dimension in range(len(vector1)):
        dot_product = dot_product + vector1[dimension]*vector2[dimension]
    return dot_product

def norm_vector(vector):
    #compute the norm of a vector
    norm = 0
    for dimension in range(len(vector)):
        norm = norm + vector[dimension]**2
    norm = math.sqrt(norm)
    return norm

def similarity_between_two_vectors(vector1, vector2):
    #compute the similarity of two vectors by finding the cosine of their angle
    if norm_vector(vector1) == 0:
        return None
    cosine_similarity = dot_function_of_two_vectors(vector1, vector2)/(norm_vector(vector1)*norm_vector(vector2))
    return cosine_similarity

def equivalent_cleaned_doc_speeches(filename):
    #give the equivalent of a cleaned file int the speeches directory
    speeches_equivalent = ""
    for character_number in range(8, len(filename)):
        speeches_equivalent = speeches_equivalent + filename[character_number]
    return speeches_equivalent

def most_relevant_documents_list(tf_idf_matrix, question_vector, files_names):
    #find the most relevant document by computing the similarities between the question vector and the documents vectors
    max_similarity = []
    max_similarity_value = 0
    for file_number in range(len(files_names)):
        similarity = similarity_between_two_vectors(question_vector, tf_idf_matrix[file_number])
        if similarity == None:
            return None
        if similarity > max_similarity_value:
            max_similarity = [files_names[file_number]]
            max_similarity_value = similarity
        elif similarity == max_similarity_value:
            max_similarity.append(files_names[file_number])
    for file_number in range(len(max_similarity)):
        max_similarity[file_number] = equivalent_cleaned_doc_speeches(max_similarity[file_number])
    return max_similarity

def highest_tf_idf_question(corpus_words, question_vector):
    #create a list containing the words with the highest TF-IDF in the question
    highest_tf_idf_question_words = []
    highest_tf_idf_question_words_value = 0
    for word_number in range(len(corpus_words)):
        if question_vector[word_number] > highest_tf_idf_question_words_value:
            highest_tf_idf_question_words = [corpus_words[word_number]]
            highest_tf_idf_question_words_value = question_vector[word_number]
        elif question_vector[word_number] == highest_tf_idf_question_words_value:
            highest_tf_idf_question_words.append(corpus_words[word_number])
    if highest_tf_idf_question_words_value == 0:
        return None
    return highest_tf_idf_question_words

def equivalent_speeches_doc_cleaned(filename):
    #give the equivalent of a speeches file int the cleaned directory
    return "cleaned_" + filename

def first_occurrence_word_in_cleaned_file(filename, target_word):
    #return the word number of the fist occurrence of a word in a file
    cleaned_file = open("cleaned\\" + equivalent_speeches_doc_cleaned(filename), "r", encoding="utf-8")
    file_words = words_of_file(cleaned_file)
    cleaned_file.close()
    for file_word_number in range(len(file_words)):
        if file_words[file_word_number] == target_word:
            return file_word_number
    return None

def first_sentence_word_in_file(filename, target_word):
    #return the first sentence containing a word in a file
    target_word_number = first_occurrence_word_in_cleaned_file(filename, target_word)
    if target_word_number == None:
        return None
    file = open("speeches\\" + filename, "r", encoding="utf-8")
    lines = file.readlines()
    file.close()
    sentence = ""
    in_word = False
    word_number = -1
    target_word_in_sentence = False
    for line in lines:
        for character in line:
            if 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122 or 128 <= ord(character):
                if in_word == False:
                    word_number = word_number + 1
                    in_word = True
            else:
                in_word = False
            if word_number == target_word_number:
                target_word_in_sentence = True
            if ord(character) <= 31 or ord(character) == 46 or ord(character) == 63 or ord(character) == 127:
                if target_word_in_sentence == True:
                    return sentence
                sentence = ""
            else:
                sentence = sentence + character

def first_sentence_highest_tf_idf_words_in_documents(most_relevant_documents, highest_tf_idf_question_words):
    #return the first sentence containing one of the word with the highest TF-IDF in the most relevant documents
    for file_number in range(len(most_relevant_documents)):
        for word in highest_tf_idf_question_words:
            sentence = first_sentence_word_in_file(most_relevant_documents[file_number], word)
            if sentence != None:
                return sentence
    return None

dimport sys
from function import *

if __name__ == '__main__':
    # ///we could maybe rearrange the order of the calls of the functions here to make it more clean
    # ///we could potentially merge files_and_authors_names_by_dates and groups_of_files

    # Title:
    print("Python project My first chatBot:", end="\n\n")

    # Initialisation:

    # here we define the speeches directory as directory
    # if the speeches directory is not found then it ends the program with a custom error
    if not os.path.exists("speeches"):
        sys.exit("speeches directory is missing")
    directory = "./speeches"

    # here we create the cleaned directory and define it as cleaned_directory
    # if the cleaned directory already exists we can just define it as cleaned_directory
    if not os.path.exists("cleaned"):
        clean_directory = create_cleaned_files(directory)
    else:
        clean_directory = "./cleaned"

    # here we make the list of the cleaned files names and president names and sort them by date of presidents
    files_names = list_of_files(clean_directory, "txt")
    dates_presidents = {"Giscard dEstaing": (1974, 1981), "Mitterrand": (1981, 1995), "Chirac": (1995, 2007), "Sarkozy": (2007, 2012), "Hollande": (2012, 2017), "Macron": (2017, 2022)}
    files_names, presidents_names = files_and_authors_names_by_dates(files_names, dates_presidents)

    # here we create gather the speeches made by the same president to make groups
    groups_of_files = groups_of_files_by_name(files_names, presidents_names)

    # here we make the TF-IDF of th cleaned files as a dictionary
    tf_idf, idf = tf_idf_of_files(files_names)

    # Mode selection:

    # here we ask the user which one of the 2 existing modes he wants to use
    mode_choice = None
    while mode_choice != "Q/A Mode" and mode_choice != "Chatbot Mode" and mode_choice != "quit":
        if mode_choice != None:
            print("This is not an existing mode", end="\n\n")
        print("Which mode would you like to use:")
        print('Enter "Q/A Mode" to ask one of the predefined questions')
        print('Enter "Chatbot Mode" to ask a question to "M.Bot" our esteemed president')
        print('Enter "quit" to quit the program')
        mode_choice = input()
        print()

        # "Q/A Mode":

        # in "Q/A Mode" you can only ask predefined questions, but, at least, the answers will make sense (no offence M.Bot, we like you very much but...)
        # here we check the selected mode and print its title
        if mode_choice == "Q/A Mode":
            print("Q/A Mode :", end="\n\n")

            # here we check if the user wants to get out of the mode or the program
            question_choice = None
            while question_choice != "quit mode" and question_choice != "quit":

                # here we check if the user enter an invalid value
                if question_choice != None:
                    print("This is not one of the possible questions", end="\n\n")

                # here the user select the question he want to ask
                print("To see the unimportant words in the document corpus, enter 1")
                print("To see the words with the highest TF-IDF score, enter 2")
                print("To see the most repeated words by a certain president, enter 3")
                print("To see the presidents who said a certain word and the ones who said it the most, enter 4")
                print("To see the first president who said a certain word or another certain word, enter 5")
                print("To see the words that all the presidents have pronounced but that did not appears in all of their speeches, enter 6")
                print('To quit "Q/A Mode", enter "quit mode"')
                print('To quit the program, enter "quit"')
                question_choice = input()
                print()

                # here we check if the user asked for the first question and if yes we print the answer and the choice of the question go back to None
                if question_choice == "1":
                    unimportant_words = unimportant_words_in_files(tf_idf, "directory")
                    if unimportant_words == None:
                        print("There are no unimportant words in the document corpus", end="\n\n")
                    else:
                        print("The unimportant words in the document corpus are: ")
                        print(unimportant_words, end="\n\n")
                    question_choice = None

                # here we check if the user asked for the second question and if yes we print the answer and the choice of the question go back to None
                elif question_choice == "2":
                    words_with_highest_tf_idf = highest_tf_idf(tf_idf)
                    if words_with_highest_tf_idf == None:
                        print("There are no words in the document corpus", end="\n\n")
                    else:
                        print("The words with the highest TF-IDF in the corpus are: ")
                        print(words_with_highest_tf_idf, end="\n\n")
                    question_choice = None

                # here we check if the user asked for the third question and if yes we print the answer and the choice of the question go back to None
                elif question_choice == "3":
                    print(presidents_names)
                    president_choice = input("Enter the name of the president: ")
                    print()
                    if president_choice not in presidents_names:
                        print(f'There is no french president called "{president_choice}"', end="\n\n")
                    else:
                        most_repeated_words_president = most_repeated_not_unimportant_words_in_group_of_files(tf_idf, groups_of_files, president_choice)
                        if most_repeated_words_president == None:
                            print(f"It seems president {president_choice} did not say anything interesting", end="\n\n")
                        else:
                            print(f"The most repeated words by president {president_choice} are: ")
                            print(most_repeated_words_president, end="\n\n")
                    question_choice = None

                # here we check if the user asked for the forth question and if yes we print the answer and the choice of the question go back to None
                elif question_choice == "4":
                    target_word = input("Enter the word: ")
                    print()
                    presidents_using_target_word, presidents_using_the_most_target_word = groups_of_files_using_word(groups_of_files, target_word)
                    if presidents_using_target_word == None:
                        print(f'There are no presidents who said "{target_word}"', end="\n\n")
                    else:
                        print(f'The presidents who said the word "{target_word}" are: ')
                        print(presidents_using_target_word)
                        print("And the ones who said it the most are: ")
                        print(presidents_using_the_most_target_word, end="\n\n")
                    question_choice = None

                # here we check if the user asked for the fith question and if yes we print the answer and the choice of the question go back to None
                elif question_choice == "5":
                    word1 = input("Enter the first word: ")
                    first_to_use_word1 = first_to_use(groups_of_files, word1)
                    word2 = input("Enter the second word: ")
                    first_to_use_word2 = first_to_use(groups_of_files, word2)
                    print()
                    if first_to_use_word1 == None:
                        if first_to_use_word2 == None:
                            print("None of them used one of those words", end="\n\n")
                        else:
                            print(f'The first president who said "{word1}" or "{word2}" was: ')
                            print(first_to_use_word2)
                            print(f'By saying "{word2}"', end="\n\n")
                    elif first_to_use_word2 == None:
                        print(f'The first president who said "{word1}" or "{word2}" was: ')
                        print(first_to_use_word1)
                        print(f'By saying "{word1}"', end="\n\n")
                    elif first_to_use_word1 < first_to_use_word2 in presidents_names:
                        print(f'The first president who said "{word1}" or "{word2}" was: ')
                        print(first_to_use_word1)
                        print(f'By saying "{word1}"', end="\n\n")
                    elif first_to_use_word2 < first_to_use_word1 in presidents_names:
                        print(f'The first president who said "{word1}" or "{word2}" was: ')
                        print(first_to_use_word2)
                        print(f'By saying "{word2}"', end="\n\n")
                    else:
                        print(f'The first president who said "{word1}" or "{word2}" was: ')
                        print(first_to_use_word1)
                        print("By saying both", end="\n\n")
                    question_choice = None

                # here we check if the user asked for the sixth question and if yes we print the answer and the choice of the question go back to None
                elif question_choice == "6":
                    words_used_by_all_but_not_all_speeches = not_unimportant_words_used_by_all_groups(tf_idf, groups_of_files)
                    if words_used_by_all_but_not_all_speeches == None:
                        print("There are no words that all the presidents have pronounced but that did not appear in all of their speeches", end="\n\n")
                    else:
                        print("The words that all presidents have pronounced but that did not appear in all of their speeches are: ")
                        print(words_used_by_all_but_not_all_speeches, end="\n\n")
                    question_choice = None

                # here we check if the user asked for quiting the mode
                elif question_choice == "quit mode":
                    quit_mode_choice = None

                    # here we check if the user really wants to do so, if yes the choice of the mode go back to None and if no the choice of the question go back to None
                    while quit_mode_choice != "yes" and quit_mode_choice != "no":
                        print("Are you sure you want to quit that mode")
                        print('"yes" or "no"')
                        quit_mode_choice = input()
                        print()
                        if quit_mode_choice == "yes":
                            mode_choice = None
                        elif quit_mode_choice == "no":
                            question_choice = None

                # here we check if the user asked for quiting the program
                elif question_choice == "quit":
                    quit_choice = None

                    # here we check if the user really wants to do so, if yes we just let the program close and if no the choice of the question go back to None
                    while quit_choice != "YES" and quit_choice != "NO":
                        print("Are you sure you want to quit the program")
                        print('"YES" or "NO"')
                        quit_choice = input()
                        print()
                        if quit_choice == "YES":
                            print("Goodbye")
                        elif quit_choice == "NO":
                            question_choice = None

        # "Chatbot Mode":

        # in "Chatbot Mode" you can ask questions to M.Bot himself, what an honor, but, be careful, sometimes his answers are just too smart for us
        # here we check the selected mode, print its title and then the wonderful M.Bot introduce himself to us with this beautiful french language of him
        if mode_choice == "Chatbot Mode":
            print("Chatbot Mode: ", end="\n\n")
            print('M.Bot : Bonjour cher compatriote ! Ou plutôt "Hello deer compatriote !" comme disent les anglais.', end="\n\n")

            # here we check if the user wants to get out of the mode or the program
            question = None
            while question != "arrêter de poser des questions" and question != "partir":

                # here the fantastic M.Bot ask if we have a question (it's so considerate of him really, such a great president)
                print('M.Bot : Avez-vous une question a me poser ? Ou peut-être préféreriez-vous "arrêter de poser des questions" ou "partir" ?')
                question = input()
                print()

                # here we check if the user asked for quiting the mode
                if question == "arrêter de poser des questions":
                    print("M.Bot : Je vous demande de vous arrêter !")

                    # here we check if the user really wants to do so, if yes the choice of the mode go back to None
                    quit_mode_choice = None
                    while quit_mode_choice != "oui" and quit_mode_choice != "non":
                        print("M.Bot : Etes-vous bien sûr de vouloir arrêter de poser des questions ?")
                        print('"oui" ou "non"')
                        quit_mode_choice = input()
                        print()
                        if quit_mode_choice == "oui":
                            mode_choice = None
                            print("M.Bot : Et dans ces temps difficiles, où le mal rôde et frappe dans le monde, je souhaite que la providence veille sur la France, pour son bonheur, pour son bien et pour sa grandeur.")
                            print("M.Bot : Au revoir !", end="\n\n")
                        elif quit_mode_choice == "non":
                            question = None

                # here we check if the user asked for quiting the program
                elif question == "partir":
                    print("M.Bot : Je vous demande de vous arrêter !")

                    # here we check if the user really wants to do so, if yes we just let the program close
                    quit_choice = None
                    while quit_choice != "OUI" and quit_choice != "NON":
                        print("M.Bot : Etes-vous bien sûr de vouloir partir ?")
                        print('"OUI" ou "NON"')
                        quit_choice = input()
                        print()
                        if quit_choice == "OUI":
                            print("M.Bot : Et dans ces temps difficiles, où le mal rôde et frappe dans le monde, je souhaite que la providence veille sur la France, pour son bonheur, pour son bien et pour sa grandeur.")
                            print("M.Bot : Au revoir !", end="\n\n")
                        elif quit_choice == "NON":
                            question = None

                # here we check if the user asked "Why french?", and to be completely honest the fact that M.Bot give some of its precious time to answer such a silly question just show how attentive and patient he is
                elif question == "Pourquoi du français ?":
                    print('M.Bot : Mais vous avez tout à fait raison, monsieur, de poser la question.')
                    print("M.Bot : J'ai décidé de me conformer au deuxième article de notre belle constitution qui, je cite, dit :", '"La langue de la République est le français."', "Vive la république et vive la France !", end="\n\n")

                # here we check if the user asked any other question
                else:

                    # here we tokenize the question
                    question_words = list_words_in_question(question)

                    # here we search for the question words in the corpus
                    intersections_question_corpus = words_in_question_and_corpus(question_words, tf_idf)

                    # here we calculate the TF-IDF vector for the terms in the question
                    tf_intersections_question_corpus = tf_of_intersections_question_corpus(question_words, intersections_question_corpus)
                    question_vector = tf_idf_question_vector(question_words, intersections_question_corpus, idf)

                    # here we transform TF-IDF into a matrix
                    corpus_words = corpus_words_list(files_names)
                    tf_idf_matrix = tf_idf_matrix_of_corpus(corpus_words, tf_idf)

                    # here we calculate what are the most relevant documents
                    most_relevant_documents = most_relevant_documents_list(tf_idf_matrix, question_vector, files_names)

                    # here we check if all the words in the question are either not in the corpus or unimportant words because if yes then there would be a division by 0
                    if most_relevant_documents == None:
                        print("M.Bot : Je ne vous ai pas compris !", end="\n\n")
                    else:

                        # here we calculate what are the most important words in the question
                        highest_tf_idf_question_words = highest_tf_idf_question(corpus_words, question_vector)

                        # here we are generating a response to the question
                        sentence = first_sentence_highest_tf_idf_words_in_documents(question_words, most_relevant_documents, highest_tf_idf_question_words)

                        # here we are checking if a response actually exist in the document because all the most important words could not at all in the most relevent documents and only apear in less relevant documents
                        # also M.Bot is just too much for us to understand
                        if sentence == None:
                            print("M.Bot : Tout ce que je peux vous dire, c'est que la pomme est un fruit sympatique.", end="\n\n")
                        else:
                            print("M.Bot :", sentence, end="\n\n")

        # Quit program:

        # here we check if the user asked for quiting the program
        if mode_choice == "quit":
            quit_choice = None

            # here we check if the user really wants to do so, if yes we just let the program close and if no we make the choice of the mode go back to None
            while quit_choice != "YES" and quit_choice != "NO":
                print("Are you sure you want to quit the program")
                print('"YES" or "NO"')
                quit_choice = input()
                print()
                if quit_choice == "YES":
                    print("Goodbye")
                elif quit_choice == "NO":
                    mode_choice = None

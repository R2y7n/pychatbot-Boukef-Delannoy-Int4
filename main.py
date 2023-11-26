from function import *

if __name__ == '__main__':
    #we could rearrange the order of the calls of the functions here to make it more clean
    directory = "./speeches"
    files_names = list_of_files(directory, "txt")
    dates_presidents = {"Giscard dEstaing": (1974, 1981), "Mitterrand": (1981, 1995), "Chirac": (1995, 2007), "Sarkozy": (2007, 2012), "Hollande": (2012, 2017), "Macron": (2017, 2022)}
    presidents_names = authors_names_by_dates(files_names, dates_presidents)
    print(presidents_names)
    #if the code has already been executed no need to execute it again
    if not os.path.exists("cleaned"):
        clean_directory = create_cleaned_files(directory)
    else:
        clean_directory = "./cleaned"
    files_names = list_of_files(clean_directory, "txt")
    tf_idf = tf_idf_of_directory(clean_directory)
    groups_of_files = groups_of_files_by_name(files_names, presidents_names)
    print(groups_of_files)
    print("If you want to see the unimportant words in the document corpus, enter 1")
    print("If you want to see the words with the highest TF-IDF score, enter 2")
    print("If you want to see the most repeated words by president Chirac, enter 3")
    print('If you want to see the presidents who said the word "Nation" and the ones who said it the most, enter 4')
    print('If you want to see the first president who said "climat" or "écologie", enter 5')
    print("If you want to see which words that all the presidents have pronounced but that did appeared in all of their speeches, enter 6")
    print()
    user_choice = int(input())
    print()
    if user_choice == 1:
        unimportant_words = unimportant_words_in_files(tf_idf, "directory")
        if unimportant_words == None:
            print("There are no unimportant words in the document corpus.")
        else:
            print("The unimportant words in the document corpus are: ")
            print(unimportant_words)
    elif user_choice == 2:
        words_with_highest_tf_idf = highest_tf_idf(tf_idf)
        if words_with_highest_tf_idf == None:
            print("There are no words in the document corpus.")
        else:
            print("The words with the highest TF-IDF in the corpus are: ")
            print(words_with_highest_tf_idf)
    elif user_choice == 3:
        most_repeated_words_Chirac = most_repeated_words_in_group_of_files(groups_of_files, "Chirac")
        if most_repeated_words_Chirac == None:
            print("President Chirac did not say anything.")
        else:
            print("The most repeated words by president Chirac are: ")
            print(most_repeated_words_Chirac)
    elif user_choice == 4:
        presidents_using_target_word, presidents_using_the_most_target_word = groups_of_files_using_word(groups_of_files, "nation")
        if presidents_using_target_word == None:
            print('There are no presidents who said "Nation".')
        else:
            print('The presidents who said the word "Nation" are: ')
            print(presidents_using_target_word)
            print("And the ones who said it the most are: ")
            print(presidents_using_the_most_target_word)
    elif user_choice == 5:
        first_to_use_climat = first_to_use(groups_of_files, "climat")
        first_to_use_ecologie = first_to_use(groups_of_files, "écologie")
        if first_to_use_climat == None and first_to_use_ecologie == None:
            print("None of them used one of those words.")
        elif first_to_use_climat == None:
            print('The first president who said "climat" or "écolgie" was: ')
            print(first_to_use_ecologie)
            print('By saying "écologie".')
        elif first_to_use_ecologie == None:
            print('The first president who said "climat" or "écolgie" was: ')
            print(first_to_use_climat)
            print('By saying "climat".')
        elif first_to_use_climat < first_to_use_ecologie in presidents_names:
            print('The first president who said "climat" or "écolgie" was: ')
            print(first_to_use_climat)
            print('By saying "climat".')
        elif first_to_use_ecologie < first_to_use_climat in presidents_names:
            print('The first president who said "climat" or "écolgie" was: ')
            print(first_to_use_ecologie)
            print('By saying "écologie".')
        else:
            print('The first president who said "climat" or "écolgie" was: ')
            print(first_to_use_climat)
            print('By saying both.')
    elif user_choice == 6:
        words_used_by_all_but_not_all_speeches = not_unimportant_words_used_by_all_groups(tf_idf, groups_of_files)
        if words_used_by_all_but_not_all_speeches == None:
            print("There are no words that all the presidents have pronounced but that did not appears in all of their speeches.")
        else:
            print("The words that all presidents have pronounced but that did not appears in all of their speeches are: ")
            print(words_used_by_all_but_not_all_speeches)

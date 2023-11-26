from function import *

if __name__ == '__main__':
    #we could rearrange the order of the calls of the functions here to make it more clean
    directory = "./speeches"
    files_names = list_of_files(directory, "txt")
    dates_presidents = {"Giscard dEstaing": (1974, 1981), "Mitterrand": (1981, 1995), "Chirac": (1995, 2007), "Sarkozy": (2007, 2012), "Hollande": (2012, 2017), "Macron": (2017, 2022)}
    presidents_names = authors_names_by_dates(files_names, dates_presidents)
    #if the code has already been executed no need to execute it again
    if not os.path.exists("cleaned"):
        clean_directory = create_cleaned_files(directory)
    else:
        clean_directory = "./cleaned"
    files_names = list_of_files(clean_directory, "txt")
    tf_idf = tf_idf_of_directory(clean_directory)
    groups_of_files = groups_of_files_by_name(files_names, presidents_names)
    print("To see the unimportant words in the document corpus, enter 1")
    print("To see the words with the highest TF-IDF score, enter 2")
    print("To see the most repeated words by a certain president, enter 3")
    print("To see the presidents who said the a certain word and the ones who said it the most, enter 4")
    print('To see the first president who said a certain word or another certain word, enter 5')
    print("To see the words that all the presidents have pronounced but that did not appears in all of their speeches, enter 6")
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
        print(presidents_names)
        president = input("Enter the name of the president: ")
        most_repeated_words_president = most_repeated_words_in_group_of_files(groups_of_files, president)
        if most_repeated_words_president == None:
            print(f"President {president} did not say anything.")
        else:
            print(f"The most repeated words by president {president} are: ")
            print(most_repeated_words_president)
    elif user_choice == 4:
        target_word = input("Enter the word: ")
        presidents_using_target_word, presidents_using_the_most_target_word = groups_of_files_using_word(groups_of_files, target_word)
        if presidents_using_target_word == None:
            print(f'There are no presidents who said "{target_word}".')
        else:
            print(f'The presidents who said the word "{target_word}" are: ')
            print(presidents_using_target_word)
            print("And the ones who said it the most are: ")
            print(presidents_using_the_most_target_word)
    elif user_choice == 5:
        word1 = input("Enter the first word: ")
        first_to_use_word1 = first_to_use(groups_of_files, word1)
        word2 = input("Enter the second word: ")
        first_to_use_word2 = first_to_use(groups_of_files, word2)
        if first_to_use_word1 == None and first_to_use_word2 == None:
            print("None of them used one of those words.")
        elif first_to_use_word1 == None:
            print(f'The first president who said "{word1}" or "{word2}" was: ')
            print(first_to_use_word2)
            print(f'By saying "{word2}".')
        elif first_to_use_word2 == None:
            print(f'The first president who said "{word1}" or "{word2}" was: ')
            print(first_to_use_word1)
            print(f'By saying "{word1}".')
        elif first_to_use_word1 < first_to_use_word2 in presidents_names:
            print(f'The first president who said "{word1}" or "{word2}" was: ')
            print(first_to_use_word1)
            print(f'By saying "{word1}".')
        elif first_to_use_word2 < first_to_use_word1 in presidents_names:
            print(f'The first president who said "{word1}" or "{word2}" was: ')
            print(first_to_use_word2)
            print(f'By saying "{word2}".')
        else:
            print(f'The first president who said "{word1}" or "{word2}" was: ')
            print(first_to_use_word1)
            print("By saying both.")
    elif user_choice == 6:
        words_used_by_all_but_not_all_speeches = not_unimportant_words_used_by_all_groups(tf_idf, groups_of_files)
        if words_used_by_all_but_not_all_speeches == None:
            print("There are no words that all the presidents have pronounced but that did not appears in all of their speeches.")
        else:
            print("The words that all presidents have pronounced but that did not appears in all of their speeches are: ")
            print(words_used_by_all_but_not_all_speeches)

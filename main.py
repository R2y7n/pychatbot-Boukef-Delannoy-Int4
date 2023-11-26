from function import *

if __name__ == '__main__':
    """we could rearrange the order of the calls of the functions here to make it more clean"""
    directory = "./speeches"
    files_names = list_of_files(directory, "txt")
    print(files_names)
    presidents_names = authors_names(files_names)
    dates_presidents = {"Giscard dEstaing": (1974, 1981), "Mitterrand": (1981, 1995), "Chirac": (1995, 2007), "Sarkozy": (2007, 2012), "Hollande": (2012, 2017), "Macron": (2017, 2022)}
    presidents_names = authors_names_by_dates(presidents_names, dates_presidents)
    print(presidents_names)
    """if the code has already been executed no need to execute it again"""
    if not os.path.exists("cleaned"):
        clean_directory = create_cleaned_files(directory)
    else:
        clean_directory = "./cleaned"
    files_names = list_of_files(clean_directory, "txt")
    print(files_names)
    tf_idf = tf_idf_of_directory(clean_directory)
    print(tf_idf)
    groups_of_files = groups_of_files_by_name(clean_directory, presidents_names)
    print(unimportant_words_in_files(tf_idf, "directory"))
    print(highest_tf_idf(tf_idf))
    print(most_repeated_words_in_group_of_files(groups_of_files, "Chirac"))
    presidents_using_target_word, presidents_using_the_most_target_word = groups_of_files_using_word(groups_of_files, presidents_names, "nation")
    print(presidents_using_target_word, presidents_using_the_most_target_word)
    print(first_to_use(groups_of_files, presidents_names, "climat"))
    print(first_to_use(groups_of_files, presidents_names, "écologie"))
    print(not_unimportant_words_used_by_all_groups(tf_idf, groups_of_files))

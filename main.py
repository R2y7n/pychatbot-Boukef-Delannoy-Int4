from function import *

if __name__ == '__main__':
    directory = "./speeches"
    files_names = list_of_files(directory, "txt")
    print(files_names)
    president_names = president_name(files_names)
    print(president_names)
    """if the code has already been executed no need to execute it again"""
    if not os.path.exists("cleaned"):
        clean_directory = create_cleaned_files(directory)
    else:
        clean_directory = "./cleaned"
    tf_idf = tf_idf_of_directory(clean_directory)
    print(tf_idf)
    print(tf_idf_0(tf_idf))
    print(highest_tf_idf(tf_idf))
    groups_of_files = groups_of_files_by_name(clean_directory, president_names)
    print(most_repeated_words_in_group_of_files(groups_of_files, "Chirac"))
    print(groups_of_files_using_word(groups_of_files, president_names, "nation"))

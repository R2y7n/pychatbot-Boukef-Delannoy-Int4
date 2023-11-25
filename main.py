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

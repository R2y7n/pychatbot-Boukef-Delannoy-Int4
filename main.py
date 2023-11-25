import os.path

from function import *

if '__main__' == __name__:
    files_names = list_of_files(".txt", "speeches-20231116")
    print(files_names)
    president_names = []
    for file_name in files_names:
        charcacter = 0
        while file_name[charcacter] != "_":
            charcacter = charcacter + 1
        charcacter = charcacter + 1
        name = ""
        chiffres = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        while file_name[charcacter] not in chiffres:
            name = name + file_name[charcacter]
            charcacter = charcacter + 1
            print(name)
        president_names.append(name)
    print(president_names)

original_text = "Salut comme çcava @!:;,@@{]@@^#"
clean_text = tkoff_ponctuation(original_text)

print(clean_text)

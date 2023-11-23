from function import*

if __name__ == '__main__':
    files_names = list_of_files(".txt", "speeches-20231116")
    print(files_names)
    president_names = []
    for file_name in files_names:
        charcacter = 0
        while file_name[charcacter] != "_":
            charcacter = charcacter + 1
        charcacter = charcacter + 1
        name = ""
        chiffres = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
        while file_name[charcacter] not in chiffres:
            name = name + file_name[charcacter]
            charcacter = charcacter + 1
            print(name)
        president_names.append(name)
    print(president_names)

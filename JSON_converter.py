import json
from matplotlib.pyplot import savefig

from numpy import save

def __main__():

    traduction_dict = open_json_tag()

    nombre_articles = 60

    final_list = []
    # for file_num in range(nombre_articles):
    with open('./annotations/article_number_0.json', 'r', encoding="utf8") as json_file:
        data = json.load(json_file)
        whole_text = data['rawString']
        whole_text_modified = ""
        char_added = []
        saved_char = ""
        for i in range(len(whole_text)):
            char = whole_text[i]

            if i == (len(whole_text) - 1):
                if char in [",","-","\'",".","/",":","&","’"]:
                    whole_text_modified += " " + saved_char + char
                    char_added.append((i, 1))
                elif saved_char != "":
                    whole_text_modified += " " + saved_char + " " + char
                    char_added.append((i,2))
                else:
                    whole_text_modified += char

            elif char in [",","-","\'",".","/",":","&","’"]:
                if saved_char == "":
                    saved_char = char
                else:
                    saved_char += char
            
            elif char in ["\"","“","”"]:
                if saved_char != "" and saved_char[-1] == ",": #Cas où les guillemets doivent être considérés comme des caractères spéciaux
                    saved_char += char
                else:  #Cas où les guillemets doivent etre considérés comme des mots
                    if saved_char != "":
                        if (whole_text[i - len(saved_char) - 1] != " " and whole_text[i + 1] != " "): #Ex : bla-"bla => bla - " bla
                            whole_text_modified += " " + saved_char + " " + char + " "
                            char_added.append((i - len(saved_char), 2))
                            char_added.append((i, 1))
                            saved_char = ""
                        else: #Ex : bla -"bla => bla - " bla
                            whole_text_modified += " " + saved_char + " " + char + " "
                            char_added.append((i - len(saved_char),1))
                            char_added.append((i,1))
                            saved_char = ""
                    else:
                        whole_text_modified += " " + char + " "
                        if whole_text[i -1] != " " and whole_text[i + 1] != " ":
                            char_added.append((i,2))
                        elif not (whole_text[i - 1] == " " and whole_text[i + 1] == " "):
                            char_added.append((i,1))
            
            else:
                if saved_char != "":
                    if (whole_text[i - len(saved_char) - 1] != " " and char != " "):
                        whole_text_modified += " " + saved_char + " " + char
                        char_added.append((i - len(saved_char),2))
                        saved_char = ""
                    elif not (whole_text[i - len(saved_char) - 1] == " " and char == " "):
                        whole_text_modified += " " + saved_char + " " + char
                        char_added.append((i - len(saved_char),1))
                        saved_char = ""
                    else:
                        whole_text_modified += saved_char + char
                        saved_char = ""
                else:
                    whole_text_modified += char

        whole_text_list = whole_text_modified.split()

        word_list = data['annotations'][-1]['value']['tags']
        annotated_list = []

        for tag in word_list:
            annotation = []
            for word_id in range(tag['begin'], tag['end'] + 1):
                word = data['tokenized'][word_id]['word']
                annotation.append(word)

            index = tag['begin']
            extrait = [whole_text_list[i] for i in range(index, index + len(annotation))]

            fst_char_index = count_char(whole_text_list, index)

            lst_char_index = fst_char_index + count_char(annotation, len(annotation)) - 1

            fst_char_add = nb_add_char(char_added, fst_char_index)
            fst_char_index -= fst_char_add
            lst_char_add = nb_add_char(char_added, lst_char_index)
            lst_char_index -= lst_char_add

            print((extrait,[whole_text[fst_char_index:lst_char_index]]))
            
            annotated_list.append((fst_char_index, lst_char_index, traduction_dict[tag['tag']]))

    return annotated_list



def open_json_tag():
    traduction_dict = {}
    with open('./data-model.json') as json_file:
        data = json.load(json_file)
        for tag in data['tags']:
            traduction_dict[tag['id']] = tag['shortcut']
    return traduction_dict

def count_char(list_word, index):
    c = 0
    for i in range(index):
        c += len(list_word[i]) + 1
    return c

def nb_add_char(added, index):
    c = 0
    for i in added:
        if i[0] <= index:
            c += i[1]
        else:
            break
    return c

__main__()
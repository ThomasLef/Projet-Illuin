import json

def __main__():

    traduction_dict = open_json_tag()

    nombre_articles = 60

    final_list = []
    # for file_num in range(nombre_articles):
    with open('./annotations/article_number_0.json', 'r') as json_file:
        data = json.load(json_file)
        whole_text = data['rawString']
        whole_text_modified = ""
        char_added = []
        for i in range(len(whole_text)):
            char = whole_text[i]
            if char in [",","-","\'",".","\n"]:
                if i == (len(whole_text) - 1):
                    whole_text_modified += " " + char
                    char_added.append((i,1))
                elif (whole_text[i - 1] != " " and whole_text[i + 1] != " "):
                    whole_text_modified += " " + char + " "
                    char_added.append((i,2))
                elif not (whole_text[i - 1] == " " and whole_text[i + 1] == " "):
                    whole_text_modified += " " + char + " "
                    char_added.append((i,1))
                else:
                    whole_text_modified += char
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

            list_position = range(int(0.9*tag['begin']), int(min(1.1*tag['end'] +1, len(whole_text_list)))) #Position possible of the first word, between tag[begin] +- 10%
            for index in list_position:
                extrait = [whole_text_list[i] for i in range(index, index + len(annotation))]
                if (extrait == annotation):

                    fst_char_index = count_char(whole_text_list, index)

                    lst_char_index = fst_char_index + count_char(annotation, len(annotation)) - 1

                    fst_char_add = nb_add_char(char_added, fst_char_index)
                    fst_char_index -= fst_char_add
                    lst_char_add = nb_add_char(char_added, lst_char_index)
                    lst_char_index -= lst_char_add

                    print((extrait,[whole_text[fst_char_index:lst_char_index]]))
                    break
            
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
        if i[0] < index:
            c += i[1]
        else:
            break
    return c

print(__main__())
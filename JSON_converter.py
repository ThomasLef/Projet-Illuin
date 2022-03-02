import json

def extraction_json():

    traduction_dict = open_json_tag()

    nombre_articles = 60

    final_list = []
    for file_num in range(nombre_articles):
        with open('./annotations/article_number_' + str(file_num) + '.json', 'r', encoding="utf8") as json_file:
            data = json.load(json_file)
            whole_text = data['rawString']
            word_list = data['annotations'][-1]['value']['tags']
            annotated_list = []

            for tag in word_list:
                annotated_list.append([data['tokenized'][tag['begin']]['cumulatedX'], data['tokenized'][tag['end'] +1]['cumulatedX'], traduction_dict[tag['tag']]])

        final_list.append((whole_text,{"entities": annotated_list}))
    
    return(final_list)



def open_json_tag():
    traduction_dict = {}
    with open('./data-model.json') as json_file:
        data = json.load(json_file)
        for tag in data['tags']:
            traduction_dict[tag['id']] = tag['shortcut']
    return traduction_dict

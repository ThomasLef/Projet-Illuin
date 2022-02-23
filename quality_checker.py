import spacy
import datetime
import dateparser

nlp = spacy.load('en_core_web_sm')

def date_checker(obj_date, article, precision): #Please indicate the desired date for the article, and the precision (in days)
    listdates = []
    for para in article:
        doc = nlp(para)
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                print(ent.text)
                listdates.append(ent.text)
    
    for date in listdates:
        good_date = dateparser.parse(date)
        print(good_date)
        if abs(good_date - obj_date).days < precision:
            return True
    return False

article = ["Hey, this is a great article about wILDfires and forest fires written on the 12/01/2022. It does not talk about movies."]
keywords_list = ["wildfire", "wildfires", "forest", "fire", "fires", "burn"]

# print(date_checker(obj_date, article, 15))

def relevance_checker(article, keywords, precision_key, precision_words):
    nb_words = 0
    nb_key = 0
    list_punctuation = [",",".","\'",";",":","!","?"]
    for para in article:
        nb_words+=len(para.split())
        for point in list_punctuation:
            para.replace(point, "")
        for word in para.split():
            if word.lower() in keywords:
                print(word)
                nb_key+=1

    if nb_words < precision_words:
        return False
    elif nb_key < precision_key:
        return False
    return True

def source_checker(list_sources, precision_source):
    if len(list_sources) < precision_source:
        return False
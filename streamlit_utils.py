from __future__ import unicode_literals, print_function
from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

import spacy
import re
from spacy import displacy 
from spacy.matcher import Matcher 
import visualise_spacy_tree
from IPython.display import Image, display


from spacy.lang.en import English # updated

import geopy 
import matplotlib.pyplot as plt
from geopy.extra.rate_limiter import RateLimiter

import folium
from folium.plugins import FastMarkerCluster
from folium.plugins import HeatMap

import numpy as np

from deep_translator import GoogleTranslator
from datetime import datetime, timedelta
import parsedatetime as pdt

import plotly.express as px

from transformers import BertForSequenceClassification, LongformerTokenizer, LongformerForSequenceClassification
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

from torch import nn
import torch

NLP_SENTENCES = English()
NLP_SENTENCES.add_pipe('sentencizer') 

#Model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


def classify_relevance(article, model, tokenizer):
    #Article is a string, containing the text of the article
    #Model is the Neural Network Classifier, a longformer in our case
    #Tokenizer is the tokenizer that converts the article into a valid input for the model
    token_article = tokenizer(article, padding='max_length', max_length = 512, truncation=True, return_tensors="pt")
    mask = token_article['attention_mask']
    input_id = token_article['input_ids']
    output = model(input_id, mask).logits.argmax(dim=1).item()
    return output

#Scraping Google news with Selenium and Beautifulsoup
def get_lists_from_subject(subject, num_pages,date_limits = None):

    restart = True
    problem = False

    problem_count = 0

    max_problem_count = 10

    while restart and problem_count < max_problem_count:

        translator = GoogleTranslator(source='fr', target='en')
        
        cal = pdt.Calendar()
        now = datetime.now()

        PATH = "./chromedriver_win32/chromedriver.exe"

        s=Service(PATH)
        driver = webdriver.Chrome(service=s)

        link_list = []
        date_list = []
        if date_limits is not None:
            lower_date, higher_date = date_limits
            ld, lm, ly = str(lower_date.day), str(lower_date.month), str(lower_date.year)
            hd, hm, hy = str(higher_date.day), str(higher_date.month), str(higher_date.year)
            driver.get("https://www.google.com/search?q="+subject+"&rlz=1C1CHBF_frFR863FR863&biw=1920&bih=880&sxsrf=APq-WBuYthkpiHNrhk_0YwH1w70zP27Xgg%3A1643812260630&source=lnt&tbs=cdr%3A1%2Ccd_min%3A"+lm+"%2F"+ld+"%2F"+ly+"%2Ccd_max%3A"+hm+"%2F"+hd+"%2F"+hy+"&tbm=nws&hl=en")
        else:   
            driver.get("https://www.google.com/search?q="+subject+"&rlz=1C1CHBF_frFR863FR863&biw=1920&bih=880&sxsrf=AOaemvI0XcPZB9YWw9GUVGwWTEXPDVqRxQ:1638967714934&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjGlsnDntT0AhWTTcAKHeyuDk4Q_AUoAXoECAEQAw&hl=en")

        driver.find_element(By.XPATH, "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qfvgSe']").click() #accept google policy

        for i in range(num_pages):
            if i != 0:
                try :
                    driver.find_element(By.ID, "pnnext").click()
                except :
                    break

            html_source = driver.page_source

            soup = BeautifulSoup(html_source, 'lxml')

            #Getting all g-card 
            g_card_list = soup.find_all("g-card")

            if g_card_list == []:
                driver.quit()
                problem = True
                problem_count += 1
                break
            else :
                problem = False

            for g_card in g_card_list:
                a = g_card.find("a")
                link = a['href']
                link_list.append(link)

                date = g_card.find_all("span")[-1].text
                translated_date = translator.translate(date)
                date_list.append(cal.parseDT(translated_date, now)[0].date())


        if problem :
            restart = True
        else:
            driver.quit()
            restart = False
    if not problem:
        print("Successfully scraped : ", len(link_list), " links")

    else:
        print("Problem occured during scraping")

    return link_list, date_list






#Now that we have the link list, for each link try to scrape the article if there is one and the date if there is one.
def get_df_from_link_list(link_list, date_list):

    my_timeout = 10

    data = []

    for i, link in enumerate(link_list):
        d = {}

        try:
            html_text = requests.get(link, timeout=my_timeout).text

            soup = BeautifulSoup(html_text, 'lxml')

            title = soup.find('title')
            if title != None:
                d["Title"] = title.text

            d["Link"] = link
   


            d["Date"] = date_list[i]
            
            article = soup.find('article')
            if article != None:
                paragraphs = article.find_all('p')
                big_p = ""
                for p in paragraphs:
                    big_p = big_p + p.text + " "
                
                if big_p != "":
                    d["Content"] = unicodedata.normalize("NFKD", big_p).rstrip()
        except: #Requests takes way too long or bug
            print('Could not scrap page number ' + str(i) + ', try again another time.')

        data.append(d)

    return pd.DataFrame(data)


def get_df_from_subject(subject,num_pages, date_limits = None):
    link_list, date_list = get_lists_from_subject(subject, num_pages, date_limits)
    return get_df_from_link_list(link_list, date_list)

def get_rid_of_date(df):
    res = df.drop(columns = ["Date"])
    return res

def clean(text):
    
    """Clean the text input"""
    
    # removing paragraph numbers
    text = re.sub('[0-9]+.\t','',str(text))
    # removing new line characters
    text = re.sub('\n ','',str(text))
    text = re.sub('\n',' ',str(text))
    # removing apostrophes
    text = re.sub("'s",'',str(text))
    # removing hyphens
    text = re.sub("-",' ',str(text))
    text = re.sub("??? ",'',str(text))
    # removing quotation marks
    text = re.sub('\"','',str(text))
    # removing salutations
    text = re.sub("Mr\.",'Mr',str(text))
    text = re.sub("Mrs\.",'Mrs',str(text))
    # removing any reference to outside text
    text = re.sub("[\(\[].*?[\)\]]", "", str(text))

    return text
    
def get_df_relevant(df, model, tokenizer):
    df["Relevance"] = df["Content"].apply(lambda x: classify_relevance(x, model, tokenizer))
    df = df[df["Relevance"] == 1]
    df = df.drop(columns = ["Relevance"]).reset_index(drop=True)
    return df

def sentences(text):
    # split sentences and questions
    global NLP_SENTENCES
    raw_text = text
    doc = NLP_SENTENCES(raw_text)
    return [sent.text.strip() for sent in doc.sents]


def add_location_col_in_df(df):
    nlp = spacy.load('en_core_web_sm') #Loading english NLP model
    locations = {"Location":[]}
    for sentence_list in df["Sentences"]:
        list_of_location = []
        for sentence in sentence_list:
            doc = nlp(sentence)
            for ent in doc.ents:
                if ent.label_ == 'GPE':
                    if ent.text not in list_of_location:
                        list_of_location.append(ent.text)
        locations["Location"].append(list_of_location)

    df['Location'] = pd.DataFrame(locations)

    return df


def get_locations_df_from_subject(subject, num_pages, model, tokenizer, date_limits = None):
    df = get_df_from_subject(subject,num_pages, date_limits) #DF from scraping
    print("Done scraping")
    #df = get_rid_of_date(df) #No date
    df = df.dropna() #Drop missing values
    df = df.reset_index(drop=True)
    print(f'There are {len(df.index)} usable articles')
    df = get_df_relevant(df, model, tokenizer) #Add relevance
    print(f'There are {len(df.index)} relevant articles')
    if "Content" in df.columns:
        df["Content"] = df["Content"].apply(clean) #cleaning contents
        df = df.rename(columns={"Content":"Clean_content"})
        df["Sentences"] = df["Clean_content"].apply(sentences) #getting sentences list
        df = add_location_col_in_df(df) #adding locations
    return df


def get_location_map_from_df(df, map_style = None):
    locations = np.concatenate(df["Location"])

    print(f"There are {len(locations)} locations")

    d = {}

    locator = geopy.geocoders.Nominatim(user_agent='mygeocoder')
    geocode = RateLimiter(locator.geocode,min_delay_seconds=0.5)
    lattitudes = []
    longitudes = []
    for loc in locations :
        try :
            if loc not in d.keys():
                code = geocode(loc)
                lattitudes.append(code[1][0])
                longitudes.append(code[1][1])
                d[loc] = (code[1][0],code[1][1])
            else:
                coord = d[loc]
                lattitudes.append(coord[0])
                longitudes.append(coord[1])
        except :
            pass

    if map_style == "heatmap":
        map = folium.Map([48, 5], tiles='CartoDB dark_matter', zoom_start=2)
        HeatMap(data=list(zip(lattitudes, longitudes))).add_to(map)
        return map

    else:

        folium_map = folium.Map(location=[59.338315,18.089960],
                                zoom_start=2,
                                tiles='CartoDB dark_matter')
        FastMarkerCluster(data=list(zip(lattitudes, longitudes))).add_to(folium_map)
        folium.LayerControl().add_to(folium_map)
        return folium_map


def plot_articles_per_date(df_location):
    s = df_location['Date'].value_counts().sort_index()
    dates, count = list(s.index), list(s)
    min_date = min(dates)
    max_date = max(dates)
    dateList = []
    for x in range (0, (max_date-min_date).days + 1):
        dateList.append(min_date + timedelta(days = x))
    countList = [0 for i in range(len(dateList))]
    for i in range(len(dateList)):
        if dateList[i] in dates:
            countList[i] = count[dates.index(dateList[i])]
    df_temp = pd.DataFrame({"Date" : dateList, "Count": countList})
    return px.line(df_temp, x= "Date", y = "Count", title = "Number of scraped articles per date")
    
def tokenize_input_text(question, input_text):

    input_ids = tokenizer.encode(question, input_text)

    return input_ids

def tokenize_input_text(question, input_text):

    input_ids = tokenizer.encode(question, input_text)

    return input_ids

def get_segment_ids(input_ids):
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    return segment_ids

def get_scores(input_ids,segment_ids):
    # Run through the model.
    start_scores, end_scores = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                    token_type_ids=torch.tensor([segment_ids]),
                                    return_dict = False) # The segment IDs to differentiate question from answer_text
    return start_scores, end_scores

# Find the tokens with the highest `start` and `end` scores.
def get_answer(start_scores,end_scores, input_ids):
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Combine the tokens in the answer and print it out.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer = ' '.join(tokens[answer_start:answer_end+1])

    return answer

# Better version

def get_answer_clean(start_scores, end_scores, input_ids):
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        
        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]
    return answer

def answer_from_question(question, input_text):
    input_ids = tokenize_input_text(question, input_text)
    segment_ids = get_segment_ids(input_ids)
    start_scores, end_scores = get_scores(input_ids, segment_ids)

    res = get_answer_clean(start_scores, end_scores, input_ids)

    if '[CLS]' in res:
        return "No answer found"    
    return res

def get_first_senteces_from_sentences_list(sentences_list, nb_sentences):
    return "".join(sentences_list[0:nb_sentences])

def add_QA_location_to_df(df_location, subject, nb_sentences=5):
    question = "Where did the " + subject + " occur?"
    df_location["QA_location"] = None
    df_location["QA_location"] = df_location["Sentences"].apply(lambda x : answer_from_question(question, get_first_senteces_from_sentences_list(x,nb_sentences)))
    return df_location

def add_QA_impact_to_df(df_location, subject, nb_sentences=5):
    question = "What were the impact of the " + subject + " ?"
    df_location["QA_impact"] = None
    df_location["QA_impact"] = df_location["Sentences"].apply(lambda x : answer_from_question(question, get_first_senteces_from_sentences_list(x,nb_sentences)))
    return df_location

def add_QA_cause_to_df(df_location, subject, nb_sentences=5):
    question = "What caused the " + subject + " ?"
    df_location["QA_cause"] = None
    df_location["QA_cause"] = df_location["Sentences"].apply(lambda x : answer_from_question(question, get_first_senteces_from_sentences_list(x,nb_sentences)))
    return df_location
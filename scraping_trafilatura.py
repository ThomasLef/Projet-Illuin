import trafilatura
from trafilatura import feeds
import matplotlib.pyplot as plt

# print(absice)
# print(ordo1)
# print(ordo2)

def is_number(char):
    return char in ["0","1","2","3","4","5","6","7","8","9"]

def is_barre_verti(char):
    return char == "|"

def is_comma(char):
    return char == ","

def is_asterix(char):
    return char == "*" or char == "\n"


def main():
    downloaded = trafilatura.fetch_url("https://www.nifc.gov/fire-information/statistics/wildfires")
    absice = []
    ordo1 = []
    ordo2 = []

    liste1 = absice
    liste2 = ordo1
    liste3 = ordo2

    document = trafilatura.extract(downloaded)
    bar_vue = False
    double_bar = False
    nombre = ""
    for char in document:
        if is_barre_verti(char):
            if len(nombre) > 0:
                liste1.append(int(nombre))
                nombre = ""
                oldlist1 = liste1.copy()
                liste1 = liste2
                liste2 = liste3
                liste3 = oldlist1
                bar_vue=True
                double_bar = False
            elif bar_vue:
                double_bar = True
            else:
                bar_vue = True
                double_bar = False

        elif is_number(char) and double_bar:
            bar_vue = False
            nombre += char
        
        elif is_comma(char) and len(nombre) > 0:
            pass
        
        elif is_asterix(char):
            pass
        
        else:
            bar_vue = False
            double_bar = False
            nombre = ""

    plt.plot(liste1, liste2)
    plt.show()
    plt.plot(liste1, liste3)
    plt.show()

def get_links(link):
    feedlist = feeds.find_feed_urls(link)
    print(feedlist)
    return(feedlist)

get_links('https://www.nbcnews.com/western-wildfires')
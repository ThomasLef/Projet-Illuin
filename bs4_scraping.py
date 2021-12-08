from bs4 import BeautifulSoup
import requests
import pandas as pd

#soup.find() ne trouve que le premier tag dans l'html, pour tous les avoir, il faut utiliser soup.find_all()
#En utilisant les méthodes find et find all on peut spécifier le type de balise que l'on cherche ainsi que leur classe html

MY_LINKS = [
"https://www.nifc.gov/fire-information/nfn",
"https://www.nbcnews.com/western-wildfires",
"https://wildfiretoday.com/",
"https://www.hcn.org/issues/53.11/south-wildfire-hmong-americans-in-northern-california-fight-wildfire-and-distrust",
"https://www.reddit.com/r/wildfires/",
"https://en.wikipedia.org/wiki/Wildfires_in_2020",
]

#requests.get renvoie la réponse de la page, pour avoir le contenu, il faut utiliser text, ainsi on peut en faire une soup
html_text = requests.get(MY_LINKS[0]).text

soup = BeautifulSoup(html_text, 'lxml')

#getting div with "main" id
html_main_div = soup.find('div', {"id" : "main"})

main_p_list = html_main_div.find_all('p')


table = html_main_div.find_all('table')
df = pd.read_html(str(table))[0]

print(df.head)



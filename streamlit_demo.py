import streamlit as st
import streamlit.components.v1 as components
import re

from streamlit_utils import *
from streamlit_pytrends import *

if "display" not in st.session_state:
    st.session_state.display = False

if "good_date" not in st.session_state:
    st.session_state.good_date = False

if "df_location" not in st.session_state:
    st.session_state.df_location = None

if "fig" not in st.session_state:
    st.session_state.fig = None

if "html_map" not in st.session_state:
    st.session_state.html_map = None

if "show_plot_articles_per_date" not in st.session_state:
    st.session_state.show_plot_articles_per_date = False

if "show_map" not in st.session_state:
    st.session_state.show_map = False

if "display_trends" not in st.session_state:
    st.session_state.display_trends = False

if "pytrends" not in st.session_state:
    st.session_state.pytrends = None

if "trend" not in st.session_state:
    st.session_state.trend = None

if "fft" not in st.session_state:
    st.session_state.fft = None

if "nb_ppy" not in st.session_state:
    st.session_state.nb_ppy = None

if "peak_m" not in st.session_state:
    st.session_state.peak_m = None

if "tokenizer" not in st.session_state:
    st.session_state.tokenizer = None

if "model" not in st.session_state:
    st.session_state.model = None

st.sidebar.title("Climate change scraping dashboard")

st.sidebar.image("https://www.pressonline.com/illuin-technology/files/2019/08/xlogo-illuin-technology.png.pagespeed.ic.P4glNQKPUa.png")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/fr/thumb/8/86/Logo_CentraleSup%C3%A9lec.svg/1200px-Logo_CentraleSup%C3%A9lec.svg.png")




def show_results():
    try :
        update_df()
        if st.session_state.good_date:
            st.session_state.display = True

        if st.session_state.show_plot_articles_per_date:
            st.session_state.fig = plot_articles_per_date(st.session_state.df_location)
        if st.session_state.show_map:
            st.session_state.html_map = get_map_as_html(st.session_state.df_location)
    except :
        pass

def show_trends():
    st.session_state.display_trends = True
    try :
        update_trends()
    except:
        pass
    st.session_state.trend = trend_fig(st.session_state.pytrends, topic)
    st.session_state.fft = fft_fig(*freq_pos(st.session_state.pytrends, topic, nb_years))
    st.session_state.nb_ppy = nb_peaks_per_year(*freq_pos(st.session_state.pytrends, topic, nb_years))
    st.session_state.peak_m = peak_month(st.session_state.pytrends, topic)


def update_trends():
    st.session_state.pytrends = init_pytrends(topic, nb_years)

def get_map_as_html(df_location):
    folium_map = get_location_map_from_df(df_location, map_style="heatmap")
    folium_map.save("html_maps/heatmap.html")
    HtmlFile = open("html_maps/heatmap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    return source_code

def update_df():
    st.session_state.df_location = get_locations_df_from_subject(subject, num_pages, st.session_state.model, st.session_state.tokenizer, (start_date,end_date))
    st.write("done")

def load_model_tokenizer():
    st.session_state.tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")
    st.session_state.model = torch.load('model/longformer_finetuned').to('cpu')

if st.session_state.tokenizer is None or st.session_state.model is None:
    load_model_tokenizer()

SEARCH_TYPE = ["Scraping Google News", "Times series Pytrend"]

search_type = st.selectbox("Type de recherche", SEARCH_TYPE)

if search_type == SEARCH_TYPE[0]: #Scraping

    with st.form("Paramètre de scraping"):
        
        subject = st.text_input("Mot clé de la recherche : ")

        c1,c2 = st.columns(2)

        start_date = c1.date_input('Début')
        end_date = c2.date_input('Fin')

        deb = re.sub(r'\-', r'/', str(start_date))
        fin = re.sub(r'\-', r'/', str(end_date))


        if start_date <= end_date:
            st.success('Début : `%s`\n\n Fin : `%s`' % (deb, fin))
            st.session_state.good_date = True
        else:
            st.error('Erreur : la date de fin doit être supérieure à la date de début. Veuillez entrer de nouvelles dates et appliquer les modifications.')
            st.session_state.good_date = False

        num_pages = int(st.number_input("Nombres de pages à scrap :", step = 1,min_value = 1))

        st.session_state.show_plot_articles_per_date = st.checkbox("Afficher le nombre d'articles par date", value = True)

        st.session_state.show_map = st.checkbox("Afficher la carte de chaleur correspondante", value = True)
        


        if st.form_submit_button("Appliquer les modifications"):
            st.write("Changements pris en compte.")

    st.button("Lancer le scraping", on_click = show_results)

    

    if st.session_state.display:
        
        
        st.session_state.df_location

        if st.session_state.show_plot_articles_per_date:
            
            st.plotly_chart(st.session_state.fig, use_container_width=True)

        if st.session_state.show_map:
            
            components.html(st.session_state.html_map, height = 800, width = 1200)
    
if search_type == SEARCH_TYPE[1] : #Pytrend

    with st.form("Paramètre de scraping"):
        
        topic = st.text_input("Mot clé de la recherche : ")

        nb_years = int(st.number_input("Nombres d'années à analyser :", step = 1,min_value = 1))

        if st.form_submit_button("Appliquer les modifications"):
            st.write("Changements pris en compte.")
        
    st.button("Lancer l'analyse des trends", on_click = show_trends)

    if st.session_state.display_trends and st.session_state.pytrends is not None:


        st.plotly_chart(st.session_state.trend, use_container_width=True)


        st.plotly_chart(st.session_state.fft, use_container_width=True)

        st.write(f"nb_peaks_per_year = {st.session_state.nb_ppy}")

        st.write(f"peak_month = {st.session_state.peak_m}")
    
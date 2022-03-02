import streamlit as st
import streamlit.components.v1 as components
import re

from streamlit_utils import *

if "display" not in st.session_state:
    st.session_state.display = False

if "good_date" not in st.session_state:
    st.session_state.good_date = False

st.sidebar.title("Climate change scraping dashboard")

st.sidebar.image("https://www.pressonline.com/illuin-technology/files/2019/08/xlogo-illuin-technology.png.pagespeed.ic.P4glNQKPUa.png")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/fr/thumb/8/86/Logo_CentraleSup%C3%A9lec.svg/1200px-Logo_CentraleSup%C3%A9lec.svg.png")




def show_results():
    if st.session_state.good_date:
        st.session_state.display = True

def get_map_as_html(df_location):
    # folium_map = get_location_map_from_df(df_location, map_style="heatmap")
    # folium_map.save("html_maps/heatmap.html")
    HtmlFile = open("html_maps/heatmap.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    return source_code



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

    show_plot_articles_per_date = st.checkbox("Afficher le nombre d'articles par date")

    show_map = st.checkbox("Afficher la carte de chaleur correspondante")
    


    if st.form_submit_button("Appliquer les modifications"):
        st.write("Changements pris en compte.")

st.button("Lancer le scraping", on_click = show_results)


if st.session_state.display:
    date_limits = (start_date,end_date)
    df_location = get_locations_df_from_subject(subject, num_pages, date_limits)
    
    df_location

    if show_plot_articles_per_date:
        fig = plot_articles_per_date(df_location)
        st.plotly_chart(fig, use_container_width=True)

    if show_map:
        html_map = get_map_as_html(df_location)
        components.html(html_map, height = 4, width = 1200)
        
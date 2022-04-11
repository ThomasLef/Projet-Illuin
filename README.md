# DeepCV-project
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![Open in Visual Studio Code](https://img.shields.io/badge/Editor-VSCode-blue?style=flat-square&logo=visual-studio-code&logoColor=white)](https://github.dev/ThomasLef/Projet-Illuin) 

Projet de dominante Infonum CentraleSupélec en collaboration avec Illuin Technology.

<p align="center"> <img src="https://upload.wikimedia.org/wikipedia/fr/thumb/8/86/Logo_CentraleSup%C3%A9lec.svg/800px-Logo_CentraleSup%C3%A9lec.svg.png", width = 500/></p>


<p align="center"> <img src="https://www.pressonline.com/illuin-technology/files/2019/08/xlogo-illuin-technology.png.pagespeed.ic.P4glNQKPUa.png", width = 500/></p>

## Installation
### Téléchargement, requirements & model

```bash
$ pip install -r requirements.txt
```

Pour le modèle nous avons fait un lien WeTransfer : https://we.tl/t-4BRXsc3hLV. Si le lien n'est plus valable, veuillez envoyer un mail à l'adresse suivante : wallerand.peugeot@student-cs.fr.

Pour que le scraper web fonctionne, il faut avoir un chromedriver adapté à votre version de chrome. Voici un lien vers lequel diverses versions de chromedriver sont disponibles : https://chromedriver.chromium.org/downloads.

## Usage

Pour ouvrir la page web correspondant à l'outils développé, lancer la ligne de code suivante :

```bash
streamlit run streamlit_demo.py
```

## :package: Structure
```bash
.
│   .gitignore
│   README.md
│   requirements.txt
│   streamlit_demo.py
│   streamlit_pytrends.py
│   streamlit_utils.py
│
├───chromedriver_win32
│       chromedriver.exe
│
├───legacy
│       bs4_scraping.ipynb
│       bs4_scraping.py
│       nbc_df.csv
│       nlp_exploration.ipynb
│       nlp_IE.ipynb
│       scarp_NBC.txt
│       scraping_trafilatura.py
│       selenium.ipynb
│
├───model
│       longformer_finetuned
│
├───notebooks
│       articles_timeseries.ipynb
│       BERT_QA.ipynb
│       classify_relevance.ipynb
│       fine_tuning_NER.ipynb
│       google_news_scraping.ipynb
│       metrics_model_evaluation.ipynb
│       pytrend.ipynb
│       scope_labelling.ipynb
│       scrap_n_zip.ipynb
```
Le dossier legacy regroupe un ensemble de tests que nous avions effectués, notamment au niveau du scraping web, mais qui ne se révèlent pas nécesasirement utiles pour la construction du projet en lui même. 

Les dossiers chromedriver_win32 ainsi que model contiennent les éléments décrits dans la partie installation.
## :world_map: Roadmap

- Step 1 (Novembre / Décembre) : Explorer et cadrer le sujet du projet - Benchmarker les outils de scraping - Sélectionner les 1ers sujets climatiques et les 1ères sources

- Step 2 (Janvier) : Premier pipeline pour scrapper un sujet donnée sur une source donnée - Analyse NLP sur les premières données

- Step 3 (Février) : Généralisation à d’autres sources et sujets - Classifier automatiquement par type de données - Affiner l’analyse des données extraites

- Step 4 (Mars) : Continuer à étendre le spectre d’utilisation de l’outil - Développer une 1ère interface utilisateur

- Step 5 (Avril) : Finaliser les tâches en cours - Identifier les potentiels next steps - Formaliser la présentation du travail réalisé sur l’année









# DeepCV-project
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![Open in Visual Studio Code](https://img.shields.io/badge/Editor-VSCode-blue?style=flat-square&logo=visual-studio-code&logoColor=white)](https://github.dev/ThomasLef/Projet-Illuin) 

Projet de dominante Infonum CentraleSupélec en collaboration avec Illuin Technology.

<p align="center"> <img src="https://upload.wikimedia.org/wikipedia/fr/thumb/8/86/Logo_CentraleSup%C3%A9lec.svg/800px-Logo_CentraleSup%C3%A9lec.svg.png", width = 500/></p>


<p align="center"> <img src="https://www.pressonline.com/illuin-technology/files/2019/08/xlogo-illuin-technology.png.pagespeed.ic.P4glNQKPUa.png", width = 500/></p>

## Installation
### Téléchargement, requirements & model

Pour installer les modules python requis, lancer la ligne de code suivante :

```bash
$ pip install -r requirements.txt
```

Pour le modèle nous avons fait un lien WeTransfer : https://we.tl/t-4BRXsc3hLV. Si le lien n'est plus valable, veuillez envoyer un mail à l'adresse suivante : wallerand.peugeot@student-cs.fr.

Pour que le scraper web fonctionne, il faut avoir un chromedriver adapté à votre version de chrome. Voici un lien vers lequel diverses versions de chromedriver sont disponibles : https://chromedriver.chromium.org/downloads.

## Utilisation

Pour ouvrir la page web Streamlit correspondante à l'outil développé, lancer la ligne de code suivante :

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

## Divers liens et ressources utilisés lors de ce projet

### Bases du NER

- A comprehensive guide to information extraction : https://www.analyticsvidhya.com/blog/2020/06/nlp-project-information-extraction/ 

- Extraction de lieux : https://medium.com/spatial-data-science/how-to-extract-locations-from-text-with-natural-language-processing-9b77035b3ea4

### Fine tuning de NER  

- https://towardsdatascience.com/easy-fine-tuning-of-transformers-for-named-entity-recognition-d72f2b5340e3 (utilise un module python nommé NERDA pour fine tuner des modèles transformer de pytorch ou hugginface) l’architecture utilisée est similaire à celle de cet article : http://www.lrec-conf.org/proceedings/lrec2020/pdf/2020.lrec-1.565.pdf

- https://towardsdatascience.com/custom-named-entity-recognition-using-spacy-7140ebbb3718 (crée un modèle de NER custom avec spaCy)

###  Question answering

- Adversarial SQUAD (Stanford Question Answering Dataset) : https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1184/reports/6908723.pdf

- Would it really be possible to have a single model that could do custom NER and QA on the same data? Can T5 save the day? : https://towardsdatascience.com/would-it-really-be-possible-to-have-a-single-model-that-could-do-custom-ner-and-qa-on-the-same-data-94432f12ff52
 
- A Comparative Study of Transformer-Based Language Models on Extractive Question Answering : https://arxiv.org/pdf/2110.03142.pdf 


- Deep Learning has (almost) all the answers: Yes/No Question Answering with Transformers : https://medium.com/illuin/deep-learning-has-almost-all-the-answers-yes-no-question-answering-with-transformers-223bebb70189



### Score de pertinence

- Matrice de confusion : https://likeabot.io/blog/chatbot-nlp-nlu-comment-evaluer-performance (calcul des faux positifs, etc..)

- Sur la qualité des articles : https://blog.travelpayouts.com/en/how-to-check-an-article-quality/ - https://library.weber.edu/sites/default/files/PDFs/researchandteaching/libs1704/textbook/source_evaluation.pdf


### Classification In-Scope Hors-Scope
- https://jesusleal.io/2020/11/24/Longformer-with-IMDB/ (Longformer)

- https://towardsdatascience.com/text-classification-with-bert-in-pytorch-887965e5820f (BERT)

- https://medium.com/gumgum-tech/handling-class-imbalance-by-introducing-sample-weighting-in-the-loss-function-3bdebd8203b4 (weights in loss for imbalanced data)


### Analyse tendance - Série temporelle

- https://ichi.pro/fr/introduction-aux-series-temporelles-decomposition-des-tendances-avec-python-199330136383544 





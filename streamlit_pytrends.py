from pytrends.request import TrendReq
import plotly.express as px
import plotly.tools as tls

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from nltk.corpus import stopwords
from numpy.fft import fft, fftfreq
import random
import statistics
from statistics import mode


def init_pytrends(topic, nb_years):
    pytrends = TrendReq(hl='en-US', tz=360) 
    kw_list = [topic] 
    pytrends.build_payload(kw_list, cat=16, timeframe='today '+str(nb_years)+'-y')
    return pytrends
    
    
def trend_fig(pytrends, topic):
    data = pytrends.interest_over_time() 
    data = data.reset_index() 
    fig = px.line(data, x="date", y=[topic], title=f'Recherches associées à {topic} au cours du temps')
    #fig.show() 
    return fig


def region_table(pytrends):
    by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    return by_region[by_region[topic] > 10].sort_values(by = topic, ascending = False).head() 


def couleur(*args, **kwargs):
        return "rgb(0, 100, {})".format(random.randint(0, 255)) 



def freq_pos(pytrends):
    X = fft(data[topic])  # Transformée de fourier
    freq = fftfreq(x.size, d=1/(len(data)))  # Fréquences de la transformée de Fourier
    # Calcul du nombre d'échantillon
    N = x.size
    # On prend la valeur absolue de l'amplitude uniquement pour les fréquences positives et normalisation
    X_abs = np.abs(X[:N//2])*2.0/N
    # On garde uniquement les fréquences positives
    freq_pos = freq[:N//2]/nb_years
    return freq_pos

def fft_fig(freq_pos): #Modifier cette fonction pour retourner une figure plotly
    fig = plt.figure()
    fig.plot(freq_pos[1:], X_abs[1:], label="Amplitude absolue")
    fig.xlim(0, 12)  
    fig.grid()
    fig.xlabel(r"Frequency (Peaks/Year)")
    fig.ylabel(r"Amplitude $|X(f)|$")
    fig.title("Frequency analysis")
    
    return tls.mpl_to_plotly(fig)
    
def nb_peaks_per_year(freq_pos):
    return freq_pos[np.argmax(X_abs[1:]) + 1]

def peak_month(topic, nb_years):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pytrends = init_pytrends(topic, nb_years)
    data = pytrends.interest_over_time() 
    data = data.reset_index() 
    no1_month = mode(data[data[topic] > np.quantile(data[topic].values, 0.9)].date.apply(lambda x : x.month).values)
    return months[no1_month - 1]


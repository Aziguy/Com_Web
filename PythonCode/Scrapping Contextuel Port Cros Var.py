# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:18:15 2020

@author: Admin
"""

# ************************[ Librairies Utilisées ]************************************************************************************

import re  # Permet la recherche partielle sur les pages
import time  # pause du script pour évite blacklisting de l'adresse IP

import pandas as pd  # Gestion des Dataframes & Import/ Export Csv
import requests
from bs4 import BeautifulSoup  # Librairie scraping
from tqdm import tqdm  # Affichage d'une barre de progression du script

tqdm.pandas()  # permet l'utilisation de la fonction pd.progress_apply pour voir la progression du script

# ************************[ Traitement Initial ]************************************************************************************
Df = pd.read_csv('appended.csv', encoding='utf-16',
                 sep='\t')  # Ouverture du csv contenant la totalité des adresses recensées
DfFilter = pd.read_csv('DNS Adresses Filtrées.csv', encoding='utf-16',
                       sep='\t')  # Ouverture du csv contenant les adresses varoises

DfVar = pd.merge(Df, DfFilter, on='DNS Source',
                 how='inner')  # On fusionne les deux csv précédents en ne gardant que les adresses ayant un dns en commun

#************************[ Fonctions Utilisées ]************************************************************************************

def Scrapper(Referring,Cible):
    req =''
    soup =''
    link =''
    linkP=''
    if Referring =='':
        pass
    else:
        req = requests.get(Referring) # La variable req récupére l'adresse présente dans 'Referring Page URL'
        soup = BeautifulSoup(req.text, 'lxml') #BeautifulSoup récupére la totalité de la page signalée au dessus
        for link in soup.find_all('a', href=re.compile(Cible)): #la fonction recherche le lien renvoyant vers la page de PortCros sur la page stockée
            linkP = link.parent #On récupére le contexte du lien présent sur la page
        time.sleep(2) #On marque une pause pour éviter le blacklisting potentiel de l'adresse IP sur le site.
    return linkP #On retourne le resultat dans DfVar['Scrapped']


#************************[  ]************************************************************************************

DfVar['Scrapped'] =DfVar.progress_apply(lambda x : Scrapper(x['Referring Page URL'],x ['DNS Cible']),axis=1) #On lance la fonction Scrapper en se basant sur les Colonnes énumérées : le résultat arrive dans "Scrapped"


#************************[ Restitution des données ]************************************************************************************

DfVar.to_csv('outputVar.csv', encoding="utf-16", sep='\t') #Fichier de sortie comportant l'ensemble des données récupérées entre les différentes étapes pour les adresses varoises.

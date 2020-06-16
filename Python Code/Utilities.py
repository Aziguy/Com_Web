# Mes importations
import csv
import json
import os

import folium
import geocoder
import geopy
import pandas as pd
import socket as so
import time
from tqdm.auto import tqdm
from urllib.parse import urlparse

tqdm.pandas()
from arcgis.geocoding import geocode
from arcgis.gis import GIS
from folium import plugins
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from haversine import haversine
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import spacy
from collections import Counter
# nltk.download('stopwords') # Télécharger les `stopwords`
from nltk.corpus import stopwords

stopWords = stopwords.words('french')
nlp = spacy.load('fr_core_news_sm')  # On charge le modèle français
# nlp = spacy.load('en_core_web_sm') # On charge le modèle anglais
nlp2 = spacy.load('en_core_web_lg')  # On charge le modèle le plus large

# geopy.geocoders.options.default_user_agent = 'my_app/1'
geopy.geocoders.options.default_timeout = None


# =============================================================================
# Fonctions `tag_visible()` et `text_from_html()` pour scrapper le contenu de la page d'accueil d'une url
# Elle récupère tout ce qui est vu par l'utilisateur sur la page (tous les textes)
# =============================================================================
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


#######################
# TRAITEMENT DE TEXTE
#######################

# Cette méthode permet de tokenizer mon texte
# Elle retourne une liste

def return_token(texte):
    # Tokeniser la phrase
    mod = nlp(texte)
    # Retourner le texte de chaque token
    return [X.text for X in mod]


# Cette méthode permet de supprimer les stopWords dans mon texte
# Elle retourne une liste

def cleanWords(liste):
    clean_words = []
    for token in liste:
        if token not in stopWords:
            clean_words.append(token)
    return clean_words


# Cette méthode `tupleToString` permet de convertir un tuple en chaine de caractère
# Elle prend en  paramètre un tuple et retourne une chaine (string) qui sera facilement stockable dans un dataframe.
# A l'aide de Spacy (variable `nlp`ou `nlp2`) on pourra facilement itérer sur chaque mot de la chaine de caractère.
def tupleToString(monTuple):
    maListe = []
    maChaine = ""
    for element in monTuple:
        temp = element[0]
        maListe.append(temp)
    maChaine = " ".join(str(x) for x in maListe)

    return maChaine


# Cette méthode ``wordExtractorFromFile`` permet de recenser les mots les plus fréquents dans un texte récupéré via le scraping
# Elle prend en paramètre un fichier excel et retourne un dictionnaire ayant pour clé le type de site et pour valeur la liste des mots du type
def wordExtractorFromFile(fichier):
    # Mes variables
    dicoMotsType = dict()
    common_words = tuple()
    lien, cat = "", ""
    # Lecture de mon fichier Excel
    data = pd.read_excel(fichier, "siteType", usecols="A:C")
    for indice, ligne in data.iterrows():
        cat = ligne['Catégories']
        lien = ligne['URL Acteurs']

        try:
            # reponse = requests.get("http://{}".format(lien))
            html = urllib.request.urlopen("http://{0}".format(lien)).read()
            monTexte = text_from_html(html)
            # NLP : Natural Language Processing
            doc = nlp(monTexte)
            allWords = [token.text for token in doc if
                        token.is_stop != True and token.is_punct != True and token.is_space != True and token.is_digit != True and token.is_ascii and token.is_bracket != True and token.is_currency != True and len(
                            token) > 1]
            # 20 mots les plus fréquents
            word_freq = cleanWords(allWords)
            word_freq_count = Counter(word_freq)
            common_words = word_freq_count.most_common(20)  # common_words contient ici un tuple(mot, nbre occurence)

            for mot in common_words:
                if cat not in dicoMotsType:
                    dicoMotsType[cat] = []
                    dicoMotsType[cat].append(mot[0])
                else:
                    dicoMotsType[cat].append(mot[0])
        except:
            common_wordsm = None
    return dicoMotsType


# Nettoyage du dictionnaire retourné par `wordExtractorFromFile(fichier)` à l'aide de la méthode ``cleanDictionnaire(monDico)``
# Elle nous retourne ici créer un nouveau dictionnaire `dicoMotTypeClean` qui contient la liste unique de mots représentant un type de site
def cleanDictionnaire(monDico):
    dicoMotsType = monDico
    dicoMotTypeClean = dict()

    for cle, valeur in dicoMotsType.items():
        for val in valeur:
            dicoMotTypeClean[cle] = set(valeur)

    return dicoMotTypeClean


# Cette méthode `wordExtratorFromUrl(lien)`
# Elle prend en paramètre un lien (url) et retourne les vingt (20) mots les plus fréquents dans la page d'acceuil du lien.
def wordExtratorFromUrl(lien):
    # Mes variables
    common_words = tuple()
    maChaine = ""
    try:
        # reponse = requests.get("http://{}".format(lien))
        html = urllib.request.urlopen("http://{0}".format(lien)).read()
        monTexte = text_from_html(html)
        # NLP : Natural Language Processing
        doc = nlp(monTexte)
        allWords = [token.text for token in doc if
                    token.is_stop != True and token.is_punct != True and token.is_space != True and token.is_digit != True and token.is_ascii and token.is_bracket != True and token.is_currency != True and len(
                        token) > 1]
        # 20 mots les plus fréquents
        word_freq = cleanWords(allWords)
        word_freq_count = Counter(word_freq)
        common_words = word_freq_count.most_common(20)  # common_words contient ici un tuple(mot, nbre occurence)
    except:
        common_wordsm = None
    # transformation de mon tuple en String
    maChaine = tupleToString(common_words)

    return maChaine


###################
# MAP WITH FOLIUM
###################

# folium.Choropleth

# =============================================================================
# Fonction pour convertir un string en int ou float
# Elle prend en paramètre une chaine de caractere et retoure un nombre
# =============================================================================
def extractDNS_from_Filename(csvName):
    zoneDnsCible = []
    x = csvName.split('-backlinks')
    return x


# =============================================================================
# Fonction qui permet de déterminer la distance entre un lieu donné et le parc port-cros
# Elle prend en paramètre la latitude et la longitude du lieu fait des calculs, et retourne
# la distance en km entre les deux lieux (lieu x et le parc
# =============================================================================
def getDistanceBtwPoints(lat, lon):
    lieuX = (lat, lon)
    parc = (43.0650392, 5.8936821)
    distance = haversine(lieuX, parc)
    return round(distance, 3)

def showEnumerateMarkers(fichier):
    df = pd.read_csv(fichier, encoding='utf-16', sep='\t')  # Lecture du fichier d'adresses
    # Carte
    m = folium.Map([43.9351691, 6.0679194], zoom_start=6)  # La localisation de départ pour cadrer les résultats
    m_Controle = plugins.MeasureControl(position='topleft', active_color='blue', completed_color='red',
                                        primary_length_unit='meters')
    m.add_child(m_Controle)
    # icons utilisant plugins.BeautifyIcon
    for (index, row) in df.iterrows():
        folium.Marker(location=[row['Latitudes'], row['Longitudes']], popup=row['Zone DNS'], tooltip=row['Adresses'],
                      icon=plugins.BeautifyIcon(number=row['Occurrences'], border_color='blue', border_width=1,
                                                text_color='red', inner_icon_style='margin-top:0px;')).add_to(m)
    return m.save(outfile='outputs/EnumerateMarkersZoneDNS.html')  # Le fichier de sortie est une map au format "html"
# =============================================================================
# Fonction qui permet de représenter un fichier d'adresse sur la carte
# Elle prend en paramètre un fichier csv et retourne un fichier html contenant la
# la représentation visuelle des adresses contenues dans le fichier csv donné en entrée
# =============================================================================
def showMapFromAdress(fichier):
    df = pd.read_csv(fichier, encoding='utf-16', sep='\t')  # Lecture du fichier d'adresses
    m = folium.Map([43.9351691, 6.0679194], zoom_start=6)  # La localisation de départ pour cadrer les résultats
    m_Controle = plugins.MeasureControl(position='topleft', active_color='blue', completed_color='red',
                                        primary_length_unit='meters')
    m.add_child(m_Controle)
    for (index, row) in df.iterrows():
        folium.Marker(location=[row['Latitudes'], row['Longitudes']], popup=row['Zone DNS'], tooltip=row['Adresses'],
                      icon=folium.Icon(color='red', icon='info-sign')).add_to(
            m)  # Inscris un marqueur aux endroits donnés avec la lontitude et lagitude
        m.save(outfile='outputs/MapZoneDNS.html')  # Le fichier de sortie est une map au format "html"


def showChoroplethFromAdress(f_csv, f_geojson):
    # Chargement du fichier json
    with open(f_geojson) as var:
        communes = json.load(var)
    for i in communes['features']:
        i['id'] = i['properties']['nom']
    # Chargement du fichier csv
    zoneDNS = pd.read_csv(f_csv, encoding='utf-16', sep='\t')
    # Carte
    bins = list(zoneDNS['Occurrences'].quantile([0, 0.25, 0.5, 0.75, 1]))
    mapChoropleth = folium.Map([43.9351691, 6.0679194],
                               zoom_start=6)  # La localisation de départ pour cadrer les résultats
    # Choropleth
    folium.Choropleth(geo_data=communes, name='choropleth', data=zoneDNS, columns=['Communes', 'Occurrences'],
                      key_on='feature.id', fill_color='BuPu', fill_opacity=0.7, line_opacity=0.2,
                      legend_name='Occurrences', highlight=True, bins=bins, reset=True).add_to(mapChoropleth)
    # Calque de controle (activer ou désactiver Choropleth sur la carte
    folium.LayerControl().add_to(mapChoropleth)
    return mapChoropleth.save(outfile='outputs/choroplethMapZoneDNS.html')


# =============================================================================
# Fonction pour séparer les éléments d'une zone DNS
# Elle prend en paramètre une chaine de caractere et retoure retourne le 1er ou 2e
# Element de cette chaine
# =============================================================================
def dnsZoneSpliting(zoneDNS):
    racine = ''
    if zoneDNS == '':
        pass
    else:
        element = zoneDNS.split('.')
        if len(element) == 2:
            racine = element[0]
        else:
            racine = element[1]
    return racine


# =============================================================================
# ArcGis
# Fonction pour récupérer les coordonnées de la zone DNS
# Elle prend en paramètre une zone DNS et retourne ses coordonnées (adresse complète)
# =============================================================================
def getFullAdress(zoneDNS):
    dns = zoneDNS
    adresse = ''
    commune = ''
    latitude = 0
    longitude = 0
    codePostale = 0
    csv_sortie = []
    gis = GIS("http://www.arcgis.com", "Aziguy88", "LYNEpromotion2012")
    if zoneDNS == '':
        pass
    else:
        geocode_result = geocode(address=dns)

    for x in geocode_result:
        if 'FR' in x['attributes']['Country'] and 'Var' in (
                x['attributes']['LongLabel'] or x['attributes']['Subregion']):

            adresse = x['attributes']['LongLabel']
            latitude = x['attributes']['Y']
            longitude = x['attributes']['X']
            codePostale = x['attributes']['Postal']
            commune = x['attributes']['City']

            with open('outputs/ZoneDNSFullAdresses.csv', 'a', encoding='utf-16', newline='') as fichierSortie:
                csv_sortie = csv.writer(fichierSortie, delimiter='\t')
                fichierVide = os.stat('outputs/ZoneDNSFullAdresses.csv').st_size == 0

                if fichierVide:
                    csv_sortie.writerow(['DNS Source', 'Adresses', 'Latitudes', 'Longitudes', 'Codes', 'Communes'])
                else:
                    csv_sortie.writerow([dns, adresse, latitude, longitude, codePostale, commune])
            time.sleep(2)
        else:
            pass
            # raise ValueError("{0} ne correspond pas aux critères".format(dns))
    return csv_sortie


# =============================================================================
# Geopy
# Fonction pour récupérer les coordonnées d'un acteur
# Elle prend en paramètre une chaine et retourne ses coordonnées
# =============================================================================
def getFullAdressByGeopy(maChaine):
    monAdresse = ''
    mesCoordonnees = []
    geolocator = Nominatim(user_agent="my-application", timeout=3)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    if maChaine == '':
        pass
    else:
        location = geolocator.geocode(maChaine)
        if location == None:
            monAdresse = 'Nan'
            mesCoordonnees = 'Nan'
        else:
            monAdresse = location.address
            mesCoordonnees = location.latitude, location.longitude
    return monAdresse, mesCoordonnees


# =============================================================================
# Fonction pour convertir un string en int ou float
# Elle prend en paramètre une chaine de caractere et retoure un nombre
# =============================================================================
def nombre(chaine):
    x = 0
    if chaine == '':
        pass
    elif '.' in chaine:
        x = float(chaine)
    else:
        x = int(chaine)
    return x


# =============================================================================
# Fonction pour parser une url
# Elle prend en paramètre une url et retourne son DNS
# =============================================================================
def parsage(url):
    if url == '':
        pass
    else:
        obj = urlparse(url)
    return obj.netloc


# =============================================================================
# Fonction qui compte le nombre de fois qu'une url est présente dans une liste
# Elle prend en paramètre une liste et retourne un dictionnaire contenant chaque url et son nombre d'ocurence dans la liste
# =============================================================================
def occurences(maListe):
    dictDiffUrl = dict()
    for element in maListe:
        if element == '':
            pass
        elif element in dictDiffUrl:
            dictDiffUrl[element] += 1
        else:
            dictDiffUrl[element] = 1
    return dictDiffUrl


# =============================================================================
# Fonction qui permet d'écrire dans un fichier csv
# Elle prend en paramètre un fichier csv et restitue un autre csv bien formater avec zone DNS parsées...
# =============================================================================
def exportCsvAhref(csvFile):
    with open(csvFile, 'r', encoding='utf-16') as fichier:
        data = csv.reader(fichier, delimiter='\t')
        next(data)

        for ligne in data:
            numero = nombre(ligne[0])
            domainRating = nombre(ligne[1])
            urlRating = nombre(ligne[2])
            referringDomains = nombre(ligne[3])
            referringPageURL = parsage(ligne[4])
            referringPageTitle = ligne[5]
            internalLinksCount = nombre(ligne[6])
            externalLinksCount = nombre(ligne[7])
            linkURL = parsage(ligne[8])
            textPre = ligne[9]
            linkAnchor = ligne[10]
            textPost = ligne[11]
            type = ligne[12]
            firstSeen = ligne[14]
            lastCheck = ligne[15]
            language = ligne[17]
            traffic = nombre(ligne[18])
            Keywords = nombre(ligne[19])
            linkedDomains = nombre(ligne[21])

            with open('sortieZoneA.csv', 'a', encoding='utf-16', newline='') as fichierSortie:
                csv_sortie = csv.writer(fichierSortie, delimiter='\t')
                fichierVide = os.stat('sortieZoneA.csv').st_size == 0
                if fichierVide:
                    csv_sortie.writerow(
                        ['Numéro', 'DR', 'UR', 'RD', 'RPU', 'RPT', 'ILC', 'ELC', 'LU', 'TP', 'LA', 'TP', 'Type', 'FS',
                         'LC', 'Lang', 'Trafic', 'Keywords', 'LD'])
                else:
                    csv_sortie.writerow(
                        [numero, domainRating, urlRating, referringDomains, referringPageURL, referringPageTitle,
                         internalLinksCount, externalLinksCount, linkURL, textPre, linkAnchor, textPost, type,
                         firstSeen, lastCheck, language, traffic, Keywords, linkedDomains])

    return csv_sortie


# =============================================================================
# Fonction qui permet de retourner 3 dictionnaires (attributs, source_cible, numéro_lien
# Elle prend en paramètre un fichier csv et restitue 3 dictionnaires
# =============================================================================
def mesDictionnaires(monFichierCsv):
    with open(monFichierCsv, 'r', encoding='utf-16') as fichier:
        mesDonnees = csv.reader(fichier, delimiter='\t')
        next(mesDonnees)

        # Création de mes dictionnaire soit avec {} soit à partir du constructeur dict()
        noeuds = dict()
        attribut = dict()
        liens = dict()

        zoneDNSCible = ['www.portcrosparcnational.fr', 'prod-pnpc.parcnational.fr', 'www.portcros-parcnational.fr']
        for cible in zoneDNSCible:
            noeuds[cible] = 0  # agregation de la ZoneDNSCible

        indexCourant = 1

        for colonne in mesDonnees:
            # Sachant que la colonne[4] est la source
            source = parsage(colonne[4])
            # Sachant que la colonne[8] est la destination
            dest = parsage(colonne[8])

            if source not in noeuds.keys():
                noeuds[source] = indexCourant
                indexCourant += 1

                attribut[source] = dict()
                attribut[source]['Domain Rating'] = nombre(colonne[1])
                attribut[source]['Url Rating'] = nombre(colonne[2])
                attribut[source]['Referring Domains'] = nombre(colonne[3])
                attribut[source]['Referring Page Title'] = colonne[5]
                attribut[source]['Internal Links Count'] = nombre(colonne[6])
                attribut[source]['External Links Count'] = nombre(colonne[7])
                attribut[source]['Link URL'] = colonne[8]
                attribut[source]['Text Pre'] = colonne[9]
                attribut[source]['LinkAnchor'] = colonne[10]
                attribut[source]['Text Post'] = colonne[11]
                attribut[source]['Type'] = colonne[11]
                attribut[source]['First Seen'] = colonne[14]
                attribut[source]['Last Check'] = colonne[15]
                attribut[source]['Language'] = colonne[17]
                attribut[source]['Traffic'] = nombre(colonne[18])
                attribut[source]['Keywords'] = nombre(colonne[19])
                attribut[source]['Linked Domains'] = nombre(colonne[21])

                # Gestion du lien
                liens[(source, dest)] = 1

            else:
                if (source, dest) in liens.keys():
                    liens[(source, dest)] += 1
                else:
                    liens[(source, dest)] = 1

    return attribut, liens, noeuds


# ============================================================================
# Cette fonction permet de récupérer l'adresse du serveur d'une zone DNS
# Elle en paramètre la zoneDNS et retourne ses coordonnées et adresse
# ============================================================================
def localisationServeur(url):
    ipAdd = so.gethostbyname(url)
    g = geocoder.ip(ipAdd)
    x = g.latlng
    y = g.address
    return x, y

# Mes importations
import csv
import os
import socket as so
import time
from urllib.parse import urlparse

import folium
import geocoder
import geopy
import pandas as pd
from arcgis.geocoding import geocode
from arcgis.gis import GIS
from geopy.geocoders import Nominatim

# geopy.geocoders.options.default_user_agent = 'my_app/1'
geopy.geocoders.options.default_timeout = None


# =============================================================================
# Fonction pour convertir un string en int ou float
# Elle prend en paramètre une chaine de caractere et retoure un nombre
# =============================================================================
def extractDNS_from_Filename(csvName):
    zoneDnsCible = []
    x = csvName.split('-backlinks')
    return x


# =============================================================================
# Fonction qui permet de représenter un fichier d'adresse sur la carte
# Elle prend en paramètre un fichier csv et retourne un fichier html contenant la
# la représentation visuelle des adresses contenues dans le fichier csv donné en entrée
# =============================================================================
def showMapFromAdress(fichier):
    df = pd.read_csv(fichier, encoding='utf-16', sep='\t')  # Lecture du fichier d'adresses
    m = folium.Map([43.9351691, 6.0679194], zoom_start=6)  # La localisation de départ pour cadrer les résultats
    for (index, row) in df.iterrows():
        folium.Marker(location=[row['Latitudes'], row['Longitudes']], popup=row['Zone DNS'], tooltip=row['Adresses'],
                      icon=folium.Icon(color='red', icon='info-sign')).add_to(
            m)  # Inscris un marqueur aux endroits donnés avec la lontitude et lagitude
        m.save(outfile='outputs/ZoneDNS.html')  # Le fichier de sortie est une map au format "html"


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
    latitude = 0
    longitude = 0
    csv_sortie = []
    gis = GIS()
    geocode_result = geocode(address=dns)

    for x in geocode_result:
        if 'FR' in x['attributes']['Country'] and 'Var' in (
                x['attributes']['LongLabel'] or x['attributes']['Subregion']):

            adresse = x['attributes']['LongLabel']
            latitude = x['attributes']['Y']
            longitude = x['attributes']['X']

            with open('outputs/fullAdressesZoneDNS.csv', 'a', encoding='utf-16', newline='') as fichierSortie:
                csv_sortie = csv.writer(fichierSortie, delimiter='\t')
                fichierVide = os.stat('outputs/fullAdressesZoneDNS.csv').st_size == 0

                if fichierVide:
                    csv_sortie.writerow(['Zone DNS', 'Adresses', 'Latitudes', 'Longitudes'])
                else:
                    csv_sortie.writerow([dns, adresse, latitude, longitude])
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
    geolocator = Nominatim(user_agent="my-application")
    geolocator = Nominatim(user_agent="my-application")
    from geopy.extra.rate_limiter import RateLimiter
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
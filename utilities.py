# Mes importations
import csv
import geocoder
import os
import socket as so
from urllib.parse import urlparse


# =============================================================================
# Fonction pour convertir un string en int ou float
# Elle prend en paramètre une chaine de caractere et retoure un nombre
# =============================================================================
def eltFichier(csvName):
    zoneDnsCible = []
    x = csvName.split('-backlinks')
    return x


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
# Fonction pour avoir le nombre total d'url différent d'une liste
# Elle prend en paramètre une liste d'url et retourne le total d'url différent de la liste
# =============================================================================
def nbreDifUrl(liste):
    tabUrl = []
    nbreUrl = []

    for element in liste:
        temp = element[6]
        tabUrl.append(temp)
    for x in tabUrl:
        if x not in nbreUrl:
            nbreUrl.append(x)
    return len(nbreUrl)


# =============================================================================
# Fonction qui compte le nombre de fois qu'une url est présente dans une liste
# Elle prend en paramètre une liste et retourne un dictionnaire contenant chaque url et son nombre d'ocurence dans la liste
# =============================================================================
def occurences(maListe):
    dictDiffUrl = {}
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
        mesDonnes = csv.reader(fichier, delimiter='\t')
        next(mesDonnes)

        # Création de mes dictionnaire soit avec {} soit à partir du constructeur dic()
        noeuds = dict()
        attribut = dict()
        liens = dict()

        indexCourant = 1

        for colonne in mesDonnes:
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


# # Identification de tous les noeuds cibles
# zoneDNSCible = ['www.portcrosparcnational.fr', 'prod-pnpc.parcnational.fr', 'www.portcros-parcnational.fr']
# for cible in zoneDNSCible:
#     noeuds[cible] = 0  # agregation de la ZoneDNSCible
#
# # Identification de tous les noeuds sources
# noeuds = dict()
# noeuds[zonesDNS] = numero  # un index des noeuds (différent pour chaque site)
# noeuds[zonesDNS] = numero  # un index des noeuds (différent pour chaque site)
#    tab = {}

# ============================================================================
# Cette fonction permet de récupérer l'adresse d'une zone DNS
# Elle en paramètre la zoneDNS et retourne ses coordonnées et adresse
# ============================================================================
def localisation(url):
    ipAdd = so.gethostbyname(url)
    g = geocoder.ip(ipAdd)
    x = g.latlng
    y = g.address
    return x, y


# =============================================================================
# Fonction qui permet d'écrire dans un fichier
# Elle prend en paramètre une liste et retourne un dictionnaire contenant chaque url et son nombre d'ocurence dans la liste
# =============================================================================
def createCsv():
    with open('sortieZoneA.csv', 'a', encoding='utf-8', newline='') as fichierSortie:
        csv_sortie = csv.writer(fichierSortie)
        fichierVide = os.stat('sortieZoneA.csv').st_size == 0
        if fichierVide:
            csv_sortie.writerow(['Numéro', 'DNS sources', 'Occurences', 'DNS cibles'])
        else:
            csv_sortie.writerow([numero, dnsSource, occurences, dnsCible])


# =============================================================================
# Fonction qui permet d'écrire dans un fichier
# Elle prend en paramètre un csv et écrit son contenu dans un autre fichier csv
# =============================================================================
def writeCsv(fichierCsv):
    with open(fichierCsv, 'r') as fichier:
        lecture = csv.reader(fichier)
        with open('zoneDNS_A.csv', 'w') as file_out:
            ecriture = csv.writer(file_out, delimiter='\t')
            for ligne in lecture:
                ecriture.writerow(ligne)


def writeCsvDict(fichierCsv):
    with open(fichierCsv, 'r') as fichier:
        lecture = csv.DictReader(fichierCsv)
        with open('file_out.csv', 'w') as file_out:
            entete = ['Numéro', 'X']
            ecriture = csv.DictWriter(file_out, fieldnames=entete, delimiter='\t')
            ecriture.writeheader()
            for x in lecture:
                ecriture.writerow(x)
'''
www.portcrosparcnational.fr-backlinks-subdomains-live-23-Feb-2020_16-35-25-f10142e96c2cbfcacbf0a3fe239127ea
zoneDnsCible = []
for nomFichierCsv, zoneDnsCible.append(nomFichierCsv.split('backlinks')[0])
# Pour chaque nom de fichierCSV, zoneDnsCible.append(nomFichierCsv.split('-backlinks')[0])

# Identification de tous les noeuds cibles
zoneDNSCible = ['www.portcrosparcnational.fr', 'prod-pnpc.parcnational.fr', 'www.portcros-parcnational.fr']
for cible in zoneDNSCible:
	noeuds[cible]= 0 # agregation de la ZoneDNSCible

# Identification de tous les noeuds sources
noeuds = {}
noeuds[zonesDNS] = numero # un index des noeuds (différent pour chaque site)

tab = {}
liens = dict()

indexCourant = 1
for ligne in dataCsv:
	col = ligne.split() # col[4] est la source
	source = utils.parsage(col[4])
	dest = utils.parsage(col[8])
	
	if source not in noeud.keys():
		noeud[source] = indexCourant
		indexCourant += 1
		
		attribut[source] = dict()
		attribut[source]['Domain Rating'] = utils.nombre(col[1])
		attribut[source]['Url Rating'] = utils.nombre(col[2])
        attribut[source]['Referring Domains'] = utils.nombre(col[3])
        attribut[source]['Referring Page Title'] = col[5]
        attribut[source]['Internal Links Count'] = utils.nombre(col[6])
        attribut[source]['External Links Count'] = utils.nombre(col[7])
        attribut[source]['Link URL'] = col[8]
        attribut[source]['Text Pre'] = col[9]
        attribut[source]['LinkAnchor'] = col[10]
        attribut[source]['Text Post'] = col[11]
        attribut[source]['Type'] = col[11]
        attribut[source]['First Seen'] = col[14]
        attribut[source]['Last Check'] = col[15]
        attribut[source]['Language'] = col[17]
        attribut[source]['Traffic'] = utils.nombre(col[18])
        attribut[source]['Keywords'] = utils.nombre(col[19])
        attribut[source]['Linked Domains'] = utils.nombre(col[21])

        # Gestion du lien
        liens[(source, dest)] = 1

	else:
		if (source, dest) in Liens.keys():
	        liens[(source, dest)] += 1
        else:
	        liens[(source, dest)] = 1

# A ce stade, tous les noeuds et liens sont créés

'''

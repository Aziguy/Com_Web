# Mes importations
from urllib.parse import urlparse


# =============================================================================
# Fonction pour parser une url
# Elle prend en paramètre une url et retourne son DNS
# =============================================================================
def parsage(url):
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
        if element in dictDiffUrl:
            dictDiffUrl[element] += 1
        else:
            dictDiffUrl[element] = 1
    return dictDiffUrl

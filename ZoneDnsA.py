# Mes importations
import csv
import utilities as utils

# =============================================================================
# ? Ouverture et lecture du fichier www.portcrosparcnational.fr-backlinks-subdomains.csv en mode lecture
# =============================================================================

with open('www.portcrosparcnational.fr-backlinks-subdomains.csv', 'r', encoding='utf-16') as fichier:
    data = csv.reader(fichier, delimiter='\t')
    # Création de mes listes vides
    listeZoneCible = []
    listeZoneSource = []

    for ligne in data:
        temp = utils.parsage(ligne[4])
        listeZoneCible.append(temp)
    print(len(listeZoneCible))
    print(listeZoneCible[1:14])
    print(utils.occurences(listeZoneCible))

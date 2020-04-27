# Mes importations
import networkx as nx

import Utilities as utils

# =============================================================================
# On peut appeller la fonction exportCsvAhref(monFichierCSV) ici
# Ouverture et lecture du fichier www.portcrosparcnational.fr-backlinks-subdomains.csv
# =============================================================================
'''
exporter = utils.exportCsvAhref('www.portcrosparcnational.fr-backlinks-subdomains.csv')
'''

# =============================================================================
# On peut appeller la fonction mesDictionnaires(monFichierCSV) ici
# Ouverture et lecture du fichier www.portcrosparcnational.fr-backlinks-subdomains.csv
# =============================================================================

dico = utils.mesDictionnaires('www.portcrosparcnational.fr-backlinks-subdomains.csv')
attribut = dico[0]  # Attributs
liens = dico[1]  # Liens
noeuds = dico[2]  # Noeuds

newDict = dict()
# for cle in attribut:
#     newDict = attribut[cle]
#     # if cle[0] == attribut[0]:
#     #     newDict['Occurrences'] = valeur
#     print(cle,":",attribut[cle])


print(attribut)
print(liens)
print(noeuds)

G = nx.DiGraph()

for cle, valeur in liens.items():
    G.add_node(cle[0])
    G.add_edge(cle[0], cle[1], weight=valeur)

# print(G.nodes())
# print(G.edges())
# nx.write_gexf(G, "DomaineAggregation.gexf")
# Pour visualiser avec matplotlib.pyplot
# nx.draw(G, with_labels=True)
# plt.show()

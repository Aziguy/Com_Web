# Mes importations
import networkx as nx

import utilities as utils

"""
Alors après avoir mis les fichiers sources et modifié en fonction de ma structure de données, 
çà a l'air de marcher, mais faudrait le prouver en ne construisant le réseau wue sur quelques lignes
c'est ce que j'ai tenté par la modification de la boucle de création à partir de la structure liens
pour ne considérer que les 20 premières. 
Mais comme les calculs se font sur l'intégralité du fichier ben on peut pas voir (c'est le défaut des
fonctions qui font "tout". Cf. le fichier gexf extrait.

Note: en faisant seulement la boucle sur les liens, tu ne peux mettre d'attributs aux noeuds 
et tu ne contrôle pas l'index (leur numéro)) pour le faire plus tard... 
C'est pour çà que mes suggestions étaient de d'abord créer les noeuds ;-)

)
"""


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

dico = utils.mesDictionnaires('./PNPC/www.portcrosparcnational.fr-backlinks-subdomains.csv')
print(dico[0])  # Attributs
print(dico[1])  # Liens
print(dico[2])  # Noeuds

liens = dico[1]
noeuds = dico[2]
G = nx.DiGraph()

for cle, valeur in list(liens.items())[0:20]:
    G.add_node(cle[0])
    G.add_edge(cle[0], cle[1], weight=valeur)

print(G.nodes())
print(G.edges())
nx.write_gexf(G, "DomaineAggregation.gexf")
# Pour visualiser avec matplotlib.pyplot
nx.draw(G, with_labels=True)
#autres visus
# nx.draw_kamada_kawai(G, with_labels=True) 
# nx.draw_planar(G, with_labels=True)



# import matplotlib.pyplot as plt

# plt.show()

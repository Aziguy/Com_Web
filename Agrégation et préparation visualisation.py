# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 10:32:45 2020

@author: Admin
"""


#************************[ Librairies Utilisées ]************************************************************************************


import pandas as pd    #Gestion des Dataframes & Import/ Export Csv
from urllib.parse import urlparse #Utilisation de l'option netloc pour filtrer les DNS
import networkx as nx #Utilisation pour export du résultat en format Gexf pour visualisation



#************************[ Fonctions Utilisées ]************************************************************************************

#On créée une fonction qui va effectuer un netloc (récupération adresse DNS) des adresses présentes dans le document
def Parser(url):
    if url == '':
        pass
    else:
        obj = urlparse(url)
    return obj.netloc
        

#************************[ Traitement Initial ]************************************************************************************


df0 = pd.read_csv('www.portcrosparcnational.fr-backlinks.csv', encoding='utf-16', sep='\t') #ouveture de la source 1
df1 = pd.read_csv('www.portcros-parcnational.fr-backlinks.csv', encoding='utf-16', sep='\t') #ouverture de la source 2
df2 = pd.read_csv('prod-pnpc.parcnational.fr-backlinks.csv', encoding='utf-16', sep='\t') #ouverture de la source 3

print(df0.head()) #Vérification d'acquisition
print('*****************************************')
print(df1.head()) #Vérification d'acquisition
print('*****************************************')
print(df2.head()) #Vérification d'acquisition
print('*****************************************')



dfappend = df0.append([df1,df2], ignore_index=True) #On créé le contenu dfappend qui est l'ensemble des csv à la suite. La fonction Ignore_index créé un nouvel index qui ne se base pas sur les précédents.
dfappend.reset_index(drop=True)


#************************[ Ajout de Colonnes Dataframe ]************************************************************************************

dfappend['DNS Source'] = dfappend['Referring Page URL'].apply(lambda x : Parser(x)) #on créé un netloc de Ref dans dfappend
dfappend['DNS Cible'] = dfappend['Link URL'].apply(lambda y : Parser(y))        # On créé un netloc de Link dans dfappend


dfappend['DNS de Sortie'] = dfappend['DNS Cible'] #On créé une colonne DNS Sortie qui est la copie de DNS Cible
dfappend['DNS de Sortie'].replace(to_replace=["www.portcrosparcnational.fr","prod-pnpc.parcnational.fr"], value="www.portcros-parcnational.fr", inplace=True) #On remplace les DNS servant de redirection par le nom du DNS vers lequel ils redirigent (DNS connu)


#************************[ Filtrage d'occurence : variable dfmax ]************************************************************************************

idx = dfappend.groupby(['DNS Source'])['Traffic'].transform(max) == dfappend['Traffic'] #A partir de la colonne 'DNS Source' nous recherchons l'occurence ayant la plus haute valeur par rapport à la valeur de Traffic
dfmax =dfappend[idx]
dfmax.drop_duplicates('DNS Source', inplace=True)

#************************[ Compteur d'occurences ]************************************************************************************

NodeRef = dfappend['DNS Source'] # Création d'une liste comportant les différents DNS du CSV

NodeIndex= pd.Index(NodeRef) #On créée un index des DNS avec Panda

NodeCount = NodeIndex.value_counts().reset_index() #On compte le nombre de fois que chaque DNS est présent dans la liste (Value_Count) et on attribue un numéro à chaque DNS (reset_index)

NodeCount.columns = ['DNS Source', 'Occurences'] #On renomme les colonnes de manière à ce qu'il soit possible de comprendre leur correspondance

print(NodeCount) #Vérification d'acquisition

Agreg = pd.merge(NodeCount, dfmax, on='DNS Source', how='outer') #On fusionne les deux tableaux (NodeCount, dfmax) à partir de la colonne DNS Source présente au sein des deux


#************************[ Restitution des données ]************************************************************************************

Agreg.to_csv('agrégation réseau.csv' ,encoding='utf-16', sep="\t") #Fichier de sortie correspondant aux valeurs les plus "fortes" du réseau. (Pour la partie 1)

NodeCount.to_csv('Index réseau.csv' ,encoding='utf-16', sep="\t") # Index de tous les sites utilisant le réseau sélectionné. Sert de base pour la géolocalisation des différentes entreprises (Pour la partie 2 et 3)

dfappend.to_csv('appended.csv' , encoding='utf-16', sep="\t") #Fichier comprenant l'ensemble des données sans filtre. Sera utilisé pour l'acquisition de contexte (Pour la partie 3)


#************************[ Visualisation de données ]************************************************************************************

G = nx.from_pandas_edgelist(Agreg,'DNS Source','DNS de Sortie','Occurences') #On créée une variable G qui comporte une edgelist pour Panda
#nx.draw(G, with_labels=True) #On effectue un essai pour voir si la variable est lisible en format graph
nx.write_gexf(G,"agrégation.gexf") #On exporte la variable G en format gexf sous le nom "Output.gexf"

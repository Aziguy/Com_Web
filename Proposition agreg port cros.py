# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:47:59 2020

@author: admin
"""
#import seaborn as sns

import pandas as pd
from urllib.parse import urlparse
#import networkx as nx


#On créée une fonction qui va effectuer un netloc (récupération adresse DNS) des adresses présentes dans le document
def Parser(url):
    if url == '':
        pass
    else:
        obj = urlparse(url)
    return obj.netloc

#************************************************************************************************************

df = pd.read_csv('test.csv', index_col=0, encoding='latin-1', sep=';')  #on ouvre le csv avec Panda

#************************************************************************************************************


df['DNS Source'] = df['Referring Page URL'].apply(lambda x : Parser(x)) #on créé un netloc de Ref dans DF
df['DNS Cible'] = df['Link URL'].apply(lambda y : Parser(y))        # On créé un netloc de Link dans Df


#************************************************************************************************************

idx = df.groupby(['DNS Source'])['Traffic'].transform(max) == df['Traffic'] #A partir de la colonne 'DNS Source' nous recherchons l'occurence ayant la plus haute valeur par rapport à la valeur de Traffic
dfmax =df[idx]

#************************************************************************************************************

Ref=df['Referring Page URL']  #On attribue à la variable Ref le contenu de la colonne nommée (Reffering Page Url dans cet exemple)


Count = Ref.value_counts() #On compte le nombre de fois que chaque adresse est présente dans le document
NodeRef =[Parser(url) for url in Ref]  # on créée une liste des différents DNS présent dans le CSV


NodeIndex= pd.Index(NodeRef) #On créée un index des DNS avec Panda


#************************************************************************************************************
NodeCount = NodeIndex.value_counts().reset_index() #On compte le nombre de fois que chaque DNS est présent dans la liste (Value_Count) et on attribue un numéro à chaque DNS (reset_index)


NodeCount.columns = ['DNS Source', 'Occurences'] #On renomme les colonnes de manière à ce qu'il soit possible de comprendre leur correspondance


Output = pd.merge(NodeCount, dfmax, on='DNS Source', how='outer') #On fusionne les deux tableaux (NodeCount, dfmax) à partir de la colonne DNS Source présente au sein des deux

print (Output)


#************************************************************************************************************
#On extrait les résultats sous forme de CSV
Output.to_csv('output.csv' , sep=";")

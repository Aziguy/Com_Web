# Mes importations
import Utilities as utils
import networkx as nx
import pandas as pd

# =============================================================================
# Lecture du fichier www.portcrosparcnational.fr-backlinks-subdomains.csv
# =============================================================================
df = pd.read_csv('datasets/www.portcrosparcnational.fr-backlinks-subdomains.csv', encoding='utf-16', sep='\t')
# =============================================================================

# Nous supprimons les trois (03) colonnes vides du fichier csv
df.drop(['Backlink Status', 'Day Lost', 'Js rendered'], axis='columns', inplace=True)
# On convertie les colonnes 'Referring Domains' et 'Keywords' en entier
df['Referring Domains'] = df['Referring Domains'].map(int, na_action='ignore')
df['Keywords'] = df['Keywords'].map(int, na_action='ignore')
# A l'aide de la fonction apply et de l'expression lambda, on effecue une itération dans les colonnes 'Referring Page URL' et 'Link URL'
# On leur applique la fonction parsage()
df['DNS Source'] = df['Referring Page URL'].apply(lambda x: utils.parsage(x))
df['DNS Cible'] = df['Link URL'].apply(lambda y: utils.parsage(y))

# A partir de la colonne 'DNS Source' nous recherchons l'occurence ayant la plus haute valeur par rapport à la valeur de 'Traffic'
groupe = df.groupby(['DNS Source'])['Traffic'].transform(max) == df['Traffic']
dfMax = df[groupe]
# On supprime les doublons s'il y en a
dfMax.drop_duplicates('DNS Source', inplace=True)

# On extrait et affecte la colonne 'DNS Source' à zoneDNS
# Le but ici est de pouvoir déterminer le nombre d'occurence de chaque zone DNS
zoneDNS = df['DNS Source']
nodeIndex = pd.Index(zoneDNS)
nombreDNS = nodeIndex.value_counts().reset_index()  # On compte le nombre de fois que chaque DNS est présent dans la liste (Value_Count) et on attribue un numéro à chaque DNS (reset_index)
nombreDNS.columns = ['DNS Source', 'Occurrences']  # On renomme les colonnes par 'DNS Source' et 'Occurrences'

# On fusionne les deux tableaux (nombreDNS, dfMax) à partir de la colonne DNS Source présente au sein des deux
sortie = pd.merge(nombreDNS, dfMax, on='DNS Source', how='outer')

# On enregistre le contenu de sortie dans un fichier csv
# sortie.to_csv('outputs/zoneDNS.csv', encoding='utf-16', index=False, header=True, sep='\t')

# On fait un export vers un fichier de type Gephy
G = nx.from_pandas_edgelist(sortie, 'DNS Source', 'DNS Cible', 'Occurrences')
nx.write_gexf(G, "outputs/zoneDNSAgregees.gexf")

# =============================================================================
# Test doc pandas
# =============================================================================
# df['Occurrences'] = d
# df['Occ'] = df['Referring Page URL'].value_counts()
# print(df.head())
# df['Zone DNS Source'] = df['Referring Page URL'].apply(lambda x : utils.parsage(x))
# df['Zone DNS Cible'] = df['Link URL'].apply(lambda y : utils.parsage(y))
# print(df.head())
# df['Occurences'] = df['Zone DNS Source'].value_counts()
# print(df['Zone DNS Source'].value_counts())

# print(df.iloc[:5,22:].head(10))
# for i,j in df.head(5).iterrows():
#     print(utils.parsage(j['Referring Page URL']), utils.parsage(j['Link URL']))
# df.replace('NaN', np.nan, inplace = True)
# print(df.head(5))
# print(df.isnull().sum()/len(df)) # Permet de comptabiliser le nbre de valeur manquantes dans le dataFrame pour chaque colonne
# print(df.applymap(type)==str)
# # print(df.info())
# df.fillna(0) # Permet de remplacer les valeurs nuls par 0 dans mon dataFrame
# df.dropna(axis=1) # Permet de supprimer les colonnes où il ya des valeurs manquantes
# df.dropna(axis=0) # Permet de supprimer les lignes où il ya des valeurs manquantes
# df['Nom de ma colonne'] = df['Nom de ma colonne'].map(int,na_action='ignore') # Permet de convertir ma colonne en int
# len(df['Nom de ma colonne'].unique()) # Retourne le nbre d'élément unique de ma colonne
# df.drop_duplicates(subset=['Nom de ma colonne'],keep='first', inplace=True) # Permet de supprimer les doublons de ma colonne
# df.reset_index(inplace=True)
# df['Nom de ma new colonne'] = df['Nom de ma colonne'].apply(lambda x : nomDeMaFonction(x)) # Applique une fonction sur chaque ligne de ma colonne
# df['Nom de ma colonne'].value_counts()
# df.rename(columns={'old name':'new name'}, inplace=True) # renommer une colonne

# df.fillna(0)
# newDf = pd.DataFrame()
# for num, link in df.groupby("Referring Page URL"):
#     if newDf.empty:
#         newDf = link.set_index('#')[['Linked Domains']].rename(columns={'Linked Domains':num})
#     else:
#         newDf = newDf.join(link.set_index('#')[['Linked Domains']].rename(columns={'Linked Domains': num}))
# df2 = df.groupby('Referring Page URL').max()#.agg(['max', 'count']).to_csv('example.csv', encoding='utf-16', index=False, header=True, sep='\t')
# print(type(df2))

# print(test2)
# pd.set_option("display.max_columns",30)
# print(test)
# newDf.to_csv('example1.csv', encoding='utf-16', index=True, header=True, sep='\t')
# print(df[df['Referring Domains'] == df['Referring Domains'].max()])
# print(df2.head(2))

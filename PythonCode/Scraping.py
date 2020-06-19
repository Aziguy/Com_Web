# Mes importations
import Utilities as utils
from tqdm.auto import tqdm

# Récupération des adresses des zones DNS
tqdm.pandas()
# df = pd.read_csv('outputs/zoneDNS.csv', encoding='utf-16', sep='\t')
# df['DNSSource2'] = df['DNS Source'].progress_apply(lambda x: utils.getFullAdress(x))

# Visualisation des zone DNS sur la carte
# monFichier = 'outputs/fullAdressesZoneDNS.csv'
# utils.showMapFromAdress(monFichier)

# Visualisation des zones DNS en mode choropleth
monCSV = 'datasets/zoneDNSFiltrees.csv'
monGeoJson = 'datasets/communes-83-var.geojson'
utils.showChoroplethFromAdress(monCSV, monGeoJson)

# Visualisation des zones en mode enumerate markers
# monCSV = 'datasets/ZoneDNSFullAdressesZoneDNS.csv'
# utils.showEnumerateMarkers(monCSV)
# Lecture du fichier csv
# df = pd.read_csv('datasets/index_reseau.csv', encoding='utf-16', sep='\t')
# df['Complémentaire'] = df['DNS Source'].progress_apply(lambda x : utils.getFullAdress(x))
# print(df['Complémentaire'].head(3))

# Fusion de fichiers avec la fonction merge()
# df1 = pd.read_csv('datasets/DNSAdressesFiltrees.csv', encoding='utf-16', sep='\t')
# df2 = pd.read_csv('datasets/index_reseau.csv', encoding='utf-16', sep='\t')
# df_Merge = df1.merge(df2[['DNS Source','Occurrences']], how='inner', left_on=['Zone DNS'], right_on=['DNS Source'], left_index=False, right_index=False)
# df_Merge.to_csv('outputs/zoneDNSFiltrees.csv', encoding='utf-16', sep='\t')
# df['mesAdresse'] = df['DNS Source'].apply(lambda x : utils.dnsZoneSpliting(x))
# clearAdresse = df['mesAdresse']
# clearAdresse.drop_duplicates(keep='first', inplace=True)
# clearAdresse.reset_index()
#
# geolocator = Nominatim(user_agent="my-application")
# from geopy.extra.rate_limiter import RateLimiter
# geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
# df['Coordonnées'] = clearAdresse.apply(lambda x : utils.getFullAdress(x))
# outputsCSV = df['Coordonnées'].to_csv('outputs/coordos.csv', encoding='utf-16', index=False, header=True, sep='\t')

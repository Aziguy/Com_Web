# Mes importations
from tqdm.auto import tqdm

import Utilities as utils

# Récupération des adresses des zones DNS
tqdm.pandas()
# df = pd.read_csv('outputs/zoneDNS.csv', encoding='utf-16', sep='\t')
# df['DNSSource2'] = df['DNS Source'].progress_apply(lambda x: utils.getFullAdress(x))

# Visualisation des zone DNS sur la carte
# monFichier = 'outputs/fullAdressesZoneDNS.csv'
# utils.showMapFromAdress(monFichier)

# Visualisation des zones DNS en mode choropleth
monCSV = 'datasets/ZoneDNSFullAdressesZoneDNS.csv'
monGeoJson = 'datasets/communes-83-var.geojson'
utils.showChoroplethFromAdress(monCSV, monGeoJson)
# Lecture du fichier csv
# df = pd.read_csv('datasets/Index-réseau.csv', encoding='utf-16', sep='\t')
# df['Complémentaire'] = df['DNS Source'].progress_apply(lambda x : utils.getFullAdress(x))
# print(df['Complémentaire'].head(3))

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

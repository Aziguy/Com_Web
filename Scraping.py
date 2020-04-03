# Mes importations
import pandas as pd

import Utilities as utils

df = pd.read_csv('outputs/zoneDNS.csv', encoding='utf-16', sep='\t')
df['DNSSource2'] = df['DNS Source'].apply(lambda x: utils.getFullAdress(x) if x else None)
# Lecture du fichier csv
# df = pd.read_csv('datasets/Acteurs-csv-test.csv', encoding='utf-8', sep=';')
# df['Complémentaire'] = df['Acteurs '].apply(lambda x : utils.getFullAdress(x))
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
'''
daf = pd.DataFrame({'name': ['paris', 'berlin', 'london']})
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="specify_your_app_name_here")
from geopy.extra.rate_limiter import RateLimiter

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
daf['location'] = daf['name'].apply(geocode)
#
# daf['point'] = daf['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# print(daf)

'''

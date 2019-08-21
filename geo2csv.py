import argparse

import pandas as pd
import geopy.geocoders as geo
from geopy.extra.rate_limiter import RateLimiter

parser = argparse.ArgumentParser(description="Geolocates places in a Excel file.")
parser.add_argument('excel_file', help="name of the Excel file serving as input")
parser.add_argument('-c', '--column', default='Ort', help="column of the table containing places")
parser.add_argument('csv_file', help="name of the output CSV file")

args = parser.parse_args()

geolocator = geo.Nominatim(user_agent='Itinerar')
geo.options.default_timeout = 10

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

print("Lade die Datei {}...".format(args.excel_file))
df = pd.read_excel(args.excel_file, parse_dates=True)

print("Erstelle die Geodaten")
df['GeoData'] = df[args.column].apply(geolocator.geocode)

df['Latitude'] = df['GeoData'].apply(lambda x: x.latitude if x else None)
df['Longitude'] = df['GeoData'].apply(lambda x: x.longitude if x else None)

print("Speichere die CSV-Datei {}...".format(args.csv_file))
df.to_csv(args.csv_file)

import pandas as pd
import numpy as np
import requests
import json
import time
import os

final_data = set()
coordinates = ['42.3601', '-71.0589']
keywords = [
    'Allston',
    'Back Bay',
    'Brookline',
    'Beacon Hill',
    'Chinatown',
    'Dorchester',
    'Downtown',
    'Fenway',
    'Kenmore',
    'Jamaica Plain',
    'North End',
    'Waterfront',
    'Seaport',
]

cuisines = ["American", "Chinese", "Mediterranean", "Greek", "Indian", "Italian", "Japanese", "Korean", "Mexican", "Thai", "Vietnamese"]

queries = []

for keyword in keywords:
    for cuisine in cuisines:
        queries.append(f"{cuisine} restaurants in {keyword}")

radius = '5000'
api_key = os.getenv('API_KEY')

if api_key is None:
    print('You must provide an API key as an environment variable to the program, like API_KEY="$API_KEY" ./main.py')
    exit(1)

for i, keyword in enumerate(queries):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+coordinates[0] + ',' + coordinates[1] +'&radius='+str(radius)+'&keyword='+str(keyword)+'&key='+str(api_key)
    while True:
        print(url)
        respon = requests.get(url)
        jj = json.loads(respon.text)
        print(jj)
        results = jj['results']
        for result in results:
            name = result.get('name', 'unknown name')
            place_id = result.get('place_id', 'unknown_place_id')
            rating = result.get('rating', '2.5')
            rating_count = result.get('user_ratings_total', '0')
            types = tuple(sorted(result.get('types', [])))
            vicinity = result.get('vicinity', 'Unknown Address')
            price_level = result.get('price_level', 'Unknown')
            data = (name, place_id, rating, rating_count, types, vicinity, price_level)
            final_data.add(data)
        if 'next_page_token' not in jj:
            break
        else:
            next_page_token = jj['next_page_token']
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key='+str(api_key)+'&pagetoken='+str(next_page_token)
            time.sleep(2)


export_dataframe_1_medium = pd.DataFrame.from_records(list(final_data))
export_dataframe_1_medium.to_csv('more_restaurants_in_boston.csv')

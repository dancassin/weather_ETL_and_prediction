import datetime
import json
import os
from datetime import timezone

import requests
from dotenv import load_dotenv

load_dotenv()

satellite_api_token = os.getenv("weather_api_key")  # same api key as weather data
# print(f'satellite_api_token: {satellite_api_token}')
san_diego_polygon = os.getenv(
    "san_diego_polygon"
)  # unique id for created polygon manually saved to .env
# print(f'polygon: {san_diego_polygon}')

current_datetime = datetime.datetime.now()
current_UTC = int(current_datetime.replace(tzinfo=timezone.utc).timestamp())
# print(f'current time: {current_UTC}')
days = datetime.timedelta(15)
start_date_UTC = int((current_datetime - days).replace(tzinfo=timezone.utc).timestamp())
# print(f'start_date: {start_date_UTC}')


def create_geographic_polygon(api_token):
    """
    ****ONLY RUN THIS FCN ONCE: >2500ha RESULTS IN CHARGES*****
    - sends post request to argomonitoring.com to create polygon
    - only needs to be run once per polygon
    - resulting JSON contains identification
    """
    load_dotenv()

    api_address = f"http://api.agromonitoring.com/agro/1.0/polygons?appid={api_token}"

    body = {
        "name": "san_diego",
        "geo_json": {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-117.26648, 32.75699],
                        [-117.26648, 32.79852],
                        [-117.21169, 32.79852],
                        [-117.21169, 32.75699],
                        [-117.26648, 32.75699],
                    ]
                ],
            },
        },
    }

    headers = {"Content-Type": "application/json"}

    json_data = requests.post(
        api_address, data=json.dumps(body), headers=headers
    ).json()

    filename = "san_diego_polygon_info"

    filepath = f"data_cache/{filename}.json"

    with open(filepath, "w") as json_file:
        json.dump(json_data, json_file)

    return json_data


def get_satellite_image_from_API(api_token, polygon, start_date, end_date):

    api_address = f"http://api.agromonitoring.com/agro/1.0/image/search?start={start_date}&end={end_date}&polyid={polygon}&appid={api_token}"

    satellite_json = requests.get(api_address).json()

    return satellite_json

from dotenv import load_dotenv
import os
import requests
import json

def create_geographic_polygon():
    '''
    ****ONLY RUN THIS FCN ONCE: >2500ha RESULTS IN CHARGES*****
    - sends post request to argomonitoring.com to create polygon
    - only needs to be run once per polygon
    - resulting JSON contains 
    '''
    load_dotenv()

    api_token = os.getenv('weather_api_key') #same api key as weather data
    api_address = f'http://api.agromonitoring.com/agro/1.0/polygons?appid={api_token}'

    body = {
        "name": "san_diego",
        "geo_json":{
            "type":"Feature",
            "properties":{},
            "geometry":{
                "type":"Polygon",
                "coordinates":[
                    [
                        [-117.26648,32.75699],
                        [-117.26648,32.79852],
                        [-117.21169,32.79852],
                        [-117.21169,32.75699],
                        [-117.26648,32.75699]
                    ]
                ]
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    json_data = requests.post(api_address, data=json.dumps(body), headers=headers).json()

    filename = f"san_diego_polygon_info"

    filepath = f'data_cache/{filename}.json'

    with open(filepath, 'w') as json_file:
        json.dump(json_data, json_file)

    return json_data
from dotenv import load_dotenv
import os
import requests
import json
import datetime

api_token = os.getenv('weather_api_key') #same api key as weather data
san_diego_polygon = os.getenv('san_diego_polygon') #unique id for created polygon manually saved to .env

current_datetime = datetime.now() # convert to UTC
five_days_ago = datetime.now() - 0 #need to do the math for 3 days and convert to UTC

def create_geographic_polygon(api_token):
    '''
    ****ONLY RUN THIS FCN ONCE: >2500ha RESULTS IN CHARGES*****
    - sends post request to argomonitoring.com to create polygon
    - only needs to be run once per polygon
    - resulting JSON contains identification
    '''
    load_dotenv()

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

def get_satellite_image_from_API(api_token, polygon):
    
    api_address = f'http://api.agromonitoring.com/agro/1.0/image/search?start={start date}&end={end date}&polyid={polygon}&appid={api_token}'
    pass
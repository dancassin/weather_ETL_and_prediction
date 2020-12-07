from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
from datetime import datetime


#1690158 - San Diego, CA
def get_weather_data_from_OpenWeatherMap(city_id):
    '''
    - returns current weather by city id
    - saves json file named by unix timestamp
    '''
    load_dotenv()

    api_address = 'http://api.openweathermap.org/data/2.5/weather?'
    api_token = os.getenv('weather_api_key')

    json_data = requests.get(f"{api_address}id={city_id}&appid={api_token}").json()

    filename = f"weather_data_{str(json_data['dt'])}"

    filepath = f'data_cache/{filename}.json'

    with open(filepath, 'w') as json_file:
        json.dump(json_data, json_file)

    return filepath


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


def json_to_df(filename):
    ''' open JSON and convert to pandas df
    '''
    with open(filename, 'r') as JSON:
        json_dict = json.load(JSON)
        df = pd.json_normalize(json_dict)
    return df


def kelvin_to_farenheit_calc(kelvin):
    farenheit = ((kelvin-273.15)*(9/5)) + 32
    return farenheit


def transform_df(df):
    df.weather = pd.json_normalize(df['weather'][0][0])['description'][0] # gets short description from sub dictionary
    columns_to_keep = df[['weather', 'visibility', 'dt', 'name','coord.lon','coord.lat',
                        'main.temp','main.feels_like','main.temp_min','main.temp_max',
                        'main.pressure','main.humidity','wind.speed','wind.deg','clouds.all',
                        'sys.sunrise','sys.sunset'
                        ]].copy()
    
    columns_to_keep.rename(columns = {'coord.lon':'lon', 'coord.lat':'lat', 'main.temp':'temp', 
                                    'main.feels_like':'feels_like', 'main.temp_min':'temp_min',
                                    'main.temp_max':'temp_max', 'main.pressure':'pressure',
                                    'main.humidity':'humidity', 'wind.speed':'wind_speed',
                                    'wind.deg':'wind_deg', 'clouds.all':'cloudiness_pct',
                                    'sys.sunrise':'dt_sunrise', 'sys.sunset':'dt_sunset'
                                    }, inplace=True)
    
    columns_to_convert = ['temp', 'feels_like', 'temp_min','temp_max']
    
    columns_to_keep[columns_to_convert] = \
        columns_to_keep[columns_to_convert].apply(kelvin_to_farenheit_calc) # converting kelvin to farenheit
    

    columns_to_keep['date'] = datetime.fromtimestamp(columns_to_keep['dt']).strftime('%Y-%m-%d')
    columns_to_keep['dt_sunrise'] = datetime.fromtimestamp(columns_to_keep['dt_sunrise']).strftime('%H:%M:%S')
    columns_to_keep['dt_sunset'] = datetime.fromtimestamp(columns_to_keep['dt_sunset']).strftime('%H:%M:%S')

    columns_to_keep['date'] = columns_to_keep['date'].apply(pd.to_datetime, format='%Y-%m-%d')

    columns_to_keep.set_index('dt', drop=True,inplace=True)

    return columns_to_keep

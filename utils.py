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

def get_soil_data():
    load_dotenv()

    api_address = 'http://api.agromonitoring.com/agro/1.0/soil?'
    api_token = os.getenv('weather_api_key')
    poly_id = os.getenv('san_diego_polygon')

    json_data = requests.get(f"{api_address}polyid={poly_id}&appid={api_token}").json()

    soil_df = pd.json_normalize(json_data)
    soil_df.drop(labels='dt', axis=1, inplace=True)

    return soil_df


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


def concat_weather_and_soil(weather_df, soil_df):
    final_df = pd.concat([weather_df, soil_df], axis=1)
    return final_df


def transform_weather_df(df):
    df.weather = pd.json_normalize(df['weather'][0][0])['description'][0] # gets short description from sub dictionary
    columns_to_keep = df[['weather', 'visibility', 'dt', 'name','coord.lon','coord.lat',
                        'main.temp','main.feels_like','main.temp_min','main.temp_max',
                        'main.pressure','main.humidity','wind.speed','wind.deg','clouds.all',
                        'sys.sunrise','sys.sunset', 't10','moisture','t0'
                        ]].copy()
    
    columns_to_keep.rename(columns = {'coord.lon':'lon', 'coord.lat':'lat', 'main.temp':'temp', 
                                    'main.feels_like':'feels_like', 'main.temp_min':'temp_min',
                                    'main.temp_max':'temp_max', 'main.pressure':'pressure',
                                    'main.humidity':'humidity', 'wind.speed':'wind_speed',
                                    'wind.deg':'wind_deg', 'clouds.all':'cloudiness_pct',
                                    'sys.sunrise':'dt_sunrise', 'sys.sunset':'dt_sunset',
                                    't10':'10_centi_soil_depth_temp', 'moisture':'soil_moisture', 
                                    't0':'soil_surface_temp', 
                                    }, inplace=True)
    
    columns_to_convert = ['temp', 'feels_like', 'temp_min','temp_max', '10_centi_soil_depth_temp',
                        'soil_surface_temp']
    
    columns_to_keep[columns_to_convert] = \
        columns_to_keep[columns_to_convert].apply(kelvin_to_farenheit_calc) # converting kelvin to farenheit
    

    columns_to_keep['date'] = datetime.fromtimestamp(columns_to_keep['dt']).strftime('%Y-%m-%d')
    columns_to_keep['dt_sunrise'] = datetime.fromtimestamp(columns_to_keep['dt_sunrise']).strftime('%H:%M:%S')
    columns_to_keep['dt_sunset'] = datetime.fromtimestamp(columns_to_keep['dt_sunset']).strftime('%H:%M:%S')

    columns_to_keep['date'] = columns_to_keep['date'].apply(pd.to_datetime, format='%Y-%m-%d')

    columns_to_keep.set_index('dt', drop=True,inplace=True)

    return columns_to_keep
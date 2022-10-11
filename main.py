# from satellite_image_utils import ...
import argparse

from utils import (
    concat_weather_and_soil,
    get_soil_data,
    get_weather_data_from_OpenWeatherMap,
    json_to_df,
    transform_weather_df,
)
from weather_sql_db import close_db_connection, create_db_connection, update_db

parser = argparse.ArgumentParser()
parser.add_argument(
    "--city_id",
    default="1690158",
    help="Fetch weather data for specified city. ID can be found on OpenWeatherMap.org",
)
args = parser.parse_args()


def get_weather_data():
    """
    full program
    """
    returned_connection = create_db_connection()
    filename = get_weather_data_from_OpenWeatherMap(args.city_id)
    weather_df = json_to_df(filename)
    soil_df = get_soil_data()
    merged_df = concat_weather_and_soil(weather_df, soil_df)
    df_transfomed = transform_weather_df(merged_df)

    update_db(df_transfomed, returned_connection)

    close_db_connection(returned_connection)


def get_satellite_image_data():
    pass


if __name__ == "__main__":
    get_weather_data()

import sqlite3


def create_db_connection():
    """connect to db and create cursor obj for executing SQL statements"""
    connection = sqlite3.connect("WeatherAndSoilDB.db", uri=True)
    print("Connection with database established")
    connection.cursor()
    return connection


def close_db_connection(connection):
    """close connection w/ db"""
    connection.commit()
    connection.close()


def update_db(pandas_df, connection):
    """upload pandas df to sql db"""
    pandas_df.to_sql("weather", connection, if_exists="append", index=True)
    print("Uploaded to Database")

from spotify_api import SpotifyAPI
import pandas as pd
import sqlite3
import logging
from create_db import create_database
import os
from dotenv import load_dotenv
import boto3
import botocore.exceptions
from io import StringIO

load_dotenv()

def extract_spotify_data(client_id, client_secret, user_id):
    spotify_api = SpotifyAPI(client_id, client_secret, user_id)

    # Tables list:
    track_data = []
    artist_data = []
    album_data = []
    playlist_data = []

    # Get user data
    user_item = spotify_api.get_user_data()

    # Extract user_name from user_item
    user_name = user_item.get("display_name", "")  # Assuming display_name is available in user_data

    user_dict = {
        "user_name": user_name,
        "user_id": user_id
    }

    user_data = [user_dict]

    # Get playlists 
    playlist_item = spotify_api.get_playlists()

    if playlist_item:
        for item in playlist_item:
            # Playlist information
            playlist_id = item['id']
            playlist_name = item['name']

            playlist_dict = {
                "playlist_id": playlist_id,
                "user_id": user_id,
                "playlist_name": playlist_name
            }
            playlist_data.append(playlist_dict)

            # Get tracks for each playlist
            tracks_item = spotify_api.get_playlist_tracks(playlist_id)

            for i in tracks_item:
                track_id = i['track']['id']
                track_name = i['track']['name']
                artist_id = i["track"]["artists"][0].get("id")
                artist_name = i["track"]["artists"][0].get("name")
                album_id = i["track"]["album"].get("id")
                album_name = i["track"]["album"].get("name")

                track_dict = {
                    "track_id": track_id,
                    "playlist_id": playlist_id,
                    "artist_id": artist_id,
                    "album_id": album_id,
                    "track_name": track_name
                }

                artist_dict = {
                    "artist_id": artist_id,
                    "artist_name": artist_name
                }

                album_dict = {
                    "album_id": album_id,
                    "album_name": album_name
                }

                track_data.append(track_dict)
                artist_data.append(artist_dict)
                album_data.append(album_dict)
                
            # Log the number of tracks found for each playlist
            logging.info(f"Playlist {playlist_id} has {len(tracks_item)} tracks.")
    else:
        logging.info("No playlists found.")

    return user_data, playlist_data, track_data, album_data, artist_data


def transform_data(track_data, artist_data, album_data, playlist_data, user_data):
    track_df = pd.DataFrame(track_data).rename(
        columns={"track_id": "id", "playlist_id": "playlist_id", "artist_id": "artist_id", "album_id": "album_id",
                 "track_name": "name"})
    artist_df = pd.DataFrame(artist_data).rename(columns={"artist_id": "id", "artist_name": "name"})
    album_df = pd.DataFrame(album_data).rename(columns={"album_id": "id", "album_name": "name"})
    playlist_df = pd.DataFrame(playlist_data).rename(
        columns={"playlist_id": "id", "user_id": "user_id", "playlist_name": "name"})
    user_df = pd.DataFrame(user_data).rename(columns={"user_id": "id", "user_name": "name"})
    return user_df, playlist_df, track_df, album_df, artist_df


def check_duplicates_and_missing_values(track_df, artist_df, album_df, playlist_df, user_df):
    for df, name in [(track_df, "track"), (artist_df, "artist"), (album_df, "album"), (playlist_df, "playlist"),
                     (user_df, "user")]:
        duplicate_entries = df[df.duplicated()]
        if not duplicate_entries.empty:
            logging.warning(f"Duplicate {name} found. Duplicates will be removed.")
            df.drop_duplicates(inplace=True)

        if df.isnull().values.any():
            logging.warning(f"Missing values found in {name} data. Please handle missing values appropriately.")


def load_data_to_database(user_df, playlist_df, track_df, album_df, artist_df, db_path):
    try:
        conn = sqlite3.connect(db_path)
        user_df.to_sql('user', conn, if_exists='replace', index=False)
        playlist_df.to_sql('playlist', conn, if_exists='replace', index=False)
        track_df.to_sql('track', conn, if_exists='replace', index=False)
        album_df.to_sql('album', conn, if_exists='replace', index=False)
        artist_df.to_sql('artist', conn, if_exists='replace', index=False)
    except sqlite3.Error as e:
        logging.error(f"An error occurred during data insertion: {e}", exc_info=True)
    else:
        logging.info("Data loaded to SQLite successfully.")


def upload_to_s3(df, key, folder_name='', aws_access_key=None, aws_secret_key=None, aws_region=None, aws_s3_bucket_name=None):
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        if aws_access_key and aws_secret_key and aws_region and aws_s3_bucket_name:
            s3_client = boto3.client(
                service_name='s3',
                region_name=aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )

            # Concatenate folder_name and key to form the full S3 object key
            full_key = f"{folder_name}/{key}" if folder_name else key

            s3_client.put_object(Body=csv_buffer.getvalue(), Bucket=aws_s3_bucket_name, Key=full_key)

            logging.info(f"Data successfully uploaded to AWS S3 with key: {full_key}")
        else:
            raise ValueError("AWS credentials are missing. Data not uploaded to AWS S3.")
    except botocore.exceptions.NoCredentialsError:
        logging.error("AWS credentials are incorrect or missing. Please check your AWS access key and secret key.",
                      exc_info=True)
    except botocore.exceptions.ParamValidationError:
        logging.error("Invalid parameter value. Please check your AWS region or S3 bucket name.", exc_info=True)
    except Exception as e:
        logging.error(f"An error occurred during data upload to AWS S3: {e}", exc_info=True)
    finally:
        # Close the StringIO buffer to free up resources
        csv_buffer.close()

def etl_pipeline():
    try:
        # Check for required environment variables
        required_env_vars = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET', 'SPOTIFY_USER_ID', 'DB_PATH']
        for var in required_env_vars:
            if not os.getenv(var):
                raise EnvironmentError(f"Missing required environment variable: {var}")

        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        user_id = os.getenv('SPOTIFY_USER_ID')
        db_path = os.getenv('DB_PATH')

        aws_access_key = os.getenv('AWS_ACCESS_KEY')
        aws_secret_key = os.getenv('AWS_SECRET_KEY')
        aws_s3_bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        aws_region = os.getenv('AWS_REGION')

        # ETL Extract
        user_data, playlist_data, track_data, album_data, artist_data = extract_spotify_data(client_id, client_secret,
                                                                                             user_id)

        # ETL Transform
        user_df, playlist_df, track_df, album_df, artist_df = transform_data(track_data, artist_data, album_data,
                                                                             playlist_data, user_data)

        # Perform data validation checks
        check_duplicates_and_missing_values(track_df, artist_df, album_df, playlist_df, user_df)

        if aws_access_key and aws_secret_key and aws_s3_bucket_name:
            # ETL Load to AWS S3
            upload_to_s3(user_df, 'user.csv', 'csv-files', aws_access_key, aws_secret_key, aws_region, aws_s3_bucket_name)
            upload_to_s3(playlist_df, 'playlist.csv', 'csv-files', aws_access_key, aws_secret_key, aws_region, aws_s3_bucket_name)
            upload_to_s3(track_df, 'track.csv', 'csv-files', aws_access_key, aws_secret_key, aws_region, aws_s3_bucket_name)
            upload_to_s3(album_df, 'album.csv', 'csv-files', aws_access_key, aws_secret_key, aws_region, aws_s3_bucket_name)
            upload_to_s3(artist_df, 'artist.csv', 'csv-files', aws_access_key, aws_secret_key, aws_region, aws_s3_bucket_name)

            logging.info("Data uploaded to AWS S3 successfully.")
        else:
            # ETL Load to SQLite
            create_database(db_path)  # Ensure the database is created before loading data
            load_data_to_database(user_df, playlist_df, track_df, album_df, artist_df, db_path)

            logging.info("Data loaded to SQLite successfully.")
    except EnvironmentError as e:
        logging.error(f"Error with environment variables: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"An error occurred during ETL Pipeline: {e}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    etl_pipeline()

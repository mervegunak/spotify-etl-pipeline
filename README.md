# Spotify ETL Pipeline
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline for retrieving data from the Spotify API, transforming it, and loading it into a SQLite database. The pipeline includes scripts for interacting with the Spotify API, creating a database schema, and orchestrating the ETL process.

## Prerequisites
Before using these scripts, ensure you have the following prerequisites:

- A Spotify account
- Spotify API client ID and secret. To obtain these, create a Spotify Developer account, create a new application, and retrieve the client ID and secret from the application dashboard.
- Install the required packages by running:

  ```bash
  pip install -r requirements.txt
  
## File Structure
The project is organized with the following files:

- **.env**: This file contains environment variables for the Spotify API client ID, client secret, user ID, and database path.
- **create_db.py**: This script is responsible for creating the SQLite database schema. It defines tables for users, playlists, tracks, albums, and artists.
- **spotify_api.py**: Module providing a class (`SpotifyAPI`) that handles authentication and makes requests to the Spotify API. It includes methods to fetch user data, playlists, and track details.
- **main.py**: Main script orchestrating the ETL process, including extraction, transformation, and loading of data.
- **LICENSE**: The license file for the project.
- **README.md**: Project documentation providing an overview, setup instructions, and contribution guidelines.
- **requirements.txt**: File listing the required Python packages and their versions.

## How to Run
1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/spotify-etl-pipeline.git
   cd spotify-etl-pipeline
   
2. Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   
3. Create a .env file with your Spotify API credentials and database information:

   ```bash
   SPOTIFY_CLIENT_ID="your_client_id"
   SPOTIFY_CLIENT_SECRET="your_client_secret"
   SPOTIFY_USER_ID="your_user_id"
   DB_PATH="your_db_name"

4. Run the ETL pipeline:

       python3 main.py
   
After running main.py, the ETL pipeline will fetch user data, playlist details, track information, and seamlessly load them into the SQLite database for further exploration and analysis. 

## Optional: Upload Data to AWS S3 Bucket with Boto3

I've added an option to upload data to your AWS S3 Bucket using the `upload_to_s3` function.

Just, **add your AWS S3 credentials to your `.env` file:**

   (If you don't provide this information, the script will use only your Spotify credentials and SQLite database options.)
   
      
       AWS_ACCESS_KEY="your_aws_access_key"
       AWS_SECRET_KEY="your_aws_secret_key"
       AWS_S3_BUCKET_NAME="your_s3_bucket_name"
       AWS_REGION="your_aws_region"
     
Run the ETL pipeline:

       python3 main.py

That's all! Just provide AWS S3 credentials. 

Then this script will fetch user, playlist, track data via Spotify API and upload them to your specified folder in your AWS S3 Bucket. If you do not provide these credentials, your data will be uploaded to the SQLite database.


Medium blog post is on the way !!

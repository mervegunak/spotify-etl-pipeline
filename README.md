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
  
# File Structure
The project is organized with the following files:

- **.env**: This file contains environment variables for the Spotify API client ID, client secret, user ID, and database path.
- **create_db.py**: Python script for creating the SQLite database schema.
- **spotify_api.py**: Module providing a class (`SpotifyAPI`) for interacting with the Spotify API.
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

   ```bash
    python3 main.py
   
After running main.py, the ETL pipeline will fetch user data, playlist details, track information, and seamlessly load them into the SQLite database for further exploration and analysis. 

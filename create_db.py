import sqlite3
import logging

def create_database(db_path='spotify_data.db'):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Table Definitions (aligned for consistency)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playlist (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    name TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS track (
                    id TEXT PRIMARY KEY,
                    playlist_id TEXT,
                    artist_id TEXT,
                    album_id TEXT,
                    name TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS album (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS artist (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )
            ''')

            conn.commit()
            cursor.close()

    except sqlite3.Error as e:
        logging.error(f"Error creating database: {e}", exc_info=True)

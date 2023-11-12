import base64
import requests
import logging

class SpotifyAPI:
    """A class for interacting with the Spotify API."""

    SPOTIFY_API_URL = "https://api.spotify.com/v1/"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    USER_ENDPOINT = "users"
    PLAYLISTS_ENDPOINT = "playlists"
    TRACKS_ENDPOINT = "tracks"

    def __init__(self, client_id, client_secret, user_id):
        """Initialize the SpotifyAPI instance."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_id = user_id
        self.access_token = self._get_access_token()

    def _get_request(self, url, headers):
        """Make a GET request to the specified URL."""
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _get_auth_headers(self):
        """Get the headers for authenticating with Spotify."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}

    def _get_access_token(self):
        """Get the access token for Spotify API authentication."""
        headers = self._get_auth_headers()
        data = {"grant_type": "client_credentials"}
        try:
            response = requests.post(self.TOKEN_URL, headers=headers, data=data,
                                     auth=(self.client_id, self.client_secret))
            response.raise_for_status()
            token = response.json().get("access_token")
            if token is None:
                logging.warning("Access token is None. Response content: %s", response.content)
            return token
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting access token: {e}")
            return None

    def _authenticated_request(self, endpoint):
        """Make an authenticated request to the Spotify API."""
        url = f"{self.SPOTIFY_API_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        return self._get_request(url, headers)

    def get_user_data(self):
        """Get user data for the specified user ID."""
        return self._authenticated_request(f"{self.USER_ENDPOINT}/{self.user_id}")

    def get_playlists(self):
        """Get playlists for the specified user ID."""
        return self._authenticated_request(f"{self.USER_ENDPOINT}/{self.user_id}/{self.PLAYLISTS_ENDPOINT}")["items"]

    def get_playlist_tracks(self, playlist_id):
        """Get tracks for the specified playlist ID."""
        return self._authenticated_request(f"{self.PLAYLISTS_ENDPOINT}/{playlist_id}/{self.TRACKS_ENDPOINT}")["items"]

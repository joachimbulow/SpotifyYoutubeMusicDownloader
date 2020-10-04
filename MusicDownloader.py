import requests
import base64
import json
import youtube_dl
import tempfile


class MusicDownloader:

    @staticmethod
    def get_spotify_token():
        # Authenticating the application in Spotify
        client_credentials = "YOUR SPOTIFY CLIENT CREDENTIALS"
        client_credentials_in_bytes = client_credentials.encode("utf-8")
        encoded_client_credentials = base64.b64encode(client_credentials_in_bytes)
        headers = {"Authorization": "Basic " + encoded_client_credentials.decode("utf-8"),
                   'content-type': 'application/x-www-form-urlencoded'}
        payload = {"grant_type": "client_credentials"}
        authorization_response = requests.post('https://accounts.spotify.com/api/token', params=payload, headers=headers)
        return json.loads(authorization_response.text)["access_token"]

    @staticmethod
    def get_playlist_content(playlist_id):
        # playlist_id = playlist_link[34:56]
        token = MusicDownloader.get_spotify_token()
        # Retrieving playlist information
        headers = {"Authorization": "Bearer " + token}
        playlist_response = requests.get("https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks", headers=headers)
        tracks = json.loads(playlist_response.text)["items"]

        # Making the json that the front end needs
        track_list = []
        for track in tracks:
            name = track["track"]["name"]
            artist = track["track"]["artists"][0]["name"]
            track_list.append({"name": name, "artist": artist})

        return track_list

    @staticmethod
    # Refactor this to use beautiful_soup
    def get_top_video_id(name, artist):
        print("Calling youtube api")
        # Getting the top video's ID from the YouTube Data API
        youtube_videos = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=' + name + " " + artist + " lyrics" + '&key=YOUR YOUTUBE API KEY', headers={"Accept": "application/json"}).text
        video_id = json.loads(youtube_videos)["items"][0]["id"]["videoId"]
        return video_id









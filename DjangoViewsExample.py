# Create your views here.

import json
import youtube_dl
import tempfile
import io
from django.http import FileResponse
from django.http import HttpResponse
from .MusicDownloader import MusicDownloader

def get_playlist_content(request, playlist_id):
    if request.method == 'GET':
        try:
            content = MusicDownloader.MusicDownloader.get_playlist_content(playlist_id)
            response = json.dumps(content)
        except:
            response = json.dumps([{'Error': 'An error occurred while getting the playlist information'}])

        return HttpResponse(response, content_type='text/json')


def get_song(request, name, artist):
    if request.method == 'GET':
        try:
            song_video_id = MusicDownloader.MusicDownloader.get_top_video_id(name, artist)
            # Using temporary directory for the mp3, to save storage on disc
            temp = tempfile.TemporaryDirectory()
            temp_path = temp.name.replace("\\", "/")
            song_path = temp_path + "/" + song_video_id + ".mp3"
            ydl_opts = {
                'outtmpl': song_path,
                'format': 'bestaudio/best'
            }
            yt = youtube_dl.YoutubeDL(ydl_opts)
            yt.download(["https://www.youtube.com/watch?v=" + song_video_id])
            song = open(song_path, "rb")
            song_buffer = io.BytesIO(song.read())
            song.close()
            # File response is a a streaming http response subclass which means it streams the song.
            # (See django documentation)
            response = FileResponse(song_buffer)
            return response


        except Exception as e:
            response = json.dumps([{'Error': 'An error eccoured when fetching the song.' + e}])

        return HttpResponse(response, content_type='text/json')
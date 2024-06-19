import os
from django.http import JsonResponse
from ..models import Music, Artist, Album, Genre, MusicSerializer
from uuid import uuid4
from .filesystem.utils import get_metadata
from rest_framework.views import APIView
import json
from mutagen import MutagenError
from django.db import Error

MUSIC_PATH = "/music"
# Audio file extensions
AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg"]


def get_tree(path, level):
    """
    edge cases :
        * Not handling hidden files / folders
        * Not following symlinks (os.scandir)
        * Large directories may cause out of memory or timeout. use pagination and limit size...

    """
    tree = {
        "name": os.path.normpath(path).split(os.sep)[-1],
        "path": path,
        "folders": [],
        "musics": [],
        "opened": False,
    }
    for p in os.listdir(path):
        p_path = os.path.join(path, p)
        if level > 0:
            if os.path.isdir(p_path):
                tree["folders"].append(get_tree(p_path, level - 1))
            elif (
                os.path.isfile(p_path)
                and os.path.splitext(p_path)[1] in AUDIO_EXTENSIONS
            ):
                existing_music = Music.objects.filter(path=p_path)
                if not existing_music:
                    music_result = updateDb(p, p_path)
                else:
                    music_result = {"music": existing_music.first()}
                if music_result["music"]:
                    music_dict = MusicSerializer(music_result["music"]).data
                    music_result["music"] = music_dict
                tree["musics"].append(music_result)
    return tree


# TODO endpoint for scanning in background


class FolderView(APIView):
    def post(self, request):
        try:
            path = None
            if request.body:
                body = json.loads(request.body)
                path = body["path"]
            tree = get_tree(path if path else MUSIC_PATH, 1)
            # json_tree = json.dumps(tree, ensure_ascii=False)  # TODO check non-ASCII characters serialization
            return JsonResponse(tree)  # safe=False
        except Exception as e:
            return JsonResponse({"error": str(e)})


def updateDb(music_name: str, music_path: str):
    genre = None
    artist = None
    album = None
    music_result = {"music": None}
    try:
        metadata = get_metadata(music_path)
        if metadata.genre:
            genre, created = Genre.objects.get_or_create(name=metadata.genre)
        if metadata.artist:
            artist, created = Artist.objects.get_or_create(name=metadata.artist)
        if metadata.album:
            temp_album = Album(
                name=metadata.album,
                artist=artist,
                genre=genre,
                date=metadata.album_release_date,
            )
            existing_albums = Album.objects.filter(name=metadata.album, artist=artist)
            if not existing_albums:
                temp_album.save()
                album = temp_album
            else:
                album = existing_albums.first()
        music = Music(name=music_name, path=music_path, artist=artist, album=album)
        music.set_checksum()
        existing_music = Music.objects.filter(checksum=music.checksum)
        if not existing_music:
            music.bpm = metadata.bpm
            music.duration = metadata.track_duration
            music.track = metadata.track_number
            music.save()
        music_result["music"] = Music.objects.filter(checksum=music.checksum).first()
    except (MutagenError, Error, Exception) as err:
        print(err)
        music_result["music"] = Music(name=music_name, path=music_path)
        music_result["error"] = str(err)
    return music_result

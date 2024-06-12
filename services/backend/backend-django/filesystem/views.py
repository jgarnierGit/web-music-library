import os
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Music, Artist, Album, MusicSerializer
from uuid import uuid4

MUSIC_PATH = "/music"
# Audio file extensions
AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg", ".flac"]


def get_tree(path, level):
    """
    edge cases :
        * Not handling hidden files / folders
        * Not following symlinks (os.scandir)
        * Large directories may cause out of memory or timeout. use pagination and limit size...

    """
    tree = {
        "id": path + str(level),
        "name": os.path.normpath(path).split(os.sep)[-1],
        "path": path,
        "folders": [],
        "musics": [],
    }
    for p in os.listdir(path):
        p_path = os.path.join(path, p)
        if os.path.isdir(p_path) and level > 1:
            tree["folders"].append(get_tree(p_path, level - 1))
        elif os.path.isfile(p_path) and os.path.splitext(p_path)[1] in AUDIO_EXTENSIONS:
            music = updateDb(p, p_path, "fake_artist", "fake_album")
            tree["musics"].append(MusicSerializer(music).data)
    return tree


def get_tree_at(request, path=None):
    try:
        tree = get_tree(path if path else MUSIC_PATH, 2)
        # json_tree = json.dumps(tree, ensure_ascii=False)  # TODO check non-ASCII characters serialization
        return JsonResponse(tree)  # safe=False
    except Exception as e:
        return JsonResponse({"error": str(e)})


def updateDb(music_name: str, music_path: str, artist_name: str, album_name: str):
    artist, created = Artist.objects.get_or_create(name=artist_name)
    album, created = Album.objects.get_or_create(name=album_name, artist=artist)
    music = Music(name=music_name, path=music_path, artist=artist, album=album)
    music.set_checksum()
    existing_music = Music.objects.filter(checksum=music.checksum)
    if not existing_music:
        music.save()
    existing_music = Music.objects.filter(checksum=music.checksum).first()
    return existing_music


class IncrementMusicPlayedView(APIView):
    def post(self, request, item_id):
        try:
            music = Music.objects.get(id=item_id)
            music.count_played += 1
            music.save()
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(MusicSerializer(music).data)

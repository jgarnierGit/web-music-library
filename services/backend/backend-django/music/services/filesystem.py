from music.api_views.filesystem.utils import get_metadata
from ..models import Music, Artist, Album, Genre
from mutagen import MutagenError
from django.db import Error


def updateDb(music_name: str, music_path: str, force_update=False):
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
        if not existing_music or force_update:
            music.bpm = metadata.bpm
            music.duration = metadata.track_duration
            music.track = metadata.track_number
            music.save()
            music_result["saved"] = True
        music_result["music"] = Music.objects.filter(checksum=music.checksum).first()
    except (MutagenError, Error, Exception) as err:
        print(err)
        music_result["music"] = Music(name=music_name, path=music_path)
        music_result["error"] = str(err)
    return music_result

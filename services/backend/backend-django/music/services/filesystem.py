from music.api_views.filesystem.utils import get_metadata
from ..models import Music, Artist, Album, Genre
from mutagen import MutagenError
from django.db import Error
from typing import List
from itertools import chain


class BulkMusicData:
    def __init__(self, music: Music, genres: List[Genre]):
        self.music = music
        self.genres = genres


def get_model_to_save(music_name: str, music_path: str):
    artist = None
    album = None
    has_created_album = False
    has_created_artist = False
    created_genres = []
    genres = []
    try:
        metadata = get_metadata(music_path)
        has_genre = len(metadata.genre) > 0
        if has_genre:
            existing_genres = Genre.objects.filter(name__in=metadata.genre)
            existing_genre_names = [g.name for g in existing_genres]
            for g in metadata.genre:
                if g not in existing_genre_names:
                    genre = Genre(name=g)
                    genres.append(genre)
            created_genres = Genre.objects.bulk_create(
                [g for g in genres], ignore_conflicts=True
            )
            genres = list(Genre.objects.filter(name__in=metadata.genre))

        if metadata.artist:
            artist, has_created_artist = Artist.objects.get_or_create(
                name=metadata.artist
            )
            if has_genre:
                if has_created_artist:
                    artist.genres.set(genres)
                else:
                    artist.genres.set(list(chain(artist.genres.all(), genres)))

        if metadata.album:
            album, has_created_album = Album.objects.get_or_create(
                name=metadata.album,
                artist=artist,
            )
            if has_created_album:
                album.date = metadata.album_release_date
                album.save()
            if has_genre:
                if has_created_album:
                    album.genres.set(genres)
                else:
                    album.genres.set(list(chain(album.genres.all(), genres)))

        music = Music(name=music_name, path=music_path, artist=artist, album=album)
        music.set_checksum()
        music.bpm = metadata.bpm
        music.duration = metadata.track_duration
        music.track = metadata.track_number
        bulk_music = BulkMusicData(music=music, genres=genres)
        return {"music": bulk_music}
    except (MutagenError, Error, Exception) as err:
        print(f"{music_path} {str(err)}")
        return None


def update_bulk_music_db(musics_data: List[BulkMusicData], force_update=False):
    musics_result = []
    processed_musics = []
    if not force_update:
        for index, music_data in enumerate(musics_data):
            existing_music = Music.objects.filter(checksum=music_data.music.checksum)
            if existing_music:
                music_data.remove(index)
    try:
        created_musics = Music.objects.bulk_create(
            [music_data.music for music_data in musics_data], ignore_conflicts=True
        )
        processed_musics += created_musics
        if force_update:
            existing_musics = Music.objects.filter(
                checksum__in=[music_data.music.checksum for music_data in musics_data]
            )
            for e_music in existing_musics:
                e_genre = [
                    music_data.genres
                    for music_data in musics_data
                    if music_data.music.checksum == e_music.checksum
                    and len(music_data.genres) > 0
                ]
                if len(e_genre) > 0:
                    e_music.genres.set(e_genre[0])
            Music.objects.bulk_update(existing_musics)
            processed_musics += list(existing_musics)
        else:
            for c_music in created_musics:
                c_genres = [
                    music_data.genres
                    for music_data in musics_data
                    if music_data.music.checksum == c_music.checksum
                    and len(music_data.genres) > 0
                ]
                if len(c_genres) > 0:
                    c_music.genres.set(c_genres[0])
    except (Error, Exception) as err:
        print(f" {str(err)}")
        return None
    musics_result = [{"music": m, "saved": True} for m in processed_musics]
    return musics_result

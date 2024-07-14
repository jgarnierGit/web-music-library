from music.models import Artist, Genre, Album
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg


def get_albums_cards(limit: int, offset: int, filters=[]):
    query = (
        Album.objects.all().annotate(
            tracks_count=Count("FK_MUSIC_ALBUM", distinct=True),
        )
        # .prefetch_related("genres")
    )
    for filter in filters:
        match filter["type"]:
            case _:
                pass

    return query[offset : offset + limit]


def get_artists_cards(limit: int, offset: int, filters=[]):
    query = (
        Artist.objects.all().annotate(
            tracks_count=Count("FK_MUSIC_ARTIST", distinct=True),
            albums_count=Count("FK_ALBUM_ARTIST", distinct=True),
        )
        # .prefetch_related("genres")
    )
    for filter in filters:
        match filter["type"]:
            case "geom":
                query = get_geom_filter(query, filter)

    return query[offset : offset + limit]


def get_genres_cards(limit: int, offset: int, filters=[]):
    query = Genre.objects.all().annotate(
        artists_count=Count("artist", distinct=True),
        dates=ArrayAgg("album__date", distinct=True),
    )

    for filter in filters:
        match filter["type"]:
            case _:
                pass

    return query[offset : offset + limit]


def get_geom_filter(artists_query, filter):
    if not filter.get("value", None):
        pass
    elif filter["value"] == "ACTIVE_GEOM_FILTER":
        artists_query = artists_query.filter(geom__isnull=False)
    elif filter["value"] == "ACTIVE_NO_GEOM_FILTER":
        artists_query = artists_query.filter(geom__isnull=True)
    return artists_query

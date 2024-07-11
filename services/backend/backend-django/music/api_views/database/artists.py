from music.models import Artist, Genre, Album
from django.db.models import Count, Prefetch
from django.contrib.postgres.aggregates import ArrayAgg


def get_artists_cards(limit: int, offset: int, filters=[]):
    artists_query = (
        Artist.objects.all()
        .annotate(
            tracks_count=Count("FK_MUSIC_ARTIST", distinct=True),
            albums_count=Count("FK_ALBUM_ARTIST", distinct=True),
        )
        .prefetch_related("genres")
    )
    for filter in filters:
        match filter["type"]:
            case "geom":
                artists_query = get_geom_filter(artists_query, filter)

    return artists_query[offset : offset + limit]


def get_geom_filter(artists_query, filter):
    if not filter["value"]:
        pass
    elif filter["value"] == "ACTIVE_GEOM_FILTER":
        artists_query = artists_query.filter(geom__isnull=False)
    elif filter["value"] == "ACTIVE_NO_GEOM_FILTER":
        artists_query = artists_query.filter(geom__isnull=True)
    return artists_query

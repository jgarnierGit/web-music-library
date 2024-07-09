from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import (
    Music,
    Artist,
    MusicSerializer,
    ArtistSerializer,
    ArtistCardSerializer,
)
from django.contrib.gis.geos import GEOSGeometry
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from random import choice
from django.db.models import Count
from django.db.models import Q


class IncrementMusicPlayedView(APIView):
    def post(self, request, item_id):
        try:
            music = Music.objects.get(id=item_id)
            music.count_played += 1
            music.save()
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(MusicSerializer(music).data)


class ArtistsListView(APIView):
    def get(self, request):
        limit = request.query_params.get("limit", 10)
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                return Response(
                    {"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST
                )
        offset = request.query_params.get("offset", 0)
        if offset:
            try:
                offset = int(offset)
            except ValueError:
                return Response(
                    {"error": "Invalid offset value"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        artists = Artist.objects.all().annotate(
            tracks_count=Count("FK_MUSIC_ARTIST", distinct=True),
            albums_count=Count("FK_ALBUM_ARTIST", distinct=True),
        )[offset : offset + limit]
        return JsonResponse(
            {"artists": [ArtistCardSerializer(artist).data for artist in artists]}
        )

    def post(self, request):
        artist_param = request.data
        if artist_param:
            offset = artist_param.get("offset", 0)
            limit = artist_param.get("limit", 10)
            artists_query = Artist.objects.all().annotate(
                tracks_count=Count("FK_MUSIC_ARTIST", distinct=True),
                albums_count=Count("FK_ALBUM_ARTIST", distinct=True),
            )
            for filter in artist_param.get("filters", []):
                match filter["type"]:
                    case "geom":
                        if not filter["value"]:
                            pass
                        elif filter["value"] == "ACTIVE_GEOM_FILTER":
                            artists_query = artists_query.filter(geom__isnull=False)
                        elif filter["value"] == "ACTIVE_NO_GEOM_FILTER":
                            artists_query = artists_query.filter(geom__isnull=True)
        artists_res = artists_query[offset : offset + limit]
        return JsonResponse(
            {"artists": [ArtistCardSerializer(artist).data for artist in artists_res]}
        )


class ArtistUpdateView(APIView):
    def put(self, request, artist_id):
        artist = Artist.objects.get(id=artist_id)
        artist_data = request.data
        if artist_data["geom"]:
            artist.geom = GEOSGeometry(str(artist_data["geom"]))
            del artist_data["geom"]
        serializer = ArtistSerializer(artist, data=artist_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_GET
def artist_count(request):
    count_artists = Artist.objects.count()
    print(count_artists)
    return JsonResponse({"result": count_artists})


@require_GET
def artist_geoms(request):
    artists_with_geoms = Artist.objects.filter(geom__isnull=False)
    return JsonResponse(
        {"result": [ArtistSerializer(artist).data for artist in artists_with_geoms]}
    )


@require_GET
def music_count(request):
    count_musics = Music.objects.count()
    print(count_musics)
    return JsonResponse({"result": count_musics})


class PlaylistNextView(APIView):
    def post(self, request):
        music_filter = request.data
        if music_filter:
            match music_filter["filter"]["type"]:
                case "ARTIST":
                    musics_pk = Music.objects.filter(
                        artist__pk__in=music_filter["filter"]["targetIds"]
                    ).values_list("pk", flat=True)
                case "FOLDER":
                    if len(music_filter["filter"]["targetIds"]) == 1:
                        musics_pk = Music.objects.filter(
                            path__startswith=music_filter["filter"]["targetIds"][0]
                        ).values_list("pk", flat=True)
                    else:
                        print("multi folder filtering not implemented yet")
                case "COUNTRY":
                    musics_pk = Music.objects.filter(
                        artist__country_name__in=music_filter["filter"]["targetIds"]
                    ).values_list("pk", flat=True)
                case _:
                    print("unknown filter, or empty filter, fallback to full random")
                    musics_pk = Music.objects.values_list("pk", flat=True)
        else:
            musics_pk = Music.objects.values_list("pk", flat=True)
        # watch out perfs about loading the whole pk list in memory

        random_pk = choice(musics_pk)
        random_obj = Music.objects.get(pk=random_pk)
        return JsonResponse(MusicSerializer(random_obj).data)

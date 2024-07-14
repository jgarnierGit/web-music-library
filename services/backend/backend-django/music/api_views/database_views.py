from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import (
    Music,
    Album,
    MusicSerializer,
)
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from random import choice
from django.db.models import Count
from .database.db_artists_views import *
from .database.db_albums_views import *
from .database.db_genres_views import *


class IncrementMusicPlayedView(APIView):
    def post(self, request, item_id):
        try:
            music = Music.objects.get(id=item_id)
            music.count_played += 1
            music.save()
        except Music.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(MusicSerializer(music).data)


@require_GET
def music_count(request):
    count = Music.objects.count()
    return JsonResponse({"result": count})


@require_GET
def year_count(request):
    count = Album.objects.all().values("date").annotate(total=Count("date")).count()
    return JsonResponse({"result": count})


class PlaylistNextView(APIView):
    def post(self, request):
        music_filter = request.data
        if music_filter:
            match music_filter["filter"]["type"]:
                case "ARTIST":
                    musics_pk = Music.objects.filter(
                        artist__pk__in=music_filter["filter"]["targetIds"]
                    ).values_list("pk", flat=True)
                case "ALBUM":
                    musics_pk = Music.objects.filter(
                        album__pk__in=music_filter["filter"]["targetIds"]
                    ).values_list("pk", flat=True)
                case "COUNTRY":
                    musics_pk = Music.objects.filter(
                        artist__country_name__in=music_filter["filter"]["targetIds"]
                    ).values_list("pk", flat=True)
                case "FOLDER":
                    if len(music_filter["filter"]["targetIds"]) == 1:
                        musics_pk = Music.objects.filter(
                            path__startswith=music_filter["filter"]["targetIds"][0]
                        ).values_list("pk", flat=True)
                    else:
                        print("multi folder filtering not implemented yet")
                case "GENRE":
                    musics_pk = Music.objects.filter(
                        genres__pk__in=music_filter["filter"]["targetIds"]
                    ).values_list("pk", flat=True)
                case "YEAR":
                    musics_pk = Music.objects.filter(
                        album__date__in=music_filter["filter"]["targetIds"]
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

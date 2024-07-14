from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from music.models import (
    Artist,
    ArtistUpdaterSerializer,
    ArtistSerializer,
    ArtistCardSerializer,
)
from django.contrib.gis.geos import GEOSGeometry
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .requests import get_artists_cards
from .commons import extract_get_params_cards, extract_post_params_cards


class ArtistsListView(APIView):
    def get(self, request):
        limit, offset = extract_get_params_cards(request)
        contents = get_artists_cards(limit=limit, offset=offset)
        serialized_cards = ArtistCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})

    def post(self, request):
        limit, offset, filters = extract_post_params_cards(request)
        contents = get_artists_cards(limit=limit, offset=offset, filters=filters)
        serialized_cards = ArtistCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})


class ArtistView(APIView):
    def put(self, request, artist_id):
        artist = Artist.objects.get(id=artist_id)
        artist_data = request.data
        if artist_data["geom"]:
            artist.geom = GEOSGeometry(str(artist_data["geom"]))
            del artist_data["geom"]
        serializer = ArtistUpdaterSerializer(artist, data=artist_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_GET
def artist_count(request):
    count = Artist.objects.count()
    return JsonResponse({"result": count})


@require_GET
def artist_geoms(request):
    artists_with_geoms = Artist.objects.filter(geom__isnull=False)
    return JsonResponse(
        {"result": [ArtistSerializer(artist).data for artist in artists_with_geoms]}
    )

from rest_framework.response import Response
from rest_framework.views import APIView
from music.models import Album, AlbumCardSerializer, YearCardSerializer
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .requests import get_albums_cards, get_years_cards
from .commons import extract_get_params_cards, extract_post_params_cards


@require_GET
def album_count(request):
    count = Album.objects.count()
    return JsonResponse({"result": count})


class AlbumsListView(APIView):
    def get(self, request):
        limit, offset = extract_get_params_cards(request)
        contents = get_albums_cards(limit=limit, offset=offset)
        serialized_cards = AlbumCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})

    def post(self, request):
        limit, offset, filters = extract_post_params_cards(request)
        contents = get_albums_cards(limit=limit, offset=offset, filters=filters)
        serialized_cards = AlbumCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})


class YearsListView(APIView):
    def get(self, request):
        limit, offset = extract_get_params_cards(request)
        contents = get_years_cards(limit=limit, offset=offset)
        serialized_cards = YearCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})

    def post(self, request):
        limit, offset, filters = extract_post_params_cards(request)
        contents = get_years_cards(limit=limit, offset=offset, filters=filters)
        serialized_cards = YearCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})

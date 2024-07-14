from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from music.models import Genre, GenreCardSerializer
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .requests import get_genres_cards
from .commons import extract_get_params_cards, extract_post_params_cards


@require_GET
def genre_count(request):
    count = Genre.objects.count()
    return JsonResponse({"result": count})


class GenresListView(APIView):
    def get(self, request):
        limit, offset = extract_get_params_cards(request)
        contents = get_genres_cards(limit=limit, offset=offset)
        serialized_cards = GenreCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})

    def post(self, request):
        limit, offset, filters = extract_post_params_cards(request)
        contents = get_genres_cards(limit=limit, offset=offset, filters=filters)
        serialized_cards = GenreCardSerializer(contents, many=True).data
        return Response({"contents": serialized_cards})

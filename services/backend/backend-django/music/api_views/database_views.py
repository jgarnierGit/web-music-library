from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Music, Artist, MusicSerializer, ArtistSerializer
from django.views.decorators.http import require_GET
from django.http import JsonResponse


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
        artists = Artist.objects.all()
        return JsonResponse(
            {"artists": [ArtistSerializer(artist).data for artist in artists]}
        )


class ArtistUpdateView(APIView):
    def put(self, request, artist_id):
        artist = Artist.objects.get(id=artist_id)
        serializer = ArtistSerializer(artist, data=request.data)
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

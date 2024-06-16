import os
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
import musicbrainzngs

MAIL = os.environ.get("API_HEADER_MAIL")
APP_VERSION = os.environ.get("APP_VERSION")
APP_NAME = os.environ.get("APP_NAME")


def configure_musicbrainz():
    if not MAIL:
        return HttpResponse("API header mail is required", status=403)

    musicbrainzngs.set_useragent(APP_NAME, APP_VERSION, contact=MAIL)
    musicbrainzngs.set_format(fmt="json")
    musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)


class ArtistCountryView(APIView):
    def get(self, request, artist_name):
        configure_musicbrainz()
        # Search for the artist, returning 25 results by default.
        search_data = musicbrainzngs.search_artists(
            query=f"artist:{artist_name}", limit=1, offset=None, strict=True
        )
        country = (
            "UNKNOWN"
            if search_data["count"] == 0
            else search_data["artists"][0]["country"]
        )
        return JsonResponse({"artist_name": artist_name, "country": country})

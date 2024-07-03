import os
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
import musicbrainzngs
from unidecode import unidecode

MAIL = os.environ.get("API_HEADER_MAIL")
APP_VERSION = os.environ.get("APP_VERSION")
APP_NAME = os.environ.get("APP_NAME")


def configure_musicbrainz():
    print(f"MAIL={MAIL}")
    if not MAIL or MAIL.strip() == "":
        raise ValueError("API header mail is required")

    musicbrainzngs.set_useragent(APP_NAME, APP_VERSION, contact=MAIL)
    musicbrainzngs.set_format(fmt="json")
    musicbrainzngs.set_rate_limit(limit_or_interval=1.0, new_requests=1)


def get_matching_countries(search_data, artist_name):
    strict_match = {
        artist.get("country", None)
        for artist in search_data["artists"]
        if "country" in artist and artist["name"].lower() == artist_name.lower()
    }
    if len(strict_match) > 0:
        return strict_match
    partial_match = {
        artist.get("country", None)
        for artist in search_data.get("artists", [])
        if "country" in artist
        and all(
            word in unidecode(artist["name"].lower())
            for word in unidecode(artist_name.lower()).split()
        )
    }
    return partial_match


class ArtistCountryView(APIView):
    def get(self, request, artist_name):
        try:
            configure_musicbrainz()
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=403)
        # Search for the artist, returning 25 results by default.
        search_data = musicbrainzngs.search_artists(
            query=f"artist:{artist_name}", limit=None, offset=None, strict=True
        )
        match_result = get_matching_countries(search_data, artist_name)
        return JsonResponse({"result": list(match_result)})

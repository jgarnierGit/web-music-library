from django.test import TestCase
from music.api_views.external_views import get_matching_countries


class TestGetMatchingCountries(TestCase):
    def test_get_matching_countries(self):
        search_data = {
            "artists": [
                {"name": "Beethoven", "country": "Germany"},
                {"name": "Saint-Saëns", "country": "France"},
                {"name": "Jean-Sébastien Bach", "country": "Germany"},
                {"name": "Mozart"},
            ]
        }

        # exact matching
        self.assertEqual(get_matching_countries(search_data, "Beethoven"), {"Germany"})

        # Partial matching
        self.assertEqual(get_matching_countries(search_data, "bach"), {"Germany"})

        # complex partial matching
        self.assertEqual(get_matching_countries(search_data, "saint saens"), {"France"})

        # Test with no matching artists
        self.assertEqual(get_matching_countries(search_data, "mozart"), set())

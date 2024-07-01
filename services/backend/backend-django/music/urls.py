from django.urls import path

from . import views

urlpatterns = [
    path("folder/list", views.FolderView.as_view(), name="get_folder_content"),
    path(
        "music/<str:item_id>/increment/",
        views.IncrementMusicPlayedView.as_view(),
        name="increment_played",
    ),
    path(
        "music/getRandom",
        views.PlaylistNextView.as_view(),
        name="get_next_music_random",
    ),
    path(
        "artist/<str:artist_name>/getCountry",
        views.ArtistCountryView.as_view(),
        name="get_artist_country",
    ),
    path("artist/list", views.ArtistsListView.as_view(), name="get_artists"),
    path("artist/count", views.artist_count, name="get_count_artists"),
    path(
        "artist/<str:artist_id>",
        views.ArtistUpdateView.as_view(),
        name="artist_update",
    ),
]

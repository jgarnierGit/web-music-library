from django.urls import path

from . import views

urlpatterns = [
    path("albums/count", views.album_count, name="get_count_albums"),
    path("albums/list", views.AlbumsListView.as_view(), name="get_albums"),
    path(
        "artist/<str:artist_id>",
        views.ArtistView.as_view(),
        name="artist_update",
    ),
    path(
        "artist/<str:artist_name>/getCountry",
        views.ArtistCountryView.as_view(),
        name="get_artist_country",
    ),
    path("artists/count", views.artist_count, name="get_count_artists"),
    path("artists/list", views.ArtistsListView.as_view(), name="get_artists"),
    path("folders/list", views.FolderView.as_view(), name="get_folder_content"),
    path("folders/refresh", views.refresh_library, name="get_refresh_job"),
    path("genres/count", views.genre_count, name="get_count_genres"),
    path("genres/list", views.GenresListView.as_view(), name="get_genres"),
    path("job/<str:job_id>", views.JobView.as_view(), name="job_manager"),
    path("map/getGeometries", views.artist_geoms, name="get_artists_with_geoms"),
    path(
        "music/<str:item_id>/increment/",
        views.IncrementMusicPlayedView.as_view(),
        name="increment_played",
    ),
    path("musics/count", views.music_count, name="get_count_musics"),
    path(
        "musics/getRandom",
        views.PlaylistNextView.as_view(),
        name="get_next_music_random",
    ),
    path("years/count", views.year_count, name="get_count_years"),
    path("years/list", views.YearsListView.as_view(), name="get_years"),
]

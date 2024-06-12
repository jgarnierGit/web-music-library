from django.urls import path

from . import views

urlpatterns = [
    path("list", views.get_tree_at, name="get_tree_at"),
    path(
        "music/<str:item_id>/increment/",
        views.IncrementMusicPlayedView.as_view(),
        name="increment_played",
    ),
]

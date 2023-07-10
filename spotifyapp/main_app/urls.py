from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("artist/", views.artist_index, name="artist"),
    path("artist/<int:artist_id>/", views.artist_detail, name='artist_detail'),
    path("artist/create/", views.ArtistCreate.as_view(), name='artist_create'),
    path("song/create/", views.SongCreate.as_view(), name='song_create'),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("artist/", views.artist_index, name="artist"),
    path("artist/<int:artist_id>/", views.artist_detail, name='artist_detail'),
    path("artist/create/", views.ArtistCreate.as_view(), name='artist_create'),
    path("song/create/", views.SongCreate.as_view(), name='song_create'),
    path("playlist/create/", views.PlaylistCreate.as_view(), name='playlist_create'),
    path("playlist/<int:playlist_id>/", views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk>/delete', views.PlaylistDelete.as_view(), name='playlist_delete'),
    path('<int:playlist_id>/assoc_song/<int:song_id>/', views.assoc_song, name="assoc_song"),
    path('<int:playlist_id>/unassoc_song/<int:song_id>/', views.unassoc_song, name="unassoc_song"),
    path('accounts/signup/', views.signup, name='signup'),
]
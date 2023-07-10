from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("artist/", views.artist_index, name="artist"),
    path("artist/<int:artist_id>/", views.artist_detail, name='artist_detail')
]
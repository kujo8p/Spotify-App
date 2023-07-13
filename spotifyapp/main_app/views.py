import os
import uuid
from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .models import Artist, Song, Playlist, User
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    playlists = Playlist.objects.all()
    return render(request, "home.html", {'playlists': playlists})

def about(request):
    return render(request, "about.html")

def artist_index(request):
  artists = Artist.objects.all()
  return render(request, "artist/index.html", {'artists': artists})

def artist_detail(request, artist_id):
    artist = Artist.objects.get(id=artist_id)
    songs = Song.objects.all()
    return render(request, 'artist/detail.html', {
        'artist': artist, 'songs': songs
    })

def playlist_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    return render (request, 'playlist/detail.html', {
      'playlist': playlist
    })

def assoc_song(request, playlist_id, song_id):
    Playlist.objects.get(id=playlist_id).songs.add(song_id)
    return redirect('home', playlist_id=playlist_id)

class ArtistCreate(CreateView):
    model = Artist
    fields = ["name", "genre"]


class PlaylistCreate(CreateView):
    model = Playlist
    fields = ["title", "description"]
    success_url = ""

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


class SongCreate(CreateView):
    model = Song
    fields = ["name", "album"]

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# class AuthURL(APIView):
#   def get(self, request, format=None):
#     scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-read user-read-private'

#     url = Request('GET', 'https://accounts.spotify.com/authorize', params={
#       'scope': scopes,
#       'response_type': 'code',
#       'redirect_uri': REDIRECT_URI,
#       'client_id': CLIENT_ID
#     }).prepare().url

#     return Response({'url': url}, status=status.HTTP_200_OK)

# def spotify_callback(request, format=None):
#   code = request.GET.get('code')
#   error = request.GET.get('error')

#   response = post('https://accounts.spotify.com/api/token', data={
#     'grant_type': 'authorization_code',
#     'code': code,
#     'redirect_uri': REDIRECT_URI,
#     'client_id': CLIENT_ID,
#     'client_secret': CLIENT_SECRET
#   }).json()

#   access_token = response.get('access_token')
#   token_type = response.get('token_type')
#   refresh_token = response.get('refresh_token')
#   expires_in = response.get('expires_in')
#   error = response.get('error')
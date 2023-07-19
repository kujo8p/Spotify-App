import os
import uuid
from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from .models import Artist, Song, Playlist, User
from django.views.generic.edit import CreateView, DeleteView
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
    print(artist_id)
    artist = Artist.objects.get(id=artist_id)
    songs = Song.objects.all()
    return render(request, 'artist/detail.html', {
        'artist': artist, 'songs': songs
    })

def playlist_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    current_songs = playlist.songs.all().values_list('id')
    availible_songs = Song.objects.exclude(id__in=current_songs)
    return render (request, 'playlist/detail.html', {
      'playlist': playlist, 'availible_songs': availible_songs
    })

@login_required
def assoc_song(request, playlist_id, song_id):
    Playlist.objects.get(id=playlist_id).songs.add(song_id)
    return redirect('playlist_detail', playlist_id=playlist_id)

@login_required
def unassoc_song(request, playlist_id, song_id):
  Playlist.objects.get(id=playlist_id).songs.remove(song_id)
  return redirect('playlist_detail', playlist_id=playlist_id)

class ArtistCreate(LoginRequiredMixin, CreateView):
    model = Artist
    fields = ["name", "genre"]


class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ["title", "description"]
    success_url = ""

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


class PlaylistDelete(LoginRequiredMixin, DeleteView):
    model = Playlist
    success_url = "/"


class SongCreate(LoginRequiredMixin, CreateView):
    model = Song
    fields = ["name", "album", "artist"]

def searchBar(request):
  if request.method == 'GET':
    query = request.GET.get('query')
    if query:
      artists = Artist.objects.filter(name__icontains=query)
      return render(request, 'artist/searchbar.html', {'artists': artists})
    else:
      print("No Artist Found")
      return render(request, 'artist/searchbar.html', {})

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


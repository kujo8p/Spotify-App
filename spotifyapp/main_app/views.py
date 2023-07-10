import os
import uuid
from django.shortcuts import render
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .models import Artist, Song

def home(request):
    return render(request, "home.html")

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

class AuthURL(APIView):
  def get(self, request, format=None):
    scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-library-read user-read-private'

    url = Request('GET', 'https://accounts.spotify.com/authorize', params={
      'scope': scopes,
      'response_type': 'code',
      'redirect_uri': REDIRECT_URI,
      'client_id': CLIENT_ID
    }).prepare().url

    return Response({'url': url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
  code = request.GET.get('code')
  error = request.GET.get('error')

  response = post('https://accounts.spotify.com/api/token', data={
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
  }).json()

  access_token = response.get('access_token')
  token_type = response.get('token_type')
  refresh_token = response.get('refresh_token')
  expires_in = response.get('expires_in')
  error = response.get('error')
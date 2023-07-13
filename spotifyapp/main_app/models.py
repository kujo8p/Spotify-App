from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Artist(models.Model):
  name = models.CharField(max_length=50)
  genre = models.CharField(max_length=50)

  def __str__(self):
      return self.name

  def get_absolute_url(self):
      return reverse('artist_detail', kwargs={'artist_id': self.id})

class Song(models.Model):
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  album = models.CharField(max_length=50)

  def __str__(self):
      return self.name

class Playlist(models.Model):
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  songs = models.ManyToManyField(Song)

  def __str__(self):
      return self.title

  def get_absolute_url(self):
      return reverse('playlist_detail', kwargs={'playlist_id': self.id})
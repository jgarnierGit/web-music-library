import uuid
from django.contrib.gis.db import models
from django.db import migrations
from django.contrib.postgres.operations import CreateExtension
import hashlib
import os
from rest_framework import serializers

SCHEMA = '"library"'
MUSIC_PATH_MAX_LENGTH = os.environ.get("MUSIC_PATH_MAX_LENGTH", 500)


class Migration(migrations.Migration):
    operations = [CreateExtension("postgis")]


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()

    class Meta:
        db_table = f'{SCHEMA}."genre"'

    def __str__(self):
        return self.name


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    geom = models.PointField(srid=4326, null=True)

    class Meta:
        db_table = f'{SCHEMA}."artist"'

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="FK_ALBUM_ARTIST",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="FK_ALBUM_GENRE",
    )
    date = models.DateTimeField("date published", null=True)

    class Meta:
        db_table = f'{SCHEMA}."album"'

    def __str__(self):
        return self.name


class Music(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    path = models.TextField(max_length=MUSIC_PATH_MAX_LENGTH)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="FK_MUSIC_ARTIST",
        blank=True,
        null=True,
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="FK_MUSIC_ALBUM",
        blank=True,
        null=True,
    )
    track = models.IntegerField(default=0)
    duration = models.FloatField(default=0)
    bpm = models.IntegerField(null=True)
    last_played = models.DateTimeField("last time played song", null=True)
    count_played = models.IntegerField(default=0)
    count_skipped = models.IntegerField(default=0)
    checksum = models.TextField(null=True)

    class Meta:
        db_table = f'{SCHEMA}."music"'

    def __str__(self):
        return self.name

    def set_checksum(self):
        data = str(
            self.name
            + str(self.artist if self.artist.name else "")
            + str(self.album if self.album.name else "")
        )
        self.checksum = hashlib.sha256(data.encode()).hexdigest()


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):

    artist = ArtistSerializer(allow_null=True)
    album = AlbumSerializer(allow_null=True)

    class Meta:
        model = Music
        fields = "__all__"

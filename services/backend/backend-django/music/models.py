import uuid
from django.contrib.gis.db import models
from django.db import migrations
from django.contrib.postgres.operations import CreateExtension
import hashlib
import os
import json
from rest_framework import serializers

MUSIC_PATH_MAX_LENGTH = os.environ.get("MUSIC_PATH_MAX_LENGTH", 500)


class Migration(migrations.Migration):
    operations = [CreateExtension("postgis")]


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    last_played = models.DateTimeField("last time played genre", null=True)
    count_played = models.IntegerField(default=0)
    count_skipped = models.IntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint("name", name="unique_name_genre")]

    def __str__(self):
        return self.name


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    country_name = models.TextField(null=True)
    geom = models.PointField(
        srid=4326,
        null=True,
    )
    last_played = models.DateTimeField("last time played artist", null=True)
    count_played = models.IntegerField(default=0)
    count_skipped = models.IntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint("name", name="unique_name_artist")]

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
    date = models.IntegerField("Publication year", null=True)
    last_played = models.DateTimeField("last time played album", null=True)
    count_played = models.IntegerField(default=0)
    count_skipped = models.IntegerField(default=0)

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
    track = models.TextField(null=True)
    duration = models.FloatField(default=0)
    bpm = models.IntegerField(null=True)
    last_played = models.DateTimeField("last time played song", null=True)
    count_played = models.IntegerField(default=0)
    count_skipped = models.IntegerField(default=0)
    checksum = models.TextField(null=True)

    def __str__(self):
        return self.name

    def set_checksum(self):
        data = str(
            self.name
            + str(self.artist.name if self.artist else "")
            + str(self.album.name if self.album else "")
        )
        self.checksum = hashlib.sha256(data.encode()).hexdigest()


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"

    # overwrite geom serialization
    def to_representation(self, instance):
        data = {**instance.__dict__}
        # Remove the _state field from the data dictionary
        del data["_state"]
        # Serialize the geom field as a GeoJSON object
        if instance.geom:
            geom_dict = json.loads(instance.geom.geojson)
            data["geom"] = geom_dict

        return data


class ArtistNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["name"]


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):

    artist = ArtistNameSerializer(allow_null=True)
    # album = AlbumSerializer(allow_null=True)

    class Meta:
        model = Music
        fields = ["id", "name", "path", "artist"]

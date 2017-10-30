from django.db import models

# from taggit.managers import TaggableManager


class Genre(models.Model):
    name = models.CharField(max_length=150)


class Artist(models.Model):
    name = models.CharField(max_length=255)
    # tags = TaggableManager()

    lfm_id = models.CharField(max_length=36, db_index=True)


class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    release_date = models.DateField(default=None, null=True, blank=True)

    lfm_id = models.CharField(max_length=36, db_index=True)

    # tags = TaggableManager()


class Track(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    artist = models.ForeignKey('Artist', related_name='tracks')
    album = models.ForeignKey('Album', related_name='tracks', default=None, null=True, blank=True)
    genre_set = models.ManyToManyField('Genre', related_name='tracks')
    # tags = TaggableManager()

    lfm_id = models.CharField(max_length=36, default='', blank=True)





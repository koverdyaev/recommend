from django.conf import settings
from django.db import models
from django.utils.http import urlencode

import requests
from rest_framework.status import HTTP_200_OK
from retrying import retry

from apps.music.models import Track, Artist


class LastFMAccount(models.Model):
    user = models.OneToOneField('users.User', related_name='last_fm_account')
    username = models.CharField(max_length=50)

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def perform_request(self, **kwargs):
        kwargs.update({
            'api_key': settings.LFM_API_KEY,
            'format': 'json',
        })
        response = requests.get(settings.LFM_API_BASE_URL + urlencode(kwargs))
        if response.status_code != HTTP_200_OK:
            # TODO add custom exception classes
            # TODO check exception information
            raise Exception
        return response.json()

    def save_tracks(self, tracks):
        # TODO refactor to check tracks and artists of another providers
        # TODO add tags, albums and genres extraction
        db_tracks = []
        for track in tracks:
            db_track = Track.objects.filter(lfm_id=track['mbid']).first()
            if db_track is None:
                artist = track['artist']
                db_artist = Artist.objects.filter(lfm_id=artist['mbid']).first()
                if db_artist is None:
                    db_artist = Artist.objects.create(name=artist['name'], lfm_id=artist['mbid'])

                db_track = Track.objects.create(
                    artist=db_artist,
                    name=track['name'],
                    lfm_id=track['mbid']
                )
            db_tracks.append(db_track)
        self.user.tracks.add(*db_tracks)

    def fetch_all_user_tracks(self):
        kwargs = {
            'method': 'user.getlovedtracks',
            'user': self.username,
            'limit': 1000,  # 1000 is max
        }
        current_page = 1
        pages_count = 2

        # TODO: pylast library doesn't support pages, so you can't fetch more than 1000 user tracks.
        # But it is better to fork it and extend instead doing this.
        while current_page < pages_count:
            kwargs['page'] = current_page
            data = self.perform_request(**kwargs)
            tracks = data['lovedtracks']['track']
            self.save_tracks(tracks)

            current_page = data['@attr']['page']
            pages_count = data['@attr']['totalPages']

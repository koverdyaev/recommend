import json
import logging
import redis

from django.db import models
from django.db.models import Case, IntegerField, Sum, When

from apps.users.models import User
from apps.music.models import Track


logger = logging.getLogger(__name__)


class RedisConnection(models.Model):
    host = models.CharField(max_length=150)
    port = models.PositiveIntegerField()
    db = models.PositiveIntegerField()
    busy = models.BooleanField()

    def __init__(self, *args,  **kwargs):
        super().__init__(*args,  **kwargs)
        self._connection = None

    def get_connection(self):
        if self._connection is None:
            self._connection = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db,
            )
        return self._connection

    def clear_store(self):
        r = self.get_connection()
        r.flushdb()

    def mark_as_free(self):
        self.clear_store()
        self.busy = False
        self.save()


class AbstractRecommendationTable(models.Model):
    store = models.OneToOneField('RedisConnection')

    def refresh(self):
        new_store = self.get_free_connection()
        self.build(new_store)
        self.switch_connections(new_store)

    def get_free_connection(self):
        connection = RedisConnection.objects.filter(busy=False)[0]
        connection.busy = True
        connection.save()
        return connection

    def build(self, connection):
        raise NotImplementedError()

    def switch_connections(self, new_store):
        old_store = self.store
        self.store = new_store
        self.save()

        old_store.mark_as_free()

    def get_recommendation_list(self, key):
        try:
            r = self.store.get_connection()
            recommendations = r.get(key)
        except Exception:
            # TODO: add better message
            logger.error("Can't access storage", exc_info=True)
            recommendations = []
        return recommendations

    class Meta:
        abstract = True


class LibraryBasedTable(AbstractRecommendationTable):
    """Returns recommendations bases on user.id"""

    def build(self, connection):
        for user in User.objects.iterator():
            track_id_list = list(self.calculate_one_user(user))
            connection.set(user.pk, json.dumps(track_id_list))

    def get_similar_users(self, user, threshold=2, count=100):
        user_tracks = user.tracks.all()
        return set(User.objects.exclude(pk=user.pk).filter(tracks__in=user_tracks).distinct().annotate(
            score=Sum(
                Case(
                    When(tracks__in=user_tracks, then=1),
                    default=0, output_field=IntegerField()
                )
            )
        ).order_by('-score').filter(score__gte=threshold)[:count].values_list('id', flat=True))

    def get_similar_tracks(self, user, similar_users_ids, threshold=2, count=100):
        return Track.objects.exclude(user=user).filter(user__id__in=similar_users_ids).distinct().annotate(
            score=Sum(
                Case(
                    When(user__id__in=similar_users_ids, then=1),
                    default=0, output_field=IntegerField()
                )
            )
        ).filter(score__gte=threshold).order_by('-score')[:count]

    def calculate_one_user(self, user):
        similar_users = self.get_similar_users(user)
        similar_tracks = self.get_similar_tracks(user, similar_users)
        return similar_tracks


class GenreBasedTable(AbstractRecommendationTable):
    # TODO add build realization
    pass


class TagBasedTable(AbstractRecommendationTable):
    # TODO add build realization
    pass


class TrackBasedTable(AbstractRecommendationTable):
    # TODO add build realization
    pass


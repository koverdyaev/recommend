from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from apps.music.models import Track
from apps.taskapp.celery import fetch_lfm_user_tracks
from apps.recommendation_storage.models import LibraryBasedTable
from .serializers import LastFMAccountSerializer, TrackSerializer


# TODO: add registration/login views
# TODO: add pagination_class or check http://chibisov.github.io/drf-extensions/docs/#paginatebymaxmixin


class TrackListView(ListAPIView):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()


# TODO: replace UserTrack's views with one viewset
class UserTrackListView(ListAPIView):
    serializer_class = TrackSerializer

    def get_queryset(self):
        return self.request.user.tracks.all()


class AddUserTrackView(DestroyAPIView):
    """Add track to a user's library"""
    serializer_class = TrackSerializer
    queryset = Track.objects.all()

    def perform_create(self, instance):
        self.request.user.tracks.add(instance)


class RemoveUserTrackView(DestroyAPIView):
    """Remove track from a user's library"""
    serializer_class = TrackSerializer

    def get_queryset(self):
        return self.request.user.tracks.all()

    def perform_destroy(self, instance):
        self.request.user.tracks.remove(instance)


class SubmitLastFMAccount(CreateAPIView):
    serializer_class = LastFMAccountSerializer


class FetchLastFMLibraryView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            lfm_account = request.user.last_fm_account_id
        except ObjectDoesNotExist:
            raise ValidationError({'lfm_account': 'LastFM account doesn\'t exist'})

        # TODO: get job id to check result
        fetch_lfm_user_tracks.apply_async(args=(lfm_account,))
        return Response(status=HTTP_200_OK)


class GetLibraryRecommendationView(ListAPIView):
    serializer_class = TrackSerializer

    def get_queryset(self):
        table = LibraryBasedTable()
        track_ids = table.get_recommendation_list(self.request.user.pk)
        return Track.objects.filter(pk__in=track_ids)

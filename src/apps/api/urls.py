from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'signup/$', views.SignUpView.as_view()),
    # url(r'login/$', views.LoginView.as_view()),

    url(r'tracks/$', views.TrackListView.as_view()),

    url(r'submit-lfm/$', views.SubmitLastFMAccount.as_view()),
    url(r'fetch-lfm-library/$', views.FetchLastFMLibraryView.as_view()),

    url(r'user-tracks/$', views.UserTrackListView.as_view()),
    url(r'user-tracks/(?P<pk>\d+)/add/$', views.AddUserTrackView.as_view()),
    url(r'user-tracks/(?P<pk>\d+)/remove/$', views.RemoveUserTrackView.as_view()),

    url(r'get-library-recommendations/$', views.GetLibraryRecommendationView.as_view()),
]

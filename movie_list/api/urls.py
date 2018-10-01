from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MovieCreateView, MovieDetailsView, BucketCreateView, BucketDetailsView

urlpatterns = {
    # Movies
    url(r'^movies/$', MovieCreateView.as_view(), name="movie.create"),
    url(r'^movies/(?P<pk>[0-9]+)/$', MovieDetailsView.as_view(), name="movie.details"),
    # Buckets
    url(r'^buckets/$', BucketCreateView.as_view(), name="bucket.create"),
    url(r'^buckets/(?P<pk>[0-9]+)/$', BucketDetailsView.as_view(), name="bucket.details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
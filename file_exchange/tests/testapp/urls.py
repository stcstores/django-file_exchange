from django.conf.urls import re_path
from pytest_djangoapp.compat import get_urlpatterns

from . import views

urlpatterns = get_urlpatterns(
    [
        re_path(
            r"^file_download_status/(?P<pk>\d+)/$",
            views.ExtendedFileDownloadStatusView.as_view(),
            name="file_download_status",
        ),
    ]
)

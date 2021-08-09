from django.conf.urls import re_path
from pytest_djangoapp.compat import get_urlpatterns

from . import views

urlpatterns = get_urlpatterns(
    [
        re_path(
            r"^file_download_status/$",
            views.ExtendedFileDownloadStatusView.as_view(),
            name="file_download_status",
        ),
        re_path(
            r"^file_download_page/$",
            views.ExtendedDownloadFileView.as_view(),
            name="file_download_page",
        ),
    ]
)

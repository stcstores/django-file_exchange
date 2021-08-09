from file_exchange import views
from file_exchange.tests.testapp import models


class ExtendedFileDownloadStatusView(views.FileDownloadStatusView):
    model = models.ExtendedFileDownload


class ExtendedDownloadFileView(views.DownloadFileView):
    model = models.ExtendedFileDownload
    status_url = "status_url"
    create_file_url = "create_file_url"

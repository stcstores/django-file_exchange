from file_exchange import views
from file_exchange.tests.testapp import models


class ExtendedFileDownloadStatusView(views.FileDownloadStatusView):
    model = models.ExtendedFileDownload

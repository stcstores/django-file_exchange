import factory

from . import models


class ExtendedFileDownloadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ExtendedFileDownload

    name = factory.Sequence(lambda n: f"File Download {n}")
    status = models.ExtendedFileDownload.IN_PROGRESS
    created_at = None
    completed_at = None
    error_message = ""

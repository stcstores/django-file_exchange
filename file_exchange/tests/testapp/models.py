from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from file_exchange.models import FileDownload


class UnextendedFileDownload(FileDownload):
    pass


class ExtendedFileDownload(FileDownload):
    name = models.CharField(max_length=10)
    download_file = models.FileField(blank=True, null=True)

    @classmethod
    def generate_file(cls):
        return SimpleUploadedFile(name="test_file.txt", content=b"Hello, World!")


class FileDownloadWithFileCreationError(FileDownload):
    download_file = models.FileField(blank=True, null=True)

    @classmethod
    def generate_file(cls):
        raise Exception("TEST EXCEPTION")

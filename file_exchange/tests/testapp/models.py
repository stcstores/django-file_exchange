from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from file_exchange.models import FileDownload


class UnextendedFileDownload(FileDownload):
    pass


class ExtendedFileDownload(FileDownload):
    name = models.CharField(max_length=10)
    download_file = models.FileField(blank=True, null=True)

    def generate_file(self):
        return SimpleUploadedFile(name="test_file.txt", content=b"Hello, World!")


class FileDownloadWithFileCreationError(FileDownload):
    download_file = models.FileField(blank=True, null=True)

    def generate_file(self):
        raise Exception("TEST EXCEPTION")


class FileDownloadWithPreGenerationMethod(FileDownload):
    def generate_file(self):
        return SimpleUploadedFile(name="test_file.txt", content=b"Hello, World!")

    def pre_generation(self):
        pass


class FileDownloadWithPostGenerationMethod(FileDownload):
    def generate_file(self):
        return SimpleUploadedFile(name="test_file.txt", content=b"Hello, World!")

    def post_generation(self):
        pass

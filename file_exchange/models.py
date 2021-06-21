"""Models for the File Exchange app."""
from django.db import models

from file_exchange import tasks

IN_PROGRESS = "in_progress"
COMPLETE = "complete"
ERRORED = "errored"


class BaseFileExchangeManager(models.Manager):
    """Base class for file exchange managers."""

    pass


class FileDownloadManager(BaseFileExchangeManager):
    """Model Manager for file download models."""

    def create_download(self):
        """Create a missing information export."""
        instance = self.create()
        task = tasks.create_file_download.delay(
            app_label=self.model._meta.app_label,
            model_name=self.model._meta.model_name,
            instance_id=instance.id,
        )
        return task, instance


class BaseFileExchangeModel(models.Model):
    """Base class for file exchange models."""

    IN_PROGRESS = IN_PROGRESS
    COMPLETE = COMPLETE
    ERRORED = ERRORED

    STATUSES = (
        ("In Progress", IN_PROGRESS),
        ("Complete", COMPLETE),
        ("Errored", ERRORED),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default=IN_PROGRESS,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True)

    class Meta:
        """Meta class for file_exchange.BaseFileExchangeModel."""

        abstract = True


class FileDownload(BaseFileExchangeModel):
    """Base class for file download models."""

    objects = FileDownloadManager()

    class Meta:
        """Meta class for file_exchange.FileDownload."""

        abstract = True

    @classmethod
    def generate_file(cls):
        """Return the file to be downloaded."""
        raise NotImplementedError("Override...")

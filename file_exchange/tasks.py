"""Celery tasks for the File Exchange app."""

from typing import Type

from celery import shared_task
from django.apps import apps
from django.db import transaction
from django.utils import timezone

from file_exchange import models


@shared_task  # type: ignore
def create_file_download(app_label: str, model_name: str, instance_id: int) -> None:
    """Task for creating file downloads."""
    model: Type[models.FileDownload] = apps.get_model(app_label, model_name)
    download_instance: models.FileDownload = model.objects.get(id=instance_id)
    try:
        with transaction.atomic():
            download_instance.pre_generation()
        with transaction.atomic():
            generated_file = download_instance.generate_file()
            setattr(
                download_instance,
                download_instance.download_file_field_name,
                generated_file,
            )
        with transaction.atomic():
            download_instance.post_generation()
    except Exception as e:
        download_instance.status = download_instance.ERRORED
        download_instance.completed_at = timezone.now()
        download_instance.error_message = repr(e)
    else:
        download_instance.status = download_instance.COMPLETE
        download_instance.completed_at = timezone.now()
    finally:
        download_instance.save()

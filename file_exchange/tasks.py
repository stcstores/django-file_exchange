"""Celery tasks for the File Exchange app."""

from celery import shared_task
from django.apps import apps
from django.db import transaction
from django.utils import timezone


@shared_task
def create_file_download(app_label, model_name, instance_id):
    """Task for creating file downloads."""
    model = apps.get_model(app_label, model_name)
    download_instance = model.objects.get(id=instance_id)
    try:
        with transaction.atomic():
            download_instance.pre_generation()
        with transaction.atomic():
            download_instance.download_file = download_instance.generate_file()
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

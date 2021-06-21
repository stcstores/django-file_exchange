"""Celery tasks for the File Exchange app."""

from celery import shared_task
from django.apps import apps
from django.utils import timezone


@shared_task
def create_file_download(app_label, model_name, instance_id):
    """Task for creating file downloads."""
    model = apps.get_model(app_label, model_name)
    download_instance = model.objects.get(id=instance_id)
    try:
        download_instance.download_file = model.generate_file()
    except Exception as e:
        download_instance.status = download_instance.ERRORED
        download_instance.completed_at = timezone.now()
        download_instance.error_message = repr(e)
    else:
        download_instance.status = download_instance.COMPLETE
        download_instance.completed_at = timezone.now()
    finally:
        download_instance.save()

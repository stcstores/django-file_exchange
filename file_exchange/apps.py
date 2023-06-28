"""App config for the File Exchange app."""
from django.apps import AppConfig


class FileExchangeConfig(AppConfig):
    """App config for the File Exchange app."""

    default_auto_field = "django.db.models.BigAutoField"  # type: ignore
    name = "file_exchange"

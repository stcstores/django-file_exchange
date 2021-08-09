"""Templatetags for the django-file_exchange app."""

from typing import Any

from django import template

from file_exchange.models import BaseFileExchangeModel

register = template.Library()


@register.simple_tag
def file_exchange_status(file_exchange_instance: BaseFileExchangeModel) -> Any:
    """Return the status of a file exchange instance as a formatted string."""
    return file_exchange_instance.get_status_display()


@register.simple_tag
def file_exchange_created_at(file_exchange_instance: BaseFileExchangeModel) -> Any:
    """Return the date a file exchange instance was created as a string."""
    return file_exchange_instance.created_at.strftime("%Y-%m-%d %H:%M")

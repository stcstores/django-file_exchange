"""Celery tasks for the File Exchange app."""

import time

from celery import shared_task


def slow_task():
    """Slow function for testing celery."""
    time.sleep(10)


@shared_task
def test_task():
    """A task for testing celery."""
    slow_task()
    return "hello"

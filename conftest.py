import tempfile

from pytest_djangoapp import configure_djangoapp_plugin

MEDIA_DIR = tempfile.TemporaryDirectory()

pytest_plugins = ("celery.contrib.pytest",)
pytest_plugins = configure_djangoapp_plugin(
    {"MEDIA_ROOT": tempfile.mkdtemp(), "DEBUG": True},
    migrate=True,
)

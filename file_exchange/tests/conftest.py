import pytest
import pytest_factoryboy
from django.apps import apps

from file_exchange.tests.testapp import factories, models

pytest_factoryboy.register(factories.ExtendedFileDownloadFactory)


@pytest.fixture
def unextended_file_download_model():
    return models.UnextendedFileDownload


@pytest.fixture
def unextended_file_download_instance(unextended_file_download_model):
    return unextended_file_download_model.objects.create()


@pytest.fixture
def extended_file_download_model():
    return models.ExtendedFileDownload


@pytest.fixture
def extended_file_download_instance(extended_file_download_model):
    return extended_file_download_model.objects.create(name="Bilbo")


@pytest.fixture
def file_download_with_file_creation_error_model():
    return apps.get_model("testapp", "FileDownloadWithFileCreationError")


@pytest.fixture()
def file_download_instance_with_successful_file_creation(
    celery_session_worker, extended_file_download_model
):
    task, instance = extended_file_download_model.objects.create_download()
    task.get()
    instance.refresh_from_db()
    return instance


@pytest.fixture
def file_download_instance_with_errored_file_creation(
    celery_session_worker,
    file_download_with_file_creation_error_model,
):
    (
        task,
        instance,
    ) = file_download_with_file_creation_error_model.objects.create_download()
    task.get()
    instance.refresh_from_db()
    return instance

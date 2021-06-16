import datetime

import pytest
from django.apps import apps
from mock import patch

from file_exchange import models as file_exchange_models
from file_exchange import tasks


def test_test():
    assert True is not False


@pytest.fixture
def unextended_file_download_model():
    return apps.get_model("testapp", "UnextendedFileDownload")


@pytest.fixture
def unextended_file_download_instance(unextended_file_download_model):
    return unextended_file_download_model.objects.create()


@pytest.fixture
def extended_file_download_model():
    return apps.get_model("testapp", "ExtendedFileDownload")


@pytest.fixture
def extended_file_download_instance(extended_file_download_model):
    return extended_file_download_model.objects.create(name="Bilbo")


@pytest.fixture
def file_download_with_file_creation_error_model():
    return apps.get_model("testapp", "FileDownloadWithFileCreationError")


@pytest.fixture()
def file_download_instance_with_successfull_file_creation(extended_file_download_model):
    return extended_file_download_model.objects.create_download()


@pytest.fixture()
def file_download_instance_with_errored_file_creation(
    file_download_with_file_creation_error_model,
):
    return file_download_with_file_creation_error_model.objects.create_download()


def test_file_download_instance_has_IN_PROGRESS_attribute(
    extended_file_download_instance,
):
    assert (
        extended_file_download_instance.IN_PROGRESS == file_exchange_models.IN_PROGRESS
    )


def test_file_download_instance_has_COMLLETE_attribute(
    extended_file_download_instance,
):
    assert extended_file_download_instance.COMPLETE == file_exchange_models.COMPLETE


def test_file_download_instance_has_ERRORED_attribute(
    extended_file_download_instance,
):
    assert extended_file_download_instance.ERRORED == file_exchange_models.ERRORED


def test_file_download_instance_uses_file_download_manager(
    extended_file_download_model,
):
    assert isinstance(
        extended_file_download_model.objects, file_exchange_models.FileDownloadManager
    )


def test_file_download_instance_status_default_value(unextended_file_download_instance):
    assert unextended_file_download_instance.status == file_exchange_models.IN_PROGRESS


def test_file_download_instance_created_at_default_value(
    extended_file_download_instance,
):
    assert isinstance(extended_file_download_instance.created_at, datetime.datetime)


def test_file_download_instance_completed_at_default_value(
    extended_file_download_instance,
):
    assert extended_file_download_instance.completed_at is None


def test_extended_file_download_extra_field(extended_file_download_instance):
    assert extended_file_download_instance.name == "Bilbo"


def test_create_download_populates_file_field(
    file_download_instance_with_successfull_file_creation,
):
    assert (
        file_download_instance_with_successfull_file_creation.download_file.name
        is not None
    )


def test_create_download_creates_file(
    file_download_instance_with_successfull_file_creation,
):
    with open(
        file_download_instance_with_successfull_file_creation.download_file.path
    ) as f:
        assert f.read() == "Hello, World!"


def test_create_download_sets_status(
    file_download_instance_with_successfull_file_creation,
):
    status = file_download_instance_with_successfull_file_creation.COMPLETE
    assert file_download_instance_with_successfull_file_creation.status == status


def test_create_download_sets_completed_at(
    file_download_instance_with_successfull_file_creation,
):
    assert isinstance(
        file_download_instance_with_successfull_file_creation.created_at,
        datetime.datetime,
    )


def test_file_creation_error_does_not_add_file(
    file_download_instance_with_errored_file_creation,
):
    assert file_download_instance_with_errored_file_creation.download_file.name is None


def test_file_creation_error_sets_staus(
    file_download_instance_with_errored_file_creation,
):
    status = file_download_instance_with_errored_file_creation.ERRORED
    assert file_download_instance_with_errored_file_creation.status == status


def test_file_creation_error_sets_completed_at(
    file_download_instance_with_errored_file_creation,
):
    assert isinstance(
        file_download_instance_with_errored_file_creation.completed_at,
        datetime.datetime,
    )


@patch("file_exchange.tasks.slow_task")
def test_celery(slow_task, celery_session_worker):
    tasks.test_task.delay().get()
    slow_task.assert_called_once()

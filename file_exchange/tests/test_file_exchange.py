import datetime
from unittest.mock import patch

import pytest

from file_exchange import models

from .testapp import models as testapp_models


def test_FileDownload_generate_file_method_raises_not_implemented(
    unextended_file_download_instance,
):
    with pytest.raises(NotImplementedError):
        unextended_file_download_instance.generate_file()


def test_file_download_instance_has_IN_PROGRESS_attribute(
    extended_file_download_instance,
):
    assert extended_file_download_instance.IN_PROGRESS == models.IN_PROGRESS


def test_file_download_instance_has_COMLLETE_attribute(
    extended_file_download_instance,
):
    assert extended_file_download_instance.COMPLETE == models.COMPLETE


def test_file_download_instance_has_ERRORED_attribute(
    extended_file_download_instance,
):
    assert extended_file_download_instance.ERRORED == models.ERRORED


def test_file_download_instance_uses_file_download_manager(
    extended_file_download_model,
):
    assert isinstance(extended_file_download_model.objects, models.FileDownloadManager)


def test_file_download_instance_status_default_value(unextended_file_download_instance):
    assert unextended_file_download_instance.status == models.IN_PROGRESS


def test_file_download_instance_created_at_default_value(
    extended_file_download_instance,
):
    assert isinstance(extended_file_download_instance.created_at, datetime.datetime)


def test_file_download_instance_completed_at_default_value(
    extended_file_download_instance,
):
    assert extended_file_download_instance.completed_at is None


def test_file_download_instance_error_message_default_value(
    extended_file_download_instance,
):
    assert extended_file_download_instance.error_message == ""


def test_extended_file_download_extra_field(extended_file_download_instance):
    assert extended_file_download_instance.name == "Bilbo"


def test_create_download_populates_file_field(
    file_download_instance_with_successful_file_creation,
):
    assert (
        file_download_instance_with_successful_file_creation.download_file.name
        is not None
    )


def test_create_download_creates_file(
    file_download_instance_with_successful_file_creation,
):
    with open(
        file_download_instance_with_successful_file_creation.download_file.path
    ) as f:
        assert f.read() == "Hello, World!"


def test_create_download_sets_status(
    file_download_instance_with_successful_file_creation,
):
    status = file_download_instance_with_successful_file_creation.COMPLETE
    assert file_download_instance_with_successful_file_creation.status == status


def test_create_download_sets_completed_at(
    file_download_instance_with_successful_file_creation,
):
    assert isinstance(
        file_download_instance_with_successful_file_creation.created_at,
        datetime.datetime,
    )


def test_create_download_does_not_set_error_message(
    file_download_instance_with_successful_file_creation,
):
    assert file_download_instance_with_successful_file_creation.error_message == ""


def test_file_creation_error_does_not_add_file(
    file_download_instance_with_errored_file_creation,
):
    assert file_download_instance_with_errored_file_creation.download_file.name == ""


def test_file_creation_error_sets_status(
    file_download_instance_with_errored_file_creation,
):
    status = file_download_instance_with_errored_file_creation.ERRORED
    assert file_download_instance_with_errored_file_creation.status == status


def test_file_creation_error_sets_error_message(
    file_download_instance_with_errored_file_creation,
):
    assert (
        file_download_instance_with_errored_file_creation.error_message
        == "Exception('TEST EXCEPTION')"
    )


def test_file_creation_error_sets_completed_at(
    file_download_instance_with_errored_file_creation,
):
    assert isinstance(
        file_download_instance_with_errored_file_creation.completed_at,
        datetime.datetime,
    )


def test_pre_generation_method_is_called(celery_session_worker):
    with patch(
        "file_exchange.tests.testapp.models.FileDownloadWithPreGenerationMethod.pre_generation"
    ):
        (
            task,
            instance,
        ) = testapp_models.FileDownloadWithPreGenerationMethod.objects.create_download()
        task.get()
        assert instance.pre_generation.called_once()


def test_post_generation_method_is_called(celery_session_worker):
    with patch(
        "file_exchange.tests.testapp.models.FileDownloadWithPostGenerationMethod.post_generation"
    ):
        (
            task,
            instance,
        ) = (
            testapp_models.FileDownloadWithPostGenerationMethod.objects.create_download()
        )
        task.get()
        assert instance.post_generation.called_once()

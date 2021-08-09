import datetime as dt

import pytest

from file_exchange import models

from .testapp import views


@pytest.fixture
def in_progress_file_download(extended_file_download_factory):
    return extended_file_download_factory.create(
        status=models.BaseFileExchangeModel.IN_PROGRESS,
        created_at=dt.datetime(
            year=2021, month=6, day=22, hour=9, minute=57, second=23
        ),
        completed_at=None,
        error_message="",
    )


@pytest.fixture
def complete_file_download(extended_file_download_factory):
    return extended_file_download_factory.create(
        status=models.BaseFileExchangeModel.COMPLETE,
        created_at=dt.datetime(
            year=2021, month=6, day=22, hour=9, minute=57, second=23
        ),
        completed_at=dt.datetime(
            year=2021, month=6, day=22, hour=10, minute=26, second=45
        ),
        error_message="",
    )


@pytest.fixture
def errored_file_download(extended_file_download_factory):
    return extended_file_download_factory.create(
        status=models.BaseFileExchangeModel.ERRORED,
        created_at=dt.datetime(
            year=2021, month=6, day=22, hour=9, minute=57, second=23
        ),
        completed_at=dt.datetime(
            year=2021, month=6, day=22, hour=10, minute=26, second=45
        ),
        error_message="TEST_ERROR_MESSAGE",
    )


@pytest.fixture
def file_download_status_response_with_in_progress_download(
    request_client, in_progress_file_download
):
    client = request_client(ajax=True)
    response = client.get(("file_download_status", {}), ajax=True)
    return response


@pytest.fixture
def file_download_status_response_with_in_progress_download_content(
    file_download_status_response_with_in_progress_download,
):
    response_text = (
        file_download_status_response_with_in_progress_download.content.decode("utf-8")
    )
    return response_text


@pytest.fixture
def file_download_status_response_with_complete_download(
    request_client, complete_file_download
):
    client = request_client(ajax=True)
    response = client.get(("file_download_status", {}), ajax=True)
    return response


@pytest.fixture
def file_download_status_response_with_complete_download_content(
    file_download_status_response_with_complete_download,
):
    return file_download_status_response_with_complete_download.content.decode("utf-8")


@pytest.fixture
def file_download_status_response_with_no_existant_download(request_client):
    client = request_client(ajax=True)
    response = client.get(("file_download_status", {}), ajax=True)
    return response


@pytest.fixture
def file_download_status_response_with_no_existant_download_content(
    file_download_status_response_with_no_existant_download,
):
    return file_download_status_response_with_no_existant_download.content.decode(
        "utf-8"
    )


def test_in_progress_file_download_status_view_shows_status(
    file_download_status_response_with_in_progress_download_content,
):
    assert (
        "In Progress" in file_download_status_response_with_in_progress_download_content
    )


def test_in_progress_file_download_status_view_shows_created_at(
    in_progress_file_download,
    file_download_status_response_with_in_progress_download_content,
):
    date = in_progress_file_download.created_at
    date_string = date.strftime("%Y-%m-%d %H:%M")
    assert (
        date_string in file_download_status_response_with_in_progress_download_content
    )


def test_complete_file_download_status_view_shows_status(
    file_download_status_response_with_complete_download_content,
):
    assert "Complete" in file_download_status_response_with_complete_download_content


def test_complete_file_download_status_view_shows_created_at(
    in_progress_file_download,
    file_download_status_response_with_complete_download_content,
):
    date = in_progress_file_download.created_at
    date_string = date.strftime("%Y-%m-%d %H:%M")
    assert date_string in file_download_status_response_with_complete_download_content


def test_download_status_with_no_existant_download(
    file_download_status_response_with_no_existant_download_content,
):
    text = file_download_status_response_with_no_existant_download_content
    assert "<p>NO DOWNLOAD HAS BEEN CREATED</p>" in text


@pytest.fixture
def file_download_page_view_response(request_client):
    client = request_client(ajax=True)
    response = client.get(("file_download_page", {}), ajax=True)
    return response


@pytest.fixture
def file_download_page_view_response_content(file_download_page_view_response):
    return file_download_page_view_response.content.decode("utf8")


def test_file_download_page_contains_status_url(
    file_download_page_view_response_content,
):
    text = file_download_page_view_response_content
    assert views.ExtendedDownloadFileView.status_url in text


def test_file_download_page_contains_created_file_url(
    file_download_page_view_response_content,
):
    text = file_download_page_view_response_content
    assert views.ExtendedDownloadFileView.create_file_url in text

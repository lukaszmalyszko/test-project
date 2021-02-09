from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from project.models import STATUS_ERROR, STATUS_READY, DownloadContent, Http, db, Image
from project.schemas import ImageSchema
from project.worker.handlers import _download_content_text, _download_content_images
from tests.fixture_factories import DownloadContentFactory
from tests.unit.data.example_html import (
    get_example_html_code_in_bytes,
    get_expected_cleared_text,
)


class TestDownloadContentTextHandler:
    @patch("project.adapters.local_adapter.urlretrieve")
    @patch("project.worker.handlers.urllib.request.urlopen")
    def test_update_images_and_change_status_to_ready(
        self, urlopen_mock, urlretrieve_mock, init_database
    ):
        self.__given_download_content(url='http://test.pl')
        self.__given_urlopen_mock(urlopen_mock)

        _download_content_images(self.download_content_data["id"])

        self.__then_download_content_images_should_be_updated()

    @patch("project.worker.handlers.urllib.request.urlopen")
    def test_update_text_and_change_status_to_ready(self, urlopen_mock, init_database):
        self.__given_download_content()
        self.__given_urlopen_mock(urlopen_mock)

        self.__when_prepare_downloaded_text()

        self.__then_download_content_text_should_be_updated()

    @patch("project.worker.handlers.urllib.request.urlopen")
    def test_change_status_to_error_when_value_error(self, urlopen_mock, init_database):
        error = ValueError()
        self.__given_download_content()
        self.__given_urlopen_mock(urlopen_mock, error)
        msg = "Incorrect URL address"

        self.__when_prepare_downloaded_text()

        self.__then_download_content_text_shouldnt_be_updated(msg)

    @patch("project.worker.handlers.urllib.request.urlopen")
    def test_change_status_to_error_when_http_error(self, urlopen_mock, init_database):
        self.__given_download_content()
        expected_msg = "HTTP Error 500: Internal Error"
        error = HTTPError(
            self.download_content_data["url"], 500, "Internal Error", {}, None
        )
        self.__given_urlopen_mock(urlopen_mock, error)

        self.__when_prepare_downloaded_text()

        self.__then_download_content_text_shouldnt_be_updated(expected_msg)

    @patch("project.worker.handlers.urllib.request.urlopen")
    def test_change_status_to_error_when_url_error(self, urlopen_mock, init_database):
        self.__given_download_content()
        msg = "Unknown host"
        error = URLError(msg)
        self.__given_urlopen_mock(urlopen_mock, error)

        self.__when_prepare_downloaded_text()

        self.__then_download_content_text_shouldnt_be_updated(msg)

    def __given_urlopen_mock(self, urlopen_mock, side_effect=None):
        http_response = Mock()
        http_response.getcode.return_value = Http.OK
        http_response.read.return_value = get_example_html_code_in_bytes()
        urlopen_mock.return_value = http_response
        urlopen_mock.side_effect = side_effect

    def __given_download_content(self, **kwargs):
        self.download_content_data = DownloadContentFactory.build(**kwargs)
        download_content = DownloadContent(**self.download_content_data)
        db.session.add(download_content)
        db.session.commit()

    def __then_download_content_images_should_be_updated(self):
        download_content = DownloadContent.query.get(self.download_content_data["id"])
        expected_images = ["static/tmp/python-logo.png"]

        self.__assert_images(download_content, expected_images)
        assert download_content.status == STATUS_READY
        assert download_content.status_msg == self.download_content_data["status_msg"]

    def __assert_images(self, download_content, expected_images):
        assert [img.path for img in download_content.images] == expected_images

    def __then_download_content_text_should_be_updated(self):
        download_content = DownloadContent.query.get(self.download_content_data["id"])

        assert download_content.text == get_expected_cleared_text()
        assert download_content.status == STATUS_READY
        assert download_content.status_msg == self.download_content_data["status_msg"]

    def __then_download_content_text_shouldnt_be_updated(self, msg):
        download_content = DownloadContent.query.get(self.download_content_data["id"])

        assert download_content.text == ""
        assert download_content.status == STATUS_ERROR
        assert download_content.status_msg == msg

    def __when_prepare_downloaded_text(self):
        _download_content_text(self.download_content_data["id"])

from unittest.mock import patch

from project.models import DownloadContent, Http, db
from tests.fixture_factories import DownloadContentFactory


class TestRestDownloadContent:
    def test_return_download_content_status(self, test_client, init_database):
        self.__given_download_content()
        expected_response = {"status": self.download_content_data["status"]}
        url = f"/extractor/{self.download_content_data['id']}"

        response = test_client.get(url, content_type="application/json;only=status")

        assert response.status_code == Http.OK
        assert response.json == expected_response

    def test_return_msg_if_not_download_content_pending_status(
        self, test_client, init_database
    ):
        expected_response = {"msg": "Obiekt o wskazanym id nie istnieje"}
        url = "/extractor/123"

        response = test_client.get(url, content_type="application/json;only=status")

        assert response.status_code == Http.NOT_FOUND
        assert response.json == expected_response

    def test_get_return_unprocessable_entity_response_when_cant_find_only_content_type(
        self, test_client, init_database
    ):
        self.__given_download_content()
        expected_response = {"msg": "Not acceptable response."}
        url = f"/extractor/{self.download_content_data['id']}"

        response = test_client.get(url, content_type="application/json")

        assert response.status_code == Http.NOT_ACCEPTABLE
        assert response.json == expected_response

    @patch("project.download_content.download_contents.download_content_text")
    def test_create_download_content_and_send_task_for_text(
        self, celery_mock, test_client, init_database
    ):
        body = {
            "url": "https://www.test.pl/",
            "name": "test",
        }
        url = "/extractor/"

        response = test_client.post(
            url, json=body, content_type="application/json;only=text"
        )

        assert response.status_code == Http.CREATED
        celery_mock.delay.assert_called_once_with(response.json["id"])

    def test_return_unprocessable_entity_response_when_invalid_url(
        self, test_client, init_database
    ):
        body = {
            "url": "//test.pl/",
            "name": "test",
        }
        url = "/extractor/"

        response = test_client.post(
            url, json=body, content_type="application/json;only=text"
        )

        assert response.status_code == Http.UNPROCESSABLE_ENTITY
        assert response.json == {}

    def test_post_return_unprocessable_entity_response_when_cant_find_only_content_type(
        self, test_client, init_database
    ):
        body = {
            "url": "https://test.pl/",
            "name": "test",
        }
        url = "/extractor/"

        response = test_client.post(url, json=body, content_type="application/json")

        assert response.status_code == Http.NOT_ACCEPTABLE
        assert response.json == {"msg": "Not acceptable response."}

    @patch("project.download_content.download_contents.download_content_images")
    def test_create_download_content_and_send_task_for_images(
        self, celery_mock, test_client, init_database
    ):
        body = {
            "url": "https://www.test.pl/",
            "name": "test",
        }
        url = "/extractor/"

        response = test_client.post(
            url, json=body, content_type="application/json;only=images"
        )

        assert response.status_code == Http.CREATED
        celery_mock.delay.assert_called_once_with(response.json["id"])

    @patch("project.download_content.download_contents.download_content_images")
    @patch("project.download_content.download_contents.download_content_text")
    def test_create_download_content_and_send_task_for_both(
        self,
        download_content_text_mock,
        download_content_images_mock,
        test_client,
        init_database,
    ):
        body = {
            "url": "https://www.test.pl/",
            "name": "test",
        }
        url = "/extractor/"

        response = test_client.post(
            url, json=body, content_type="application/json;only=both"
        )

        assert response.status_code == Http.CREATED
        download_content_text_mock.delay.assert_called_once_with(response.json["id"])
        download_content_images_mock.delay.assert_called_once_with(response.json["id"])

    def __given_download_content(self, **kwargs):
        self.download_content_data = DownloadContentFactory.build(**kwargs)
        download_content = DownloadContent(**self.download_content_data)
        db.session.add(download_content)
        db.session.commit()

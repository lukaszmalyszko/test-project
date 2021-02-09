from unittest.mock import patch

from project.adapters.local_adapter import LocalAdapter


class TestLocalAdapter:
    @patch("project.adapters.local_adapter.urlretrieve")
    def test_returns_list_with_images_paths(self, urlretrieve_mock):
        download_date = "2021-02-09"
        test_images = [
            "http://test/photo1.png",
            "http://test/photo2.png",
            "http://test/photo3.png",
        ]
        adapter = LocalAdapter()

        response = adapter.upload_images(test_images, download_date)

        for test_image, response_image in zip(test_images, response):
            filename = test_image.split("/")[-1]
            assert filename in response_image["path"]

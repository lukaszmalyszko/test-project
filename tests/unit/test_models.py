from project.models import DownloadContent, Image
from project.schemas import ImageSchema
from tests.fixture_factories import DownloadContentFactory, ImageFactory


def test_download_content():
    download_content_data = DownloadContentFactory.build()

    download_content = DownloadContent(**download_content_data)

    assert download_content.id == download_content_data["id"]
    assert download_content.url == download_content_data["url"]
    assert download_content.status == download_content_data["status"]
    assert download_content.status_msg == download_content_data["status_msg"]
    assert download_content.name == download_content_data["name"]
    assert download_content.text == download_content_data["text"]
    assert download_content.download_date == download_content_data["download_date"]


def test_download_content_with_image_return_both():
    download_content_data = DownloadContentFactory.build()
    image_data = ImageFactory.build()
    image = Image(**image_data)
    download_content_data["images"] = [image]

    download_content = DownloadContent(**download_content_data)

    download_content_data["download_date"] = __prepare_download_date(
        download_content_data
    )
    download_content_data["images"] = [ImageSchema().dump(image)]
    assert download_content.both() == download_content_data


def __prepare_download_date(download_content_data):
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    return download_content_data["download_date"].strftime(date_format)


def test_download_content_with_images():
    image_data = ImageFactory.build()
    image = Image(**image_data)
    download_content_data = DownloadContentFactory.build()
    download_content_data["images"] = [image]
    download_content = DownloadContent(**download_content_data)

    assert download_content.images.first() == image

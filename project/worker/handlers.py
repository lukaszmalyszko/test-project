import urllib.request
from urllib.error import HTTPError, URLError

from project.adapters.local_adapter import LocalAdapter
from project.models import STATUS_ERROR, STATUS_READY, DownloadContent, Image, db
from project.utils import clear_html_and_parse_to_text, get_images_url
from project.worker import celery


@celery.task(name="tasks.download_content_images")
def download_content_images(download_content_id: int) -> None:
    _download_content_images(download_content_id)


def _download_content_images(
    download_content_id, adapter: LocalAdapter = LocalAdapter()
) -> None:
    download_content = DownloadContent.query.get(download_content_id)
    content = _get_content(download_content)
    if content:
        images = get_images_url(content, download_content.url)
        storage_images = adapter.upload_images(images)
        for image in storage_images:
            image_obj = Image(**image)
            db.session.add(image_obj)
            download_content.images.append(image_obj)
        download_content.status = STATUS_READY
    db.session.commit()


@celery.task(name="tasks.download_content_text")
def download_content_text(download_content_id: int) -> None:
    _download_content_text(download_content_id)


def _download_content_text(download_content_id: int) -> None:
    download_content = DownloadContent.query.get(download_content_id)
    content = _get_content(download_content)
    if content:
        cleared_text = clear_html_and_parse_to_text(content)
        download_content.text = cleared_text
        download_content.status = STATUS_READY
    db.session.commit()


def _get_content(download_content: DownloadContent) -> bytes:
    content = b""
    try:
        content = urllib.request.urlopen(download_content.url).read()
    except ValueError:
        msg = "Incorrect URL address"
        download_content.status = STATUS_ERROR
        download_content.status_msg = f"{msg}"
    except HTTPError as msg:
        download_content.status = STATUS_ERROR
        download_content.status_msg = f"{msg}"
    except URLError as msg:
        download_content.status = STATUS_ERROR
        download_content.status_msg = f"{msg.args[0]}"
    return content

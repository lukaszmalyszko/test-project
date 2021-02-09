import datetime

from flask import request
from marshmallow import ValidationError

from project.models import STATUS_PENDING, DownloadContent, Http, db
from project.schemas import DownloadContentSchema
from project.worker.handlers import (download_content_images,
                                     download_content_text)

from . import download_contents_blueprint

GET_CONTENT_TYPES_MAP = {
    "application/json;only=status": "status",
    "application/json;only=text": "text",
    "application/json;only=images": "images",
    "application/json;only=both": "both",
}


@download_contents_blueprint.route("/extractor/", methods=["POST"])
def extractor():
    download_content_data = request.get_json(force=True)
    try:
        validated_data = DownloadContentSchema().load(download_content_data)
    except ValidationError:
        return unprocessable_entity_response()
    download_content = create_download_content_object(validated_data)
    content_type = request.headers["content_type"]
    send_task = POST_CONTENT_TYPES_MAP.get(content_type)
    if send_task:
        send_task(download_content.id)
    else:
        return not_acceptable_response()
    return DownloadContentSchema().dump(download_content), Http.CREATED


@download_contents_blueprint.route("/extractor/<id>", methods=["GET"])
def extractor_obj(id):
    download_content = DownloadContent.query.get(id)
    if not download_content:
        return {"msg": "Obiekt o wskazanym id nie istnieje"}, Http.NOT_FOUND
    content_type = request.headers["content_type"]
    request_only = GET_CONTENT_TYPES_MAP.get(content_type)
    if request_only:
        return {request_only: getattr(download_content, request_only)}, Http.OK
    return not_acceptable_response()


def not_acceptable_response():
    return {"msg": "Not acceptable response."}, Http.NOT_ACCEPTABLE


def unprocessable_entity_response():
    return {}, Http.UNPROCESSABLE_ENTITY


def create_download_content_object(download_content_data):
    download_content_data["status"] = STATUS_PENDING
    download_content_data["download_date"] = datetime.datetime.utcnow()
    download_content = DownloadContent(**download_content_data)
    db.session.add(download_content)
    db.session.commit()
    return download_content


def extractor_text(download_content_id: int):
    download_content_text.delay(download_content_id)


def extractor_images(download_content_id: int):
    download_content_images.delay(download_content_id)


def extractor_both(download_content_id: int):
    extractor_images(download_content_id)
    extractor_text(download_content_id)


POST_CONTENT_TYPES_MAP = {
    "application/json;only=text": extractor_text,
    "application/json;only=images": extractor_images,
    "application/json;only=both": extractor_both,
}

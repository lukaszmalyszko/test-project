from urllib.parse import urlparse

from marshmallow import Schema, ValidationError, fields, validates


class ImageSchema(Schema):
    id = fields.Integer()
    path = fields.String()
    download_content_id = fields.Integer()


class DownloadContentSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    url = fields.String()
    status = fields.String()
    status_msg = fields.String()
    text = fields.String()
    download_date = fields.DateTime()
    images = fields.Nested(ImageSchema(many=True))

    @validates("url")
    def validate_url(self, url):
        parsed = urlparse(url)
        if bool(parsed.netloc) and bool(parsed.scheme):
            return url
        else:
            raise ValidationError("Wrong field value.", "url")

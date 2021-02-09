from flask import Blueprint

download_contents_blueprint = Blueprint("download_content", __name__)

from . import download_contents

import datetime

import factory
from factory.fuzzy import FuzzyChoice, FuzzyText

from project.models import STATUS_PENDING, STATUS_READY


class DownloadContentFactory(factory.DictFactory):
    id = factory.Sequence(lambda n: n + 1)
    status = FuzzyChoice([STATUS_PENDING, STATUS_READY])
    status_msg = ""
    name = FuzzyText(length=20)
    url = FuzzyText(length=24)
    text = ""
    download_date = datetime.datetime.utcnow()
    images = []


class ImageFactory(factory.DictFactory):
    id = factory.Sequence(lambda n: n + 1)
    path = FuzzyText(length=24)

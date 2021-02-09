from enum import IntEnum

from flask_sqlalchemy import SQLAlchemy

from project.schemas import DownloadContentSchema

db = SQLAlchemy()

STATUS_PENDING = "Pending"
STATUS_READY = "Ready"
STATUS_ERROR = "Error"


class DownloadContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    url = db.Column(db.String(248))
    status = db.Column(db.String(8))
    status_msg = db.Column(db.String(128), default="")
    text = db.Column(db.Text, nullable=True)
    download_date = db.Column(db.DateTime())
    images = db.relationship("Image", backref="DownloadContent", lazy="dynamic")

    def both(self):
        return DownloadContentSchema().dump(self)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(248))
    download_content_id = db.Column(db.Integer, db.ForeignKey("download_content.id"))


class Http(IntEnum):
    OK = 200  #: Zwracane jeżeli nie wystąpiły błędy
    CREATED = 201  #: Zwracane przez zapytania POST/PUT jeżeli udało się utworzyć obiekt
    NO_CONTENT = 204  #: Zwracane w przypadku, gdy API nie musi zwracać treści odpowiedzi (np. usunięcie obiektu)
    PERMANENT_REDIRECT = 301  #: Zwracane jeżeli potrzeba wykonać przekierowanie
    BAD_REQUEST = 400  #: Zwracane jeżeli wystąpił ogólny błąd walidacji
    UNAUTHORIZED = 401  #: Zwracane, jeżeli wymagana jest autoryzacja
    FORBIDDEN = 403  #: Zwracane, jeżeli użytkownik nie ma prawa dostępu
    NOT_FOUND = 404  #: Zwracane, jeżeli obiekt nie istnieje
    NOT_ACCEPTABLE = (
        406  #: Zwracane, jeżeli nie można zwrócić odpowiedzi na dane zapytanie
    )
    CONFLICT = 409  #: Zwracane, jeżeli obiekt już istnieje
    UNSUPPORTED_MEDIA_TYPE = 415  #: Zwracane jeżeli obiekt jest w innym formacie niż oczekiwaliśmy (zwykle JSON)
    UNPROCESSABLE_ENTITY = 422  #: Zwracane, gdy dane w poprawnym formacie nie przechodzą dodatkowo stworzonej walidacji
    BAD_GATEWAY = (
        502  #: Zwracane, jeżeli wystąpił błąd komunikacji z zależnym komponentem
    )
    INFINITE_REDIRECTION_LOOP = 508  #: Zwracane, jeżeli wykryto zapętlenie przekierowań

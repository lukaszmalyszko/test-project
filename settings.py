import os

# database info
user = os.getenv("DB_USER", "flask")
password = os.getenv("DB_PASSWORD", "")
host = os.getenv("DB_HOST", "mysql")
name = os.getenv("DB_NAME", "flask")
STORAGE_URI = f"mysql+pymysql://{user}:{password}@{host}/{name}"

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

GOOGLE_APPLICATION_CREDENTIALS = "gcs.json"

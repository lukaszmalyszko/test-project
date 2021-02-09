import pathlib

from google.cloud import storage

from project.adapters.local_adapter import LocalAdapter

CLOUD_PATH = "https://storage.googleapis.com/"
# 'https://storage.googleapis.com/BUCKET_NAME/OBJECT_NAME'


class GCSAdapter(LocalAdapter):
    def __init__(self, bucket_name: str):
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.storage_client.bucket(bucket_name)

    def upload_images(self, images, download_date) -> list:
        images_paths = super().upload_images(images, download_date)
        cloud_paths = []
        for image in images_paths:
            local_path = image["path"]
            filename = local_path.split("/")[-1]
            self.__upload_blob(local_path, filename)
            pathlib.Path.unlink(local_path)
            cloud_paths.append({"path": f"{CLOUD_PATH}/{self.bucket_name}/{filename}"})
        return cloud_paths

    def __upload_blob(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)


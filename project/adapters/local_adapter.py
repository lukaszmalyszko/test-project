import os
from urllib.request import urlretrieve

LOCAL_PATH = "static/tmp/"


class LocalAdapter:
    def upload_images(self, images, download_date) -> list:
        images_paths = []
        for image_url in images:
            outpath = os.path.join(f"{LOCAL_PATH}{download_date}/", image_url.split("/")[-1])
            urlretrieve(image_url, outpath)
            images_paths.append({"path": outpath})
        return images_paths

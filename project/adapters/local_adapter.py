import os
from urllib.request import urlretrieve

LOCAL_PATH = "static/tmp/"


class LocalAdapter:
    def upload_images(self, images) -> list:
        images_paths = []
        for image_url in images:
            outpath = os.path.join(LOCAL_PATH, image_url.split("/")[-1])
            urlretrieve(image_url, outpath)
            images_paths.append({"path": outpath})
        return images_paths

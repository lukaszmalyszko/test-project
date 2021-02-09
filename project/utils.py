from urllib.parse import urljoin

from bs4 import BeautifulSoup

TAGS_TO_EXCLUDE = ["script", "style", "img"]
IMG_FORMATS = ["jpg", "gif", "png"]


def clear_html_and_parse_to_text(
    html: bytes, tags_to_exclude: list = TAGS_TO_EXCLUDE
) -> str:
    soup = BeautifulSoup(html)

    for script in soup(tags_to_exclude):
        script.decompose()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


def get_images_url(html: bytes, site) -> list:
    soup = BeautifulSoup(html)
    img_tags = soup.find_all("img")
    image_urls = []
    for img in img_tags:
        image_url = urljoin(site, img["src"])
        filename = img["src"].split("/")[-1]
        if filename.split(".")[-1] in IMG_FORMATS:
            image_urls.append(image_url)
    return image_urls

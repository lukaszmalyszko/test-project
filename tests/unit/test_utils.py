from project.utils import clear_html_and_parse_to_text, get_images_url
from tests.unit.data.example_html import (
    get_example_html_code_in_bytes,
    get_expected_cleared_text,
)


def test_returns_cleared_text():
    html_page = get_example_html_code_in_bytes()
    expected_text = get_expected_cleared_text()

    cleared_text = clear_html_and_parse_to_text(html_page)

    assert cleared_text == expected_text


def test_returns_images_url_from_site():
    html_page = get_example_html_code_in_bytes()
    expected_images = ["http://test.pl/static/img/python-logo.png"]

    images = get_images_url(html_page, "http://test.pl")

    assert images == expected_images

import pytest
from playwright.sync_api import Page

from utils.config import DEFAULT_BASE_URL


def pytest_addoption(parser):
    parser.addoption(
        "--bonbonite-url",
        default=DEFAULT_BASE_URL,
        help="URL base de la tienda (puede apuntar a staging).",
    )
    parser.addoption(
        "--run-mutating",
        action="store_true",
        default=False,
        help="Habilita pruebas que registran usuarios o agregan productos al carrito.",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-mutating"):
        return

    skip_mutating = pytest.mark.skip(
        reason="Usa --run-mutating y preferiblemente una tienda de staging."
    )
    for item in items:
        if "mutating" in item.keywords:
            item.add_marker(skip_mutating)


@pytest.fixture
def store_url(request):
    return request.config.getoption("--bonbonite-url").rstrip("/")


@pytest.fixture(autouse=True)
def configure_page(page: Page):
    page.set_default_timeout(12_000)
    page.set_viewport_size({"width": 1440, "height": 1000})
import re
import warnings
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import Page

from utils.config import DEFAULT_BASE_URL

EVIDENCE_DIR = (
    Path(__file__).resolve().parent
    / "evidencias"
    / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
)


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
def configure_page(page: Page, request):
    page.set_default_timeout(12_000)
    page.set_viewport_size({"width": 1440, "height": 1000})
    yield

    case_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.nodeid)
    screenshot_path = EVIDENCE_DIR / f"{case_name}.png"
    try:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_path), full_page=True)
    except Exception as error:
        warnings.warn(
            f"No se pudo guardar la evidencia del caso {request.node.nodeid}: {error}",
            RuntimeWarning,
        )
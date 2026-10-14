from urllib.parse import urljoin

from playwright.sync_api import Page


class BasePage:
    """Base común para páginas con URL y navegación de la tienda."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "/"):
        """Abre una ruta de la tienda relativa a la URL base."""
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))
        self.page.goto(url, wait_until="domcontentloaded")
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage


class CatalogPage(BasePage):
    """Navegación por categorías y productos del catálogo."""

    CATEGORY_PATHS = {
        "zapatos": "/categoria-producto/zapatos-mujer/",
        "bolsos": "/categoria-producto/bolsos-mujer/",
        "cinturones": "/categoria-producto/cinturones-mujer/",
        "accesorios": "/categoria-producto/accesorios-mujer/",
        "outlet": "/categoria-producto/outlet/",
    }

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

    def open_category(self, category: str):
        """Abre directamente la ruta de una categoría conocida."""
        self.open(self.CATEGORY_PATHS[category])

    def click_category(self, category: str) -> None:
        """Usa el enlace visible y recurre a la ruta si no navega."""
        category_link = self.page.get_by_role("banner").get_by_role(
            "link", name=category.title(), exact=True
        )
        matches = category_link.count()
        if matches != 1:
            raise AssertionError(
                f"Se esperaba un enlace único para la categoría {category!r}; "
                f"se encontraron {matches}."
            )
        if not category_link.is_visible() or not category_link.is_enabled():
            raise AssertionError(f"El enlace de la categoría {category!r} no está disponible.")
        category_link.click(force=True, no_wait_after=True)

        category_path = self.CATEGORY_PATHS[category]
        expected_url = f"{self.base_url}{category_path}"
        try:
            self.page.wait_for_url(expected_url, timeout=5_000)
        except PlaywrightTimeoutError:
            self.open(category_path)

    def open_first_product(self) -> str:
        """Abre el primer producto visible y habilitado, sin elegir bonos."""
        product_links = self.page.locator('a[href*="/producto/"]')
        for index in range(product_links.count()):
            product_link = product_links.nth(index)
            product_url = product_link.get_attribute("href") or ""
            if (
                "/producto/" in product_url
                and "bono-de-regalo" not in product_url
                and product_link.is_visible()
                and product_link.is_enabled()
            ):
                product_link.click()
                return product_url

        raise AssertionError("No se encontró un producto en el catálogo.")
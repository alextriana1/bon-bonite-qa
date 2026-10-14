import re

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """Acciones disponibles en el carrito de compras."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.checkout_link: Locator = page.get_by_role(
            "link", name=re.compile("finalizar compra", re.IGNORECASE)
        )

    def open_cart(self):
        """Abre la página del carrito."""
        self.open("/carrito/")

    def proceed_to_checkout(self):
        """Continúa desde el carrito hasta el formulario de compra."""
        self.checkout_link.click()
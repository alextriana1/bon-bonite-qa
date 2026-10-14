import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Acciones de selección de talla y compra de un producto."""

    ADD_TO_CART = re.compile("añadir al carrito", re.IGNORECASE)

    def open_product(self, path: str):
        """Abre la ficha de producto indicada."""
        self.open(path)

    def choose_size(self, size: str):
        """Selecciona una talla específica."""
        self.page.get_by_role("button", name=size, exact=True).click()

    def choose_first_available_size(self) -> str:
        """Espera la primera talla habilitada, la selecciona y la devuelve."""
        available_sizes = self.page.locator("button.variation-button:not([disabled])")
        size_button = available_sizes.first
        expect(size_button).to_be_visible(timeout=12_000)
        expect(size_button).to_be_enabled(timeout=12_000)
        size = size_button.inner_text().strip()
        size_button.click()
        return size

    def buy_now(self) -> None:
        """Pulsa el enlace único para agregar el producto e iniciar la compra."""
        buy_now_link = self.page.get_by_role(
            "link", name=re.compile("comprar ahora", re.IGNORECASE)
        )
        matches = buy_now_link.count()
        if matches != 1:
            raise AssertionError(
                f"Se esperaba un enlace único 'Comprar Ahora'; se encontraron {matches}."
            )
        if not buy_now_link.is_visible() or not buy_now_link.is_enabled():
            raise AssertionError("El enlace 'Comprar Ahora' no está disponible.")
        buy_now_link.click(force=True)

    def add_to_cart(self):
        """Agrega el producto al carrito desde su ficha."""
        self.page.get_by_role("button", name=self.ADD_TO_CART).click()
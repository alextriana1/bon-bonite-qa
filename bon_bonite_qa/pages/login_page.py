from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Localizadores y acciones del formulario de inicio de sesión."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.document_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator('button[name="login"]')

    def open_login(self):
        """Abre la página de Mi cuenta, donde está el formulario de acceso."""
        self.open("/mi-cuenta/")

    def login(self, document: str, password: str):
        """Envía las credenciales del cliente."""
        self.document_input.fill(document)
        self.password_input.fill(password)
        self.submit_button.click()
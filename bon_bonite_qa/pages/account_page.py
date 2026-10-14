import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class AccountPage(BasePage):
    """Localizadores y acciones de registro y edición de la cuenta."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.register_toggle = page.locator("#show_register")
        self.register_form = page.locator("#form-register")
        self.document_input = page.locator("#reg_username")
        self.first_name_input = page.locator("#first_name")
        self.last_name_input = page.locator("#last_name")
        self.email_input = page.locator("#reg_email")
        self.password_input = page.locator("#reg_password")
        self.confirm_password_input = page.locator("#reg_password2")
        self.privacy_checkbox = page.locator("#privacy_policy_reg")
        self.register_button = page.locator('#form-register button[name="register"]')
        self.update_information_button = page.get_by_role(
            "button", name=re.compile("actualizar información", re.IGNORECASE)
        )
        self.edit_first_name_input = page.locator('input[name="first_name"]')
        self.edit_last_name_input = page.locator('input[name="last_name"]')
        self.save_account_button = page.get_by_role("button", name="Guardar", exact=True).first

    def open_account(self):
        """Abre la página principal de Mi cuenta."""
        self.open("/mi-cuenta/")

    def register(self, document: str, first_name: str, last_name: str, email: str, password: str):
        """Completa y envía el formulario de registro."""
        self.register_toggle.click()
        self.document_input.fill(document)
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.confirm_password_input.fill(password)
        self.privacy_checkbox.check()
        self.register_button.click()

    def open_profile(self):
        """Abre la página de edición del perfil del cliente."""
        self.open("/mi-cuenta/edit-account/")

    def update_profile(self, first_name: str, last_name: str):
        """Actualiza el nombre y devuelve la respuesta del servidor."""
        self.update_information_button.click()
        self.edit_first_name_input.fill(first_name)
        self.edit_last_name_input.fill(last_name)
        with self.page.expect_response(
            lambda response: "admin-ajax.php" in response.url
        ) as response_info:
            self.save_account_button.click()
        return response_info.value

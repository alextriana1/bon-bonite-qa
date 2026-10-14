from datetime import date
from pathlib import Path

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class PQRSPage(BasePage):
    """Controles y acciones del formulario de peticiones, quejas y reclamos."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.cookie_consent_dialog = page.get_by_role(
            "dialog", name="Cookie consent dialog"
        )
        self.accept_cookies_button = self.cookie_consent_dialog.get_by_role(
            "button", name="Aceptar todo"
        )
        self.create_request_button = page.get_by_role("button", name="CREAR PQRS")
        self.tracking_number_input = page.get_by_role("textbox", name="Número de radicado")
        self.point_of_sale = page.locator('select[name="select-1"]')
        self.request_date = page.locator('input[name="text-2"]')
        self.customer_name = page.locator('input[name="name-1"]')
        self.address = page.locator('input[name="address-1-street_address"]')
        self.document_type = page.locator('select[name="select-2"]')
        self.document_number = page.locator('input[name="text-1"]')
        self.phone = page.locator('input[name="phone-1"]')
        self.email = page.locator('input[name="email-1"]')
        self.request_type = page.locator('select[name="select-3"]')
        self.cause = page.locator('select[name="select-4"]')
        self.description = page.locator('textarea[name="textarea-1"]')
        self.attachment = page.locator('input[name="upload-1[]"]')
        self.privacy_consent = page.locator('input[name="consent-1"]')
        self.privacy_consent_label = page.locator("label.forminator-consent")

    def accept_cookies(self):
        """Acepta el aviso de cookies solo cuando está visible."""
        if self.cookie_consent_dialog.is_visible():
            self.accept_cookies_button.click()
            self.cookie_consent_dialog.wait_for(state="hidden")

    def open_pqrs(self):
        """Abre el formulario de PQRS."""
        self.open("/pqrs/")

    def wait_for_form_ready(self):
        """Espera a que los campos del formulario estén visibles y habilitados."""
        fields = (
            self.point_of_sale,
            self.request_date,
            self.customer_name,
            self.address,
            self.document_type,
            self.document_number,
            self.phone,
            self.email,
            self.request_type,
            self.description,
        )
        for field in fields:
            field.wait_for(state="visible")
            expect(field).to_be_enabled(timeout=12_000)

        self.attachment.wait_for(state="attached")
        self.privacy_consent_label.wait_for(state="visible")
        self.create_request_button.wait_for(state="visible")

    def fill_submission_request(self, attachment_path: Path):
        """Completa la solicitud de prueba, adjunta evidencia y acepta el aviso."""
        self.wait_for_form_ready()
        self.point_of_sale.select_option(label="Bon-Bonite Sucre")
        self.request_date.fill(date.today().strftime("%d/%m/%Y"))
        self.customer_name.fill("QA Automatizacion")
        self.address.fill("Direccion de prueba 123, Medellin")
        self.document_type.select_option(label="Cédula de Ciudadanía (CC)")
        self.document_number.fill("1000000001")
        self.phone.fill("3001234567")
        self.email.fill("qa.pqrs@example.com")
        self.request_type.select_option(label="Solicitud de reversión total")
        if self.cause.is_visible():
            self.cause.select_option(label="Operación no solicitada")
        self.description.fill(
            "Solicitud de prueba automatizada con datos sinteticos. "
            "Favor no procesar; se envia para validar el formulario."
        )
        self.attachment.set_input_files(str(attachment_path))
        self.privacy_consent_label.click()

    def submit_request(self):
        """Envía el formulario de PQRS."""
        expect(self.create_request_button).to_be_enabled(timeout=12_000)
        self.create_request_button.click()
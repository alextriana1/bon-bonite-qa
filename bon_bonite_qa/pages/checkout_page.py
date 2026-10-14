from collections.abc import Mapping

from playwright.sync_api import Locator, Page, Response, expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Controles y acciones del formulario de finalizar compra."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.billing_country = page.locator("#billing_country")
        self.billing_state = page.locator("#billing_state")
        self.billing_fields = {
            "first_name": page.locator("#billing_first_name"),
            "last_name": page.locator("#billing_last_name"),
            "address_1": page.locator("#billing_address_1"),
            # "city": page.locator("#billing_city"),
            "postcode": page.locator("#billing_postcode"),
            "phone": page.locator("#billing_phone"),
            "email": page.locator("#billing_email"),
        }
        self.terms_checkbox = page.locator("#terms")
        self.continue_button = page.get_by_role(
            "button", name="Continuar", exact=True
        )
        self.place_order_button = page.locator(
            "#place_order, button[name='woocommerce_checkout_place_order']"
        ).first

    def continue_checkout(self) -> None:
        """Avanza desde el resumen hasta los datos de facturación."""
        self.continue_button.click()

    def fill_billing_form(self, details: Mapping[str, str]) -> None:
        """Completa solo los datos vacíos y conserva los valores existentes."""
        expect(self.billing_country).to_be_visible()
        expect(self.billing_country).to_be_enabled()
        if not self.billing_country.input_value().strip():
            self.billing_country.select_option(value=details["country"])
        for field, locator in self.billing_fields.items():
            editable_field = self._editable_field(locator, field)
            current_value = self._current_value(editable_field)
            if not current_value.strip():
                editable_field.fill(details[field])
        expect(self.billing_state).to_be_visible()
        expect(self.billing_state).to_be_enabled()
        if not self.billing_state.input_value().strip():
            self.billing_state.select_option(label=details["state"])
        if self.terms_checkbox.is_visible() and not self.terms_checkbox.is_checked():
            self.terms_checkbox.check()

    @staticmethod
    def _editable_field(locator: Locator, field: str) -> Locator:
        """Obtiene el control editable directo o el único dentro del contenedor."""
        is_editable = locator.evaluate(
            "element => element.matches('input, textarea') || element.isContentEditable"
        )
        if is_editable:
            return locator

        controls = locator.locator("input, textarea, [contenteditable='true']")
        matches = controls.count()
        if matches != 1:
            raise AssertionError(
                f"Se esperaba un control editable para facturación '{field}'; "
                f"se encontraron {matches}."
            )
        return controls

    @staticmethod
    def _current_value(locator: Locator) -> str:
        """Lee el valor de campos estándar o el texto de un control editable."""
        tag_name = locator.evaluate("element => element.tagName.toLowerCase()")
        if tag_name in {"input", "textarea"}:
            return locator.input_value()
        return locator.inner_text()

    def place_order(self) -> Response:
        """Envía el pedido y devuelve la respuesta AJAX del checkout."""
        with self.page.expect_response(
            lambda response: "wc-ajax=checkout" in response.url,
            timeout=30_000,
        ) as response_info:
            self.place_order_button.click()
        return response_info.value
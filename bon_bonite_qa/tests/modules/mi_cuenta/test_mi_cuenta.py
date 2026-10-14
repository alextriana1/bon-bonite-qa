import re

from playwright.sync_api import expect

from pages.login_page import LoginPage


def test_customer_can_log_in(login_page: LoginPage):
    """Comprueba que el login sea exitoso."""
    expect(login_page.document_input).to_be_hidden(timeout=12_000)

    expect(login_page.page).to_have_url(
        re.compile(r"/mi-cuenta/orders/?$"),
        timeout=12_000,
    )
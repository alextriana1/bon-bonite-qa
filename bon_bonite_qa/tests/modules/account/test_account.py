import uuid

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.login_page import LoginPage


@pytest.mark.mutating
def test_customer_can_register_and_update_profile(page, store_url):
    """Registra una cuenta nueva y comprueba que el perfil se actualice."""
    account = AccountPage(page, store_url)
    token = uuid.uuid4().hex[:10]
    document = str(1_000_000_000 + int(token[:8], 16) % 8_000_000_000)
    email = f"qa.bonbonite.{token}@example.com"
    password = f"Qa-{token}-Test!"

    account.open_account()
    account.register(document, "QA", "Automation", email, password)
    expect(account.register_form).to_be_hidden()

    account.open_profile()
    login = LoginPage(page, store_url)
    if login.document_input.is_visible():
        login.login(document, password)
        account.open_profile()

    profile_response = account.update_profile("QA Actualizado", "Automation Test")
    assert profile_response.ok, (
        f"Se esperaba una respuesta HTTP exitosa; se obtuvo HTTP {profile_response.status}."
    )
    response_success = profile_response.json().get("success")
    assert response_success is True, (
        f"Se esperaba success=True en la respuesta; se obtuvo {response_success!r}."
    )

    page.reload()
    account.update_information_button.click()
    expect(account.edit_first_name_input).to_have_value("QA Actualizado")
    expect(account.edit_last_name_input).to_have_value("Automation Test")
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from utils.config import TEST_LOGIN_DOCUMENT, TEST_LOGIN_PASSWORD


@pytest.fixture
def login_page(page: Page, store_url: str) -> LoginPage:
    """Inicia sesión con las credenciales QA configuradas en .env."""
    if not TEST_LOGIN_DOCUMENT or not TEST_LOGIN_PASSWORD:
        pytest.fail(
            "Completa BONBONITE_TEST_DOCUMENT y BONBONITE_TEST_PASSWORD "
            "en el archivo .env."
        )

    login_page = LoginPage(page, store_url)
    login_page.open_login()
    login_page.login(TEST_LOGIN_DOCUMENT, TEST_LOGIN_PASSWORD)
    return login_page
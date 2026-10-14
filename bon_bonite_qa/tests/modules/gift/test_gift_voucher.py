from playwright.sync_api import expect

from pages.base_page import BasePage


def test_gift_voucher_page_is_reachable(page, store_url):
    """Comprueba que la ficha del bono de regalo esté disponible."""
    voucher = BasePage(page, store_url)
    voucher.open("/producto/bono-de-regalo/")

    expect(page.get_by_role("heading", name="Bono de regalo")).to_be_visible()
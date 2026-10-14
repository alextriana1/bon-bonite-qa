import re

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.product_page import ProductPage
from test_data.checkout_billing import BILLING_DETAILS


@pytest.mark.mutating
def test_customer_can_buy_from_shoes_and_place_order(page, store_url, login_page):
    """Inicia sesión, compra un zapato y valida la redirección tras el pedido."""
    expect(login_page.document_input).to_be_hidden(timeout=15_000)

    catalog = CatalogPage(page, store_url)
    catalog.click_category("zapatos")
    expect(page).to_have_url(re.compile(r"/categoria-producto/zapatos-mujer/?$"))
    product_url = catalog.open_first_product()
    expect(page).to_have_url(product_url)

    product = ProductPage(page, store_url)
    product_name = page.get_by_role("heading", level=1).inner_text()
    size = product.choose_first_available_size()
    product.buy_now()

    cart = CartPage(page, store_url)
    expect(page).to_have_url(re.compile(r"/carrito/?(?:\?.*)?$"))
    expect(page.locator("body")).to_contain_text(f"{product_name} - {size}")
    expect(cart.checkout_link).to_be_visible()
    cart.proceed_to_checkout()

    checkout = CheckoutPage(page, store_url)
    expect(page).to_have_url(re.compile(r"/(finalizar-compra|checkout)/?"))
    expect(page.get_by_role("heading", name="Finalizar compra")).to_be_visible()
    expect(page.locator("body")).to_contain_text(f"{product_name} - {size}")
    expect(checkout.continue_button).to_be_visible()
    checkout.continue_checkout()
    expect(checkout.billing_fields["first_name"]).to_be_visible()

    checkout.fill_billing_form(BILLING_DETAILS)
    checkout_url = page.url
    order_response = checkout.place_order()

    assert order_response.ok, (
        f"Se esperaba HTTP exitoso al realizar el pedido; "
        f"se obtuvo HTTP {order_response.status}."
    )
    expect(page).not_to_have_url(checkout_url, timeout=30_000)
    assert page.url != checkout_url, (
        f"Se esperaba redirección a la página de pago; "
        f"la URL continuó en {page.url!r}."
    )
import re

from playwright.sync_api import expect

from pages.catalog_page import CatalogPage


def test_shoes_category_opens_product(page, store_url):
    """Comprueba el catálogo de zapatos y abre el primer zapato listado."""
    catalog = CatalogPage(page, store_url)
    catalog.open_category("zapatos")

    expect(page).to_have_title(re.compile(r"^Zapatos.*Bon-Bonite Sitio Oficial$"))

    product_url = catalog.open_first_product()
    expect(page).to_have_url(re.compile(r"/producto/"))
    expect(page.get_by_role("heading", level=1)).to_be_visible()
    assert "/producto/" in product_url, (
        f"Se esperaba una URL de producto; se obtuvo {product_url!r}."
    )
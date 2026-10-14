import re

from playwright.sync_api import expect

from pages.catalog_page import CatalogPage


def test_accessories_category_opens_first_product(page, store_url):
    """Comprueba el catálogo de accesorios y abre su primer producto."""
    catalog = CatalogPage(page, store_url)
    catalog.open_category("accesorios")

    expect(page).to_have_title(re.compile(r"^Accesorios.*Bon-Bonite Sitio Oficial$"))
    product_url = catalog.open_first_product()

    expect(page).to_have_url(product_url)
    expect(page).to_have_url(re.compile(r"/producto/"))
    expect(page.get_by_role("heading", level=1)).to_be_visible()
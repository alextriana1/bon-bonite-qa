import re

from playwright.sync_api import expect

from pages.catalog_page import CatalogPage


def test_bags_category_opens_first_product(page, store_url):
    """Comprueba el catálogo de bolsos y abre el primer bolso listado."""
    catalog = CatalogPage(page, store_url)
    catalog.open_category("bolsos")

    expect(page).to_have_title(re.compile(r"^Bolsos.*Bon-Bonite Sitio Oficial$"))
    product_url = catalog.open_first_product()

    expect(page).to_have_url(product_url)
    expect(page).to_have_url(re.compile(r"/producto/"))
    expect(page.get_by_role("heading", level=1)).to_be_visible()
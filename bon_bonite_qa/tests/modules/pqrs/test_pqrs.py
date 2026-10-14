from datetime import date
import re
from pathlib import Path

import pytest
from playwright.sync_api import expect

from pages.pqrs_page import PQRSPage


@pytest.mark.mutating
def test_pqrs_form_is_submitted(page, store_url):
    """Envía la PQRS de prueba y valida la redirección y el radicado generado."""
    pqrs = PQRSPage(page, store_url)
    attachment_path = (
        Path(__file__).resolve().parents[3]
        / "data"
        / "Hoja de vida Alexander Triana.pdf"
    )
    pqrs.open_pqrs()
    pqrs.accept_cookies()
    pqrs.fill_submission_request(attachment_path)

    expect(pqrs.request_date).to_have_value(date.today().strftime("%d/%m/%Y"))
    expect(pqrs.customer_name).to_have_value("QA Automatizacion")
    expect(pqrs.email).to_have_value("qa.pqrs@example.com")
    expect(page.get_by_text(attachment_path.name, exact=True)).to_be_visible()
    expect(pqrs.privacy_consent).to_be_checked()

    pqrs.submit_request()

    expect(page).to_have_url(
        re.compile(r"/pqrs-radicada/\?codigo=PQRS-[A-Za-z0-9-]+$"),
        timeout=30_000,
    )
    success_heading = page.get_by_role(
        "heading", name="Tu solicitud ha sido enviada con éxito"
    )
    expect(success_heading).to_be_visible(timeout=20_000)

    tracking_heading = page.get_by_role(
        "heading", name=re.compile("Número de radicado")
    )
    expect(tracking_heading).to_be_visible()
    tracking_text = tracking_heading.inner_text()
    assert re.search(r"PQRS-[A-Za-z0-9-]+", tracking_text), (
        f"Se esperaba un número de radicado PQRS; se obtuvo {tracking_text!r}."
    )
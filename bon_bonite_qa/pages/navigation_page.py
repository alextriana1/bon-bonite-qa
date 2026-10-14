from pages.base_page import BasePage


class NavigationPage(BasePage):
    """Rutas disponibles para abrir los módulos principales del sitio."""

    MODULE_PATHS = {
        "zapatos": "/categoria-producto/zapatos-mujer/",
        "bolsos": "/categoria-producto/bolsos-mujer/",
        "cinturones": "/categoria-producto/cinturones-mujer/",
        "accesorios": "/categoria-producto/accesorios-mujer/",
        "outlet": "/categoria-producto/outlet/",
        "pqrs": "/pqrs/",
        "mi_cuenta": "/mi-cuenta/",
        "bonos_regalo": "/producto/bono-de-regalo/",
        "account": "/mi-cuenta/",
    }

    def open_module(self, module: str):
        """Abre el módulo solicitado usando su ruta configurada."""
        self.open(self.MODULE_PATHS[module])
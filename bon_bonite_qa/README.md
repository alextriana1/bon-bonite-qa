# Automatización QA Bon-Bonite

Suite web en Python con pytest, Playwright y Page Object Model (POM). La URL base apunta por defecto a `https://www.bon-bonite.com` y se puede cambiar para usar un ambiente de pruebas.

## Cobertura

1. Acceso a Zapatos, Bolsos, Cinturones, Accesorios, Outlet, PQRS, Mi cuenta/Account y Bonos de regalo.
2. Acceso a categorías y apertura de un producto desde Zapatos.
3. Registro de un usuario nuevo y actualización persistente de sus datos.
4. Login, clic en Zapatos, selección de producto y talla, “Comprar Ahora”, “Finalizar compra”, “Continuar”, facturación y validación de respuesta `success` al realizar el pedido.
5. Aceptación de cookies, llenado y envío del formulario PQRS con el archivo de `data/`, y validación del mensaje de éxito y el número de radicado.

La prueba de compra puede generar una orden y la prueba PQRS envía datos de prueba y el PDF existente en `data/`; ejecútalas solo en un ambiente autorizado.

## Instalación

Desde esta carpeta, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Ejecución

En Windows, puedes abrir `run_test.bat` para elegir un caso individual o ejecutar los 10 casos.

La opción 7 valida un login exitoso. Completa estas variables en `.env` con una cuenta QA existente:

```dotenv
BONBONITE_TEST_DOCUMENT=<documento de la cuenta QA>
BONBONITE_TEST_PASSWORD=<contraseña de la cuenta QA>
```

Ejecutar los módulos públicos (no crea ni modifica datos):

```powershell
python run_tests.py --browser-channel=chrome
```

El navegador se abre en modo visible y las acciones se ralentizan para que puedas observar los pasos. Para ejecutar registro y compra en prebio:

```powershell
python run_tests.py --browser-channel=chrome --run-mutating --bonbonite-url https://www.bon-bonite.com
```

Las pruebas que crean/actualizan una cuenta, agregan productos al carrito o envían el formulario PQRS se omiten por defecto; `--run-mutating` las habilita. El runner oculta la salida detallada de pytest y muestra únicamente los casos ejecutados y aprobados. Conserva un código de salida distinto de cero si hay fallos. Cada corrida escribe el resultado individual de los casos en `resultados_tests.txt`; el informe manual de validación está en [INFORME_PRUEBAS.md](INFORME_PRUEBAS.md).

Al finalizar cada caso ejecutado se guarda una captura de página completa en `evidencias/`, dentro de una carpeta única por corrida. Esta carpeta queda fuera de `test-results/` para conservar las capturas anteriores; si no es posible tomar una, pytest muestra una advertencia sin alterar el resultado del caso.

El registro genera una cédula numérica y correo únicos por ejecución. La compra puede generar una orden; el usuario de prueba queda creado en el ambiente.

## Estructura

```text
pages/         Localizadores y acciones de las páginas (Page Objects)
test_data/     Datos compartidos para escenarios de prueba
tests/         Escenarios y validaciones con asserts
	modules/     Casos agrupados por módulo
conftest.py    Fixtures y configuración compartida de pytest/Playwright
utils/         Configuración general, incluida la URL base
	config.py    URL por defecto desde BONBONITE_BASE_URL
data/          Archivos usados por las pruebas
requirements.txt Dependencias del proyecto
pytest.ini     Configuración y marcas de pytest
run_tests.py   Ejecutor con salida resumida
```
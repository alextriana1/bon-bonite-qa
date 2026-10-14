@echo off
REM Evita mostrar cada comando mientras se ejecuta el archivo.
setlocal
REM Sitúa la ejecución en la carpeta del proyecto, sin importar desde dónde se abra.
cd /d "%~dp0"

REM Usa el intérprete instalado en el entorno virtual del proyecto.
set "PYTHON=%~dp0.venv\Scripts\python.exe"
REM Detiene el proceso si todavía no existe el entorno virtual.
if not exist "%PYTHON%" (
    echo No se encontro el entorno virtual del proyecto:
    echo %PYTHON%
    echo Crea el entorno e instala requirements.txt antes de continuar.
    pause
    exit /b 1
)

:menu
REM Muestra el menú y reinicia la selección en cada vuelta.
cls
set "TEST_CASE="
echo Bon-Bonite - Ejecucion de pruebas
echo.
echo Las pruebas de cuenta, checkout y PQRS pueden crear datos en el sitio.
echo La PQRS adjunta el archivo de data y puede generar un radicado.
echo.
echo  1. inicio de sesion
echo  2. registro y actualizacion de perfil
echo  3. Accesorios
echo  4. Bolsos
echo  5. Cinturones
echo  6. Zapatos
echo  7. Outlet
echo  8. Bono de regalo
echo  9. PQRS
echo 10. Compra
echo 11. Ejecutar los 10 casos
echo  0. Salir
echo.
set /p "OPTION=Selecciona una opcion: "

REM Relaciona cada opción con el test individual que ejecutará pytest.
if "%OPTION%"=="1" set "TEST_CASE=tests/modules/mi_cuenta/test_mi_cuenta.py::test_customer_can_log_in"
if "%OPTION%"=="2" set "TEST_CASE=tests/modules/account/test_account.py::test_customer_can_register_and_update_profile"
if "%OPTION%"=="3" set "TEST_CASE=tests/modules/accesorios/test_accesorios.py::test_accessories_category_opens_first_product"
if "%OPTION%"=="4" set "TEST_CASE=tests/modules/bolsos/test_bolsos.py::test_bags_category_opens_first_product"
if "%OPTION%"=="5" set "TEST_CASE=tests/modules/cinturones/test_cinturones.py::test_belts_category_opens_first_product"
if "%OPTION%"=="6" set "TEST_CASE=tests/modules/zapatos/test_zapatos.py::test_shoes_category_opens_product"
if "%OPTION%"=="7" set "TEST_CASE=tests/modules/outlet/test_outlet.py::test_outlet_category_opens_first_product"
if "%OPTION%"=="8" set "TEST_CASE=tests/modules/gift/test_gift_voucher.py::test_gift_voucher_page_is_reachable"
if "%OPTION%"=="9" set "TEST_CASE=tests/modules/pqrs/test_pqrs.py::test_pqrs_form_is_submitted"
if "%OPTION%"=="10" set "TEST_CASE=tests/modules/checkout/test_checkout.py::test_customer_can_buy_from_shoes_and_place_order"
if "%OPTION%"=="11" goto all_tests
if "%OPTION%"=="0" exit /b 0
if not defined TEST_CASE goto invalid_option
REM Ejecuta el caso seleccionado con Chrome y habilita los escenarios mutantes.
"%PYTHON%" run_tests.py "%TEST_CASE%" --browser-channel=chrome --run-mutating
goto show_result

:all_tests
REM Ejecuta todos los tests recopilados por el proyecto.
"%PYTHON%" run_tests.py --browser-channel=chrome --run-mutating
goto show_result

:invalid_option
REM Informa una selección inválida y vuelve a mostrar el menú.
echo Opcion no valida.
pause
goto menu

:show_result
REM Conserva el código de salida de pytest y orienta sobre el reporte.
set "RESULT=%ERRORLEVEL%"
echo.
if "%RESULT%"=="0" (
    echo La ejecucion termino correctamente.
) else (
    echo La ejecucion termino con fallos. Revisa resultados_tests.txt.
)
pause
exit /b %RESULT%
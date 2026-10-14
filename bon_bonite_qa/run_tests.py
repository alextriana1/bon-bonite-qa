import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path

import pytest


class ResultSummary:
    def __init__(self):
        self.executed = 0
        self.passed = 0
        self.results = {}

    def pytest_runtest_logreport(self, report):
        result = self.results.setdefault(
            report.nodeid,
            {"status": "sin ejecutar", "reason": ""},
        )

        if report.when == "call" or report.failed or report.skipped:
            result["status"] = report.outcome
            if report.failed or report.skipped:
                result["reason"] = self._reason(report)

    @staticmethod
    def _reason(report):
        if report.skipped and isinstance(report.longrepr, tuple) and len(report.longrepr) == 3:
            return str(report.longrepr[2])[:400]

        detail = getattr(report, "longreprtext", "") or str(report.longrepr)
        if "403 Forbidden" in detail:
            return "El sitio respondió HTTP 403 Forbidden al navegador automatizado."

        lines = [line.strip() for line in detail.splitlines() if line.strip()]
        matching_lines = [
            line
            for line in lines
            if "Error:" in line or "AssertionError" in line or "Skipped:" in line
        ]
        reason = matching_lines[-1] if matching_lines else (lines[-1] if lines else "Sin detalle")
        return reason[:400]

    def pytest_sessionfinish(self, session, exitstatus):
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter is None:
            return

        stats = reporter.stats
        passed = stats.get("passed", [])
        failed = stats.get("failed", [])
        errors = stats.get("error", [])
        skipped = stats.get("skipped", [])
        expected_failures = [report for report in skipped if hasattr(report, "wasxfail")]

        self.passed = len(passed)
        self.executed = len(passed) + len(failed) + len(errors) + len(expected_failures)
        self.write_report(stats, len(errors))

    def write_report(self, stats, errors):
        failed = len(stats.get("failed", []))
        skipped = len(stats.get("skipped", []))
        lines = [
            "Resultados de pruebas automatizadas Bon-Bonite",
            f"Fecha: {datetime.now().astimezone().isoformat(timespec='seconds')}",
            f"Casos detectados: {len(self.results)}",
            f"Casos ejecutados: {self.executed}",
            f"Aprobados: {self.passed}",
            f"Rechazados: {failed + errors}",
            f"Omitidos: {skipped}",
            "",
            "Detalle por caso:",
        ]

        for nodeid, result in self.results.items():
            status = result["status"]
            label = {
                "passed": "APROBADO",
                "failed": "RECHAZADO",
                "skipped": "OMITIDO",
            }.get(status, status.upper())
            detail = f" - {result['reason']}" if result["reason"] else ""
            lines.append(f"[{label}] {nodeid}{detail}")

        report_path = Path(__file__).with_name("resultados_tests.txt")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    summary = ResultSummary()
    pytest_args = [
        "-q",
        "--tb=no",
        "--no-header",
        "--no-summary",
        "--headed",
        "--slowmo=700",
        *sys.argv[1:],
    ]

    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        exit_code = pytest.main(pytest_args, plugins=[summary])

    print(f"Casos ejecutados: {summary.executed}")
    print(f"Casos aprobados: {summary.passed}")
    return int(exit_code)


if __name__ == "__main__":
    raise SystemExit(main())
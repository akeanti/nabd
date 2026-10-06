from typer.testing import CliRunner

from nabd import __version__
from nabd.cli import app


def test_version_option_prints_distribution_version() -> None:
    result = CliRunner().invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.output.strip() == f"nabd {__version__}"


def test_invocation_without_arguments_prints_help() -> None:
    result = CliRunner().invoke(app, [])

    assert "Usage" in result.output

from typing import Annotated

import typer

from nabd import __version__

app = typer.Typer(
    name="nabd",
    help="Provisioning, capture, calibration, dataset export, and compliance tools for Nabd nodes.",
    no_args_is_help=True,
    add_completion=False,
)


def _print_version(requested: bool) -> None:
    if requested:
        typer.echo(f"nabd {__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=_print_version, is_eager=True, help="Print the version and exit."
        ),
    ] = False,
) -> None:
    """Nabd command-line tools."""

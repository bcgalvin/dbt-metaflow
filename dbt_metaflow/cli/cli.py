from typing import Optional

import typer
from rich.console import Console

from dbt_metaflow.__about__ import __version__

app = typer.Typer()
console = Console()


def exit_with_version() -> None:
    typer.secho("dbt_metaflow version: %s" % __version__, fg="blue")
    raise typer.Exit


def version_callback(value: bool) -> None:
    if value:
        exit_with_version()


@app.callback(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print metaflow dbt version",
    ),
) -> bool:
    return True

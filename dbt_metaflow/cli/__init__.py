# SPDX-FileCopyrightText: 2024-present Bryan Galvin <bcgalvin@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from dbt_metaflow.__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="dbt-metaflow")
def dbt_metaflow():
    click.echo("Hello world!")

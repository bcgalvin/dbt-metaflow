from typer.testing import CliRunner

from dbt_metaflow.cli.cli import app

runner = CliRunner()


def test_app_entrypoint():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout

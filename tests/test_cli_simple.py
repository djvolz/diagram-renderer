"""
Integration tests for CLI functionality
"""

import subprocess

import pytest
from click.testing import CliRunner

from examples.cli import cli


class TestDashboardCommand:
    """Test dashboard command"""

    @pytest.mark.skip(reason="Dashboard command removed from CLI, now separate script")
    def test_dashboard_help(self):
        """Test dashboard command help"""
        runner = CliRunner()
        result = runner.invoke(cli, ["dashboard", "--help"])

        assert result.exit_code == 0
        assert "Launch the interactive Streamlit dashboard" in result.output


class TestCLIExecution:
    """Test CLI execution via subprocess"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_cli_script_help(self):
        """Test that examples/cli.py can show help"""
        result = subprocess.run(
            ["uv", "run", "python", "examples/cli.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        assert "Diagram Renderer CLI" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling"""

    def test_invalid_command(self):
        """Test invalid command handling"""
        runner = CliRunner()
        result = runner.invoke(cli, ["nonexistent"])

        assert result.exit_code != 0
        assert "No such command" in result.output

"""
Integration tests for simplified CLI functionality
"""
import pytest
import subprocess
import sys
from click.testing import CliRunner
from main import cli


class TestDashboardCommand:
    """Test dashboard command"""
    
    def test_dashboard_help(self):
        """Test dashboard command help"""
        runner = CliRunner()
        result = runner.invoke(cli, ['dashboard', '--help'])
        
        assert result.exit_code == 0
        assert "Launch the Streamlit dashboard" in result.output




class TestCLIExecution:
    """Test CLI execution via subprocess"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_main_script_help(self):
        """Test that main.py can show help"""
        result = subprocess.run(
            ["uv", "run", "main.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        assert "Diagram Renderer CLI" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling"""
    
    def test_invalid_command(self):
        """Test invalid command handling"""
        runner = CliRunner()
        result = runner.invoke(cli, ['nonexistent'])
        
        assert result.exit_code != 0
        assert "No such command" in result.output
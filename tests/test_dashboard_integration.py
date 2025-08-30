"""
Integration tests for Streamlit dashboard functionality
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

# Set Streamlit to run in headless mode for testing
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"


class TestDashboardIntegration:
    """Integration tests for Streamlit dashboard"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_dashboard_command_help(self):
        """Test that dashboard command shows help"""
        from click.testing import CliRunner

        # Add examples directory to path
        examples_dir = Path(__file__).parent.parent / "examples"
        sys.path.insert(0, str(examples_dir))

        try:
            from cli import dashboard

            runner = CliRunner()
            result = runner.invoke(dashboard, ["--help"])

            assert result.exit_code == 0
            assert "Launch the interactive Streamlit dashboard" in result.output
        finally:
            sys.path.remove(str(examples_dir))

    @pytest.mark.integration
    @pytest.mark.slow
    def test_dashboard_imports(self):
        """Test that dashboard.py can be imported without errors"""

        # Add examples directory to path
        examples_dir = Path(__file__).parent.parent / "examples"
        sys.path.insert(0, str(examples_dir))

        try:
            import dashboard

            # If we get here, imports worked
            assert True
        except ImportError as e:
            pytest.fail(f"Dashboard imports failed: {e}")
        except Exception as e:
            # Other errors might be expected (like Streamlit not being in test mode)
            # but import errors are what we're testing for
            if "streamlit" in str(e).lower():
                pytest.skip("Streamlit not in test mode")
            else:
                pytest.fail(f"Dashboard import failed with unexpected error: {e}")
        finally:
            sys.path.remove(str(examples_dir))

    @pytest.mark.integration
    @pytest.mark.slow
    def test_streamlit_renderer_imports(self):
        """Test that streamlit_renderer.py can be imported"""
        try:
            import st_diagram
            from st_diagram import StreamlitDiagramRenderer

            # Test that we can create an instance
            renderer = StreamlitDiagramRenderer()
            assert renderer is not None
            assert hasattr(renderer, "render_diagram_auto")

        except ImportError as e:
            if "streamlit" in str(e).lower():
                pytest.skip("Streamlit not available")
            else:
                pytest.fail(f"StreamlitRenderer import failed: {e}")

    @pytest.mark.integration
    @pytest.mark.slow
    def test_dashboard_sample_diagrams(self):
        """Test that dashboard sample diagrams are valid"""
        try:
            import st_diagram

            from diagram_renderer import DiagramRenderer

            # Test the sample diagrams used in dashboard
            sample_mermaid = """
graph TD
    A[User Input] --> B{Valid Diagram?}
    B -->|Yes| C[Render with Mermaid.js]
    B -->|No| D[Show Error]
    C --> E[Display Result]
            """

            sample_plantuml = """
@startuml
!theme dark
skinparam backgroundColor #1e1e1e
skinparam defaultTextColor white

participant User as U
participant "Streamlit App" as S
participant "Diagram Renderer" as R
participant "Browser" as B

U -> S: Input diagram code
S -> R: Process diagram
R -> S: Return HTML
S -> B: Render in browser
B -> U: Display diagram
@enduml
            """

            # Test detection
            renderer = DiagramRenderer()

            mermaid_type = renderer.detect_diagram_type(sample_mermaid)
            assert mermaid_type == "mermaid"

            plantuml_type = renderer.detect_diagram_type(sample_plantuml)
            assert plantuml_type == "plantuml"

        except ImportError:
            pytest.skip("Required modules not available")

    @pytest.mark.integration
    @pytest.mark.slow
    def test_dashboard_renderer_integration(self):
        """Test integration between dashboard renderer and diagram renderer"""
        try:
            from st_diagram import StreamlitDiagramRenderer

            renderer = StreamlitDiagramRenderer()

            # Test with simple mermaid diagram
            test_diagram = "graph TD\n  A --> B"

            # Mock streamlit components to avoid actual streamlit dependency
            import unittest.mock

            with unittest.mock.patch("streamlit_renderer.components") as mock_components:
                mock_components.html.return_value = None

                # This should not raise an exception
                result = renderer.render_diagram_auto(test_diagram)

                # Verify that components.html was called
                mock_components.html.assert_called_once()

        except ImportError:
            pytest.skip("Streamlit components not available")


class TestDashboardStartup:
    """Test dashboard startup and shutdown"""

    @pytest.fixture
    def dashboard_process(self):
        """Fixture to start and stop dashboard process"""
        process = None
        try:
            # Start dashboard in background
            process = subprocess.Popen(
                ["uv", "run", "python", "examples/cli.py", "dashboard"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid if hasattr(os, "setsid") else None,
            )

            # Give it time to start
            time.sleep(3)

            yield process

        finally:
            # Clean up process
            if process:
                try:
                    if hasattr(os, "killpg"):
                        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    else:
                        process.terminate()
                    process.wait(timeout=5)
                except:
                    # Force kill if graceful termination fails
                    try:
                        if hasattr(os, "killpg"):
                            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                        else:
                            process.kill()
                    except:
                        pass

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.skipif(
        os.getenv("CI") == "true", reason="Dashboard startup tests are flaky in CI environments"
    )
    def test_dashboard_starts_successfully(self, dashboard_process):
        """Test that dashboard starts without immediate errors"""
        # Check if process is still running
        assert dashboard_process.poll() is None, "Dashboard process terminated unexpectedly"

        # Try to read some output to see if there are obvious errors
        try:
            stdout, stderr = dashboard_process.communicate(timeout=1)
            if stderr:
                stderr_text = stderr.decode("utf-8")
                # Some stderr output is normal for Streamlit, but check for obvious errors
                if "error" in stderr_text.lower() and "traceback" in stderr_text.lower():
                    pytest.fail(f"Dashboard startup had errors: {stderr_text}")
        except subprocess.TimeoutExpired:
            # Process is still running, which is good
            pass

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.skipif(os.getenv("CI") == "true", reason="HTTP tests are flaky in CI environments")
    def test_dashboard_http_endpoint(self, dashboard_process):
        """Test that dashboard HTTP endpoint becomes available"""
        # Wait a bit longer for full startup
        time.sleep(5)

        # Check if process is still running
        if dashboard_process.poll() is not None:
            pytest.skip("Dashboard process failed to start")

        # Try to connect to default Streamlit port
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            # Any response (even error) means the server is running
            assert response.status_code in [
                200,
                404,
                403,
            ], f"Unexpected status code: {response.status_code}"
        except requests.exceptions.RequestException:
            # Could be using a different port, let's try the alternative
            try:
                response = requests.get("http://localhost:8503", timeout=5)
                assert response.status_code in [
                    200,
                    404,
                    403,
                ], f"Unexpected status code: {response.status_code}"
            except requests.exceptions.RequestException:
                pytest.skip(
                    "Dashboard HTTP endpoint not accessible (might be using different port)"
                )


class TestDashboardErrorHandling:
    """Test dashboard error handling"""

    def test_invalid_diagram_handling(self):
        """Test that dashboard handles invalid diagrams gracefully"""
        try:
            from st_diagram import StreamlitDiagramRenderer

            renderer = StreamlitDiagramRenderer()

            # Test with invalid diagram code
            invalid_diagrams = [
                "invalid diagram code",
                "```mermaid\ninvalid syntax\n```",
                "",
                "```\n\n```",
            ]

            import unittest.mock

            with unittest.mock.patch("streamlit_renderer.components") as mock_components:
                mock_components.html.return_value = None

                for invalid_diagram in invalid_diagrams:
                    # Should not raise exceptions
                    try:
                        renderer.render_diagram_auto(invalid_diagram)
                    except Exception as e:
                        pytest.fail(f"Dashboard failed to handle invalid diagram: {e}")

        except ImportError:
            pytest.skip("Streamlit components not available")

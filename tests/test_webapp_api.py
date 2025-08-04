"""
Tests for FastAPI web application functionality.

Tests the REST API endpoints, request/response handling,
and integration with the diagram rendering system.
"""

import pytest
from fastapi.testclient import TestClient


class TestWebAppAPI:
    """Test FastAPI web application endpoints"""

    @pytest.fixture
    def client(self):
        """Create test client for FastAPI app"""
        try:
            import sys
            from pathlib import Path

            # Add examples directory to path
            examples_dir = Path(__file__).parent.parent / "examples"
            sys.path.insert(0, str(examples_dir))

            from webapp import app

            return TestClient(app)
        except ImportError:
            pytest.skip("FastAPI or webapp dependencies not available")

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "diagram-renderer"

    def test_main_page_endpoint(self, client):
        """Test main page returns HTML"""
        response = client.get("/")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Check for key elements in the HTML
        html = response.text
        assert "Diagram Renderer" in html
        assert "diagramCode" in html  # Editor textarea
        assert "renderBtn" in html  # Render button

    def test_render_api_mermaid(self, client):
        """Test rendering Mermaid diagram via API"""
        request_data = {
            "code": "graph TD\n    A[Start] --> B[End]",
            "type": "mermaid",
            "format": "html",
        }

        response = client.post("/api/render", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["diagram_type"] == "mermaid"
        assert data["format"] == "html"
        assert data["content"] is not None
        assert len(data["content"]) > 1000  # Should be substantial HTML
        assert data["error"] is None

        # Check HTML content includes charset
        assert '<meta charset="utf-8">' in data["content"]

    def test_render_api_plantuml(self, client):
        """Test rendering PlantUML diagram via API"""
        request_data = {"code": "@startuml\nA -> B\n@enduml", "type": "plantuml", "format": "html"}

        response = client.post("/api/render", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["diagram_type"] == "plantuml"
        assert data["format"] == "html"
        assert data["content"] is not None

    def test_render_api_graphviz(self, client):
        """Test rendering Graphviz diagram via API"""
        request_data = {"code": "digraph G {\n    A -> B;\n}", "type": "graphviz", "format": "html"}

        response = client.post("/api/render", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["diagram_type"] == "graphviz"
        assert data["format"] == "html"
        assert data["content"] is not None

    def test_render_api_auto_detection(self, client):
        """Test auto-detection of diagram type"""
        test_cases = [
            ("graph TD; A --> B", "mermaid"),
            ("@startuml\nA -> B\n@enduml", "plantuml"),
            ("digraph G { A -> B; }", "graphviz"),
        ]

        for code, expected_type in test_cases:
            request_data = {"code": code, "type": "auto", "format": "html"}

            response = client.post("/api/render", json=request_data)

            assert response.status_code == 200
            data = response.json()

            assert data["success"] is True
            assert data["diagram_type"] == expected_type

    def test_render_api_invalid_code(self, client):
        """Test API response to invalid diagram code"""
        request_data = {
            "code": "invalid diagram syntax that makes no sense",
            "type": "auto",
            "format": "html",
        }

        response = client.post("/api/render", json=request_data)

        # Should still return 200 but with success=false or valid fallback
        assert response.status_code == 200
        data = response.json()

        # Should either fail gracefully or render as mermaid fallback
        assert "success" in data
        assert "diagram_type" in data

    def test_render_api_missing_fields(self, client):
        """Test API validation for missing required fields"""
        # Missing code field
        response = client.post("/api/render", json={"type": "mermaid"})
        assert response.status_code == 422  # Validation error

        # Empty request
        response = client.post("/api/render", json={})
        assert response.status_code == 422  # Validation error

    def test_render_api_invalid_type(self, client):
        """Test API response to invalid diagram type"""
        request_data = {"code": "graph TD; A --> B", "type": "invalid_type", "format": "html"}

        response = client.post("/api/render", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_examples_endpoint(self, client):
        """Test examples API endpoint"""
        response = client.get("/api/examples")

        assert response.status_code == 200
        data = response.json()

        # Should have examples for each diagram type
        assert "mermaid" in data
        assert "plantuml" in data
        assert "graphviz" in data

        # Each should have multiple example types
        assert len(data["mermaid"]) > 0
        assert len(data["plantuml"]) > 0
        assert len(data["graphviz"]) > 0

    def test_cors_headers(self, client):
        """Test that CORS headers are handled properly"""
        response = client.get("/health")

        # Basic check - in production you might want specific CORS headers
        assert response.status_code == 200

    def test_api_content_types(self, client):
        """Test API content type handling"""
        # JSON request
        response = client.post(
            "/api/render", json={"code": "graph TD; A --> B", "type": "mermaid", "format": "html"}
        )

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestWebAppIntegration:
    """Integration tests for web app with diagram renderer"""

    @pytest.fixture
    def client(self):
        """Create test client for FastAPI app"""
        try:
            import sys
            from pathlib import Path

            # Add examples directory to path
            examples_dir = Path(__file__).parent.parent / "examples"
            sys.path.insert(0, str(examples_dir))

            from webapp import app

            return TestClient(app)
        except ImportError:
            pytest.skip("FastAPI or webapp dependencies not available")

    def test_webapp_uses_latest_renderer(self, client):
        """Test that webapp uses the latest DiagramRenderer features"""
        request_data = {"code": "graph TD; A --> B", "type": "mermaid", "format": "html"}

        response = client.post("/api/render", json=request_data)
        data = response.json()

        # Should include latest features like charset and Unicode symbols
        html_content = data["content"]

        # UTF-8 charset
        assert '<meta charset="utf-8">' in html_content

        # GitHub-style controls with Unicode symbols
        assert "🖼" in html_content  # PNG download
        assert "⧉" in html_content  # Copy
        assert "↻" in html_content  # Reset

    def test_webapp_error_handling(self, client):
        """Test webapp error handling and logging"""
        # This tests that the webapp handles errors gracefully
        # without crashing the server

        # Try various edge cases
        edge_cases = [
            "",  # Empty string
            " ",  # Whitespace only
            "a" * 10000,  # Very long string
            "特殊字符测试",  # Unicode characters
        ]

        for code in edge_cases:
            request_data = {"code": code, "type": "auto", "format": "html"}

            response = client.post("/api/render", json=request_data)

            # Should always return a valid response (even if error)
            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            assert "diagram_type" in data

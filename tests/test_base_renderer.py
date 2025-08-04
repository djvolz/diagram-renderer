"""
Tests for the base renderer functionality
"""

import pytest

from diagram_renderer.renderers.base import BaseRenderer


class MockRenderer(BaseRenderer):
    """Mock renderer for testing base functionality"""

    def render_html(self, code, **kwargs):
        return f"<html>Mock HTML for: {code}</html>"

    def render_bytes(self, code, **kwargs):
        return f"Mock bytes for: {code}".encode()

    def clean_code(self, code):
        return code.strip()


class TestBaseRenderer:
    """Test cases for BaseRenderer base class"""

    def test_init(self):
        """Test BaseRenderer initialization"""
        renderer = MockRenderer()

        # The static dir should be relative to the diagram module
        assert renderer.static_dir.name == "static"
        assert "diagram" in str(renderer.static_dir)
        assert renderer.use_local_rendering is True

    def test_abstract_methods_implemented(self):
        """Test that abstract methods are properly implemented in mock"""
        renderer = MockRenderer()

        # These should not raise NotImplementedError
        result = renderer.render_html("test code")
        assert "Mock HTML" in result

        result = renderer.render_bytes("test code")
        assert b"Mock bytes" in result

        result = renderer.clean_code("  test  ")
        assert result == "test"

    def test_detect_diagram_type_default(self):
        """Test default detect_diagram_type returns False"""
        renderer = MockRenderer()

        result = renderer.detect_diagram_type("any code")
        assert result is False

    def test_get_static_js_content_missing_file(self):
        """Test get_static_js_content with non-existent file"""
        renderer = MockRenderer()

        result = renderer.get_static_js_content("nonexistent.js")
        assert result is None

    @pytest.mark.requires_js
    def test_get_static_js_content_existing_file(self, static_js_exists):
        """Test get_static_js_content with existing file"""
        if not static_js_exists["mermaid"]:
            pytest.skip("Mermaid.js file not found")

        renderer = MockRenderer()

        result = renderer.get_static_js_content("mermaid.min.js")
        assert result is not None
        assert len(result) > 0
        assert "mermaid" in result.lower()

    def test_inheritance_structure(self):
        """Test that BaseRenderer follows proper inheritance"""
        from abc import ABC

        assert issubclass(BaseRenderer, ABC)

        # Verify that direct instantiation raises TypeError
        with pytest.raises(TypeError):
            BaseRenderer()


class TestAbstractMethods:
    """Test cases for abstract methods in BaseRenderer"""

    def test_missing_render_html_raises_error(self):
        """Test that missing render_html implementation raises TypeError"""

        class IncompleteRenderer(BaseRenderer):
            def clean_code(self, code):
                return code

        with pytest.raises(TypeError):
            IncompleteRenderer()

    def test_missing_clean_code_raises_error(self):
        """Test that missing clean_code implementation raises TypeError"""

        class IncompleteRenderer(BaseRenderer):
            def render_html(self, code, **kwargs):
                return "test"

        with pytest.raises(TypeError):
            IncompleteRenderer()

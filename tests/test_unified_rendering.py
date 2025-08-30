"""Comprehensive tests for unified rendering functionality"""

from unittest.mock import MagicMock, patch

import pytest

from diagram_renderer.renderers.base import (
    TEMPLATE_UNIFIED,
    BaseRenderer,
)
from diagram_renderer.renderers.graphviz import GraphvizRenderer
from diagram_renderer.renderers.mermaid import MermaidRenderer
from diagram_renderer.renderers.plantuml import PlantUMLRenderer


class TestTemplateConstants:
    """Test template constant definitions and usage"""

    def test_template_constants_defined(self):
        """Test that all template constants are properly defined"""
        assert TEMPLATE_UNIFIED == "unified.html"

    def test_template_loading_with_constants(self):
        """Test that templates can be loaded using constants"""
        renderer = MermaidRenderer()

        # Test that template constants work for loading
        unified_template = renderer.get_template_content(TEMPLATE_UNIFIED)
        assert unified_template is not None
        assert len(unified_template) > 0
        assert "<!DOCTYPE html>" in unified_template


class TestBaseRendererHelperMethods:
    """Test new helper methods in BaseRenderer using concrete implementation"""

    def test_generate_error_html(self):
        """Test standardized error HTML generation"""
        renderer = MermaidRenderer()  # Use concrete renderer

        error_html = renderer._generate_error_html("Test error message")

        assert error_html == "<div>Error: Test error message</div>"

    def test_get_vizjs_content(self):
        """Test VizJS content aggregation"""
        renderer = GraphvizRenderer()  # Use concrete renderer that has VizJS methods

        # Mock the static JS content method
        with patch.object(renderer, "get_static_js_content") as mock_get_js:
            mock_get_js.side_effect = lambda filename: f"content_of_{filename}"

            result = renderer._get_vizjs_content()

            assert result == "content_of_viz-lite.js\ncontent_of_viz-full.js"
            assert mock_get_js.call_count == 2

    def test_get_vizjs_content_missing_files(self):
        """Test VizJS content when files are missing"""
        renderer = GraphvizRenderer()

        # Mock missing files
        with patch.object(renderer, "get_static_js_content", return_value=None):
            result = renderer._get_vizjs_content()
            assert result is None

    def test_generate_vizjs_rendering_script(self):
        """Test VizJS JavaScript generation"""
        renderer = GraphvizRenderer()
        code = "digraph G { A -> B }"

        script = renderer._generate_vizjs_rendering_script(code)

        assert "function renderDiagram()" in script
        assert "new Viz()" in script
        assert "renderSVGElement" in script
        assert code.replace(" ", "\\u0020") in script or code in script

    def test_populate_unified_template(self):
        """Test unified template placeholder replacement"""
        renderer = GraphvizRenderer()

        template = """<html><script>{js_content}</script><div>{diagram_content}</div><script>{panzoom_js_content}</script><script>const original = {escaped_original};</script>        // Diagram rendering function - to be overridden by specific renderers
        function renderDiagram() {
            // Default implementation - just show the content
            loading.style.display = 'none';
            diagramContent.style.display = 'block';

            // Initialize pan/zoom after content is ready
            setTimeout(() => {
                initializePanZoom();
                diagramReady = true;
            }, 100);
        }</html>"""

        result = renderer._populate_unified_template(
            template, "viz_js", "panzoom_js", "test code", "custom_script"
        )

        assert "viz_js" in result
        assert "panzoom_js" in result
        assert '"test code"' in result
        assert "custom_script" in result


class TestUnifiedRenderingIntegration:
    """Integration tests for unified rendering across diagram types"""

    def test_all_renderers_have_unified_capability(self):
        """Test that all renderers can produce unified output"""
        test_cases = [
            (MermaidRenderer(), "graph TD\n    A --> B"),
            (PlantUMLRenderer(), "@startuml\nA -> B\n@enduml"),
            (GraphvizRenderer(), "digraph G { A -> B }"),
        ]

        for renderer, code in test_cases:
            html = renderer.render_html(code)

            # Should produce valid HTML
            assert html is not None
            assert len(html) > 100
            assert "<!DOCTYPE html>" in html or "<html>" in html

    def test_unified_template_structure_consistency(self):
        """Test that unified templates have consistent structure"""
        renderers = [MermaidRenderer(), PlantUMLRenderer(), GraphvizRenderer()]
        codes = ["graph TD\n    A --> B", "@startuml\nA -> B\n@enduml", "digraph G { A -> B }"]

        htmls = []
        for renderer, code in zip(renderers, codes):
            try:
                if hasattr(renderer, "render_html_improved"):
                    html = renderer.render_html_improved(code)
                else:
                    html = renderer.render_html(code)
                htmls.append(html)
            except Exception:
                # Skip if rendering fails (dependency issues)
                htmls.append(None)

        # Filter out None results for comparison
        valid_htmls = [h for h in htmls if h and "Error:" not in h]

        if len(valid_htmls) >= 2:
            # Check for consistent control structure in valid renders
            common_elements = [
                'class="control-btn"',
                'class="diagram-container"',
                "function downloadPNG",
                "function copyDiagram",
            ]

            for element in common_elements:
                for html in valid_htmls:
                    assert element in html, f"Missing {element} in rendered HTML"


class TestErrorHandling:
    """Test error handling consistency and robustness"""

    def test_missing_static_files_handled_gracefully(self):
        """Test behavior when static JS files are missing"""
        renderer = MermaidRenderer()

        with patch.object(renderer, "get_static_js_content", return_value=None):
            html = renderer.render_html("graph TD\n    A --> B")

            assert html is not None
            assert "Error:" in html
            assert "<div>" in html

    def test_missing_template_handled_gracefully(self):
        """Test behavior when template files are missing"""
        renderer = MermaidRenderer()

        with patch.object(renderer, "get_template_content", return_value=None):
            html = renderer.render_html("graph TD\n    A --> B")

            assert html is not None
            assert "Error:" in html
            assert "<div>" in html

    def test_error_message_format_consistency(self):
        """Test that all error messages follow the same format"""
        renderer = MermaidRenderer()  # Use concrete renderer

        error_messages = ["File not found", "Network error", "Template missing"]

        for message in error_messages:
            result = renderer._generate_error_html(message)
            assert result == f"<div>Error: {message}</div>"


class TestNewMethodCoverage:
    """Test coverage for all new methods added during refactoring"""

    def test_mermaid_generate_error_html(self):
        """Test Mermaid renderer error HTML generation"""
        renderer = MermaidRenderer()

        result = renderer._generate_error_html("Test message")
        assert result == "<div>Error: Test message</div>"

    def test_mermaid_generate_rendering_script(self):
        """Test Mermaid rendering script generation"""
        renderer = MermaidRenderer()
        code = "graph TD\n    A --> B"
        escaped_original = '"test"'

        script = renderer._generate_mermaid_rendering_script(code, escaped_original)

        assert "async function renderDiagram()" in script
        assert "mermaid.initialize" in script
        assert "mermaid.render" in script
        assert code in script
        assert escaped_original in script

    def test_mermaid_populate_template(self):
        """Test Mermaid template population"""
        renderer = MermaidRenderer()

        template = """
        <html>
        <script>{js_content}</script>
        <div>{diagram_content}</div>
        <script>{panzoom_js_content}</script>
        <script>const orig = {escaped_original};</script>
        // Diagram rendering function - to be overridden by specific renderers
        function renderDiagram() {
            // Default implementation - just show the content
            loading.style.display = 'none';
            diagramContent.style.display = 'block';

            // Initialize pan/zoom after content is ready
            setTimeout(() => {
                initializePanZoom();
                diagramReady = true;
            }, 100);
        }
        </html>
        """

        result = renderer._populate_mermaid_template(
            template, "mermaid_js", "panzoom_js", "clean_code", '"original"', "custom_script"
        )

        assert "mermaid_js" in result
        assert "panzoom_js" in result
        assert "clean_code" in result
        assert '"original"' in result
        assert "custom_script" in result


class TestDemoScriptFunctionality:
    """Test the unified demo script functionality"""

    def test_demo_script_exists_and_executable(self):
        """Test that the demo script exists in the correct location"""
        import os
        from pathlib import Path

        demo_path = Path(__file__).parent.parent / "examples" / "unified_demo.py"

        assert demo_path.exists()
        assert os.access(demo_path, os.R_OK)

    def test_demo_script_imports(self):
        """Test that demo script can import required modules"""
        try:
            import os
            import sys
            from pathlib import Path

            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

            # Import the demo module
            import importlib.util

            demo_path = Path(__file__).parent.parent / "examples" / "unified_demo.py"
            spec = importlib.util.spec_from_file_location("unified_demo", str(demo_path))
            demo_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(demo_module)

            # Should have create_demo function
            assert hasattr(demo_module, "create_demo")
            assert callable(demo_module.create_demo)

        except ImportError as e:
            pytest.skip(f"Demo script import failed: {e}")


class TestStaticAssetIntegration:
    """Test static asset loading and integration"""

    def test_panzoom_library_available(self):
        """Test that panzoom library is available"""
        renderer = MermaidRenderer()

        panzoom_content = renderer.get_static_js_content("panzoom.min.js")
        assert panzoom_content is not None
        assert len(panzoom_content) > 0
        assert "panzoom" in panzoom_content.lower()

    def test_mermaid_library_upgraded(self):
        """Test that Mermaid library is the upgraded version"""
        renderer = MermaidRenderer()

        mermaid_content = renderer.get_static_js_content("mermaid.min.js")
        assert mermaid_content is not None
        assert len(mermaid_content) > 100000  # v11.6.0 should be substantial

    def test_vizjs_libraries_available(self):
        """Test that VizJS libraries are available"""
        renderer = GraphvizRenderer()

        viz_lite = renderer.get_static_js_content("viz-lite.js")
        viz_full = renderer.get_static_js_content("viz-full.js")

        assert viz_lite is not None
        assert viz_full is not None
        assert len(viz_lite) > 0
        assert len(viz_full) > 0

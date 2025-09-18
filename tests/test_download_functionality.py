"""
Tests for PNG download and interactive functionality
"""

import pytest

from diagram_renderer import DiagramRenderer


class TestInteractiveControls:
    """Test interactive control functionality in rendered HTML"""

    def test_mermaid_interactive_controls_present(self):
        """Test that Mermaid diagrams include interactive controls"""
        renderer = DiagramRenderer()

        mermaid_code = """
        graph TD
            A[Start] --> B{Decision}
            B -->|Yes| C[Action 1]
            B -->|No| D[Action 2]
        """

        html = renderer.render_diagram_auto(mermaid_code)

        # Check for main control elements (based on actual UI)
        assert 'onclick="downloadPNG()' in html
        assert 'onclick="copyDiagram()' in html
        assert 'onclick="toggleHelp()' in html
        assert 'onclick="resetView()' in html
        assert 'onclick="toggleFullscreen()' in html

        # Check for proper icons (updated to match actual implementation)
        assert "↓" in html  # Download arrow
        assert "⧉" in html  # Copy icon
        assert "?" in html  # Help icon

    def test_graphviz_interactive_controls_present(self):
        """Test that Graphviz diagrams include interactive controls"""
        renderer = DiagramRenderer()

        dot_code = """
        digraph G {
            A -> B;
            B -> C;
        }
        """

        html = renderer.render_diagram_auto(dot_code)

        # Check for same control elements
        assert 'onclick="downloadPNG()' in html
        assert 'onclick="copyDiagram()' in html
        assert 'onclick="toggleHelp()' in html
        assert 'onclick="resetView()' in html
        assert 'onclick="toggleFullscreen()' in html

    def test_panzoom_integration(self):
        """Test that panzoom library is properly integrated"""
        renderer = DiagramRenderer()

        mermaid_code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(mermaid_code)

        # Check for panzoom functionality
        assert "panzoom" in html.lower()
        assert "initializePanZoom" in html
        assert "panzoomInstance" in html
        assert "getTransform" in html

    def test_keyboard_shortcuts_present(self):
        """Test that keyboard shortcuts are implemented"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for keyboard event handling
        assert "addEventListener('keydown'" in html
        assert "case '+':" in html or "case '='" in html  # Zoom in
        assert "case '-':" in html  # Zoom out
        assert "case '0':" in html  # Reset
        assert "case 'f':" in html or "case 'F':" in html  # Fullscreen
        assert "case '?':" in html  # Help


class TestDownloadFunctionality:
    """Test PNG download functionality"""

    def test_png_download_javascript_present(self):
        """Test that PNG download JavaScript functions are included"""
        renderer = DiagramRenderer()

        mermaid_code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(mermaid_code)

        # Check for downloadPNG function
        assert "function downloadPNG()" in html
        assert "canvas.toDataURL" in html
        assert "image/png" in html

    def test_copy_diagram_functionality(self):
        """Test copy to clipboard functionality"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for copy functionality
        assert "function copyDiagram()" in html
        assert "navigator.clipboard.writeText" in html
        assert "copy-feedback" in html

    def test_help_modal_functionality(self):
        """Test help modal implementation"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for help modal
        assert "function toggleHelp()" in html
        assert 'id="help-modal"' in html
        assert "Keyboard Shortcuts" in html
        assert "Mouse Drag" in html

    def test_fullscreen_functionality(self):
        """Test fullscreen toggle functionality"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for fullscreen functionality
        assert "function toggleFullscreen()" in html
        assert "requestFullscreen" in html
        assert "exitFullscreen" in html

    def test_zoom_reset_functionality(self):
        """Test zoom reset functionality"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for reset functionality
        assert "function resetView()" in html
        assert "panzoomInstance.reset" in html or "panzoomInstance.zoom" in html


class TestTemplateStructure:
    """Test HTML template structure and CSS"""

    def test_unified_template_css_structure(self):
        """Test that unified template has proper CSS structure"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for main CSS classes
        css_classes = [
            "diagram-container",
            "top-controls",
            "bottom-controls",
            "control-group",
            "control-btn",
        ]

        for css_class in css_classes:
            assert f'class="{css_class}"' in html, f"Missing CSS class: {css_class}"

    def test_responsive_design_elements(self):
        """Test responsive design elements are present"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for viewport and responsive elements
        assert 'name="viewport"' in html
        assert "min-width:" in html
        assert "max-width:" in html
        assert "@media" in html or "width: 100%" in html

    def test_control_tooltips_present(self):
        """Test that control tooltips are properly implemented"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Check for tooltip attributes
        tooltips = [
            'title="Download PNG"',
            'title="Copy Source"',
            'title="Keyboard Shortcuts"',
            'title="Reset View"',
            'title="Fullscreen"',
        ]

        for tooltip in tooltips:
            assert tooltip in html, f"Missing tooltip: {tooltip}"


class TestStaticAssets:
    """Test static asset integration"""

    def test_mermaid_library_upgraded(self):
        """Test that Mermaid library is upgraded version"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Should include substantial Mermaid.js content (v11.6.0)
        mermaid_sections = html.split("// Mermaid.js")
        assert len(mermaid_sections) > 1 or "mermaid" in html.lower()

    def test_panzoom_library_integrated(self):
        """Test that panzoom library is properly integrated"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Should include panzoom functionality
        assert "panzoom" in html.lower()
        assert any(keyword in html for keyword in ["Panzoom", "panzoom(", "new Panzoom"])

    def test_no_external_dependencies(self):
        """Test that all dependencies are bundled (no CDN links)"""
        renderer = DiagramRenderer()

        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)

        # Should not have external script sources
        external_patterns = [
            "cdn.jsdelivr.net",
            "unpkg.com",
            "cdnjs.cloudflare.com",
            "googleapis.com",
            'src="http',
            "src='http",
        ]

        for pattern in external_patterns:
            assert pattern not in html, f"Found external dependency: {pattern}"


class TestErrorHandlingRobustness:
    """Test error handling in various scenarios"""

    def test_missing_js_libraries_handled(self):
        """Test behavior when JavaScript libraries are missing"""
        from unittest.mock import patch

        renderer = DiagramRenderer()

        # Get the mermaid renderer from the renderers list
        mermaid_renderer = next(r for name, r in renderer.renderers if name == "mermaid")
        with patch.object(mermaid_renderer, "get_static_js_content", return_value=None):
            html = renderer.render_diagram_auto("graph TD; A-->B")

            # Should handle missing libraries gracefully
            assert html is not None
            # Check for error indicators in the new template
            assert "JavaScript Library Missing" in html or "error" in html.lower()

    def test_invalid_diagram_code_handled(self):
        """Test handling of invalid diagram code"""
        renderer = DiagramRenderer()

        # Test empty code - should return None
        html = renderer.render_diagram_auto("")
        assert html is None

        # Test other codes - should produce HTML (with fallback to Mermaid)
        test_codes = [
            "invalid syntax here",  # Invalid (fallback to Mermaid)
            "graph TD\n    A --->>>> B",  # Malformed Mermaid
            "digraph { A -> }",  # Incomplete Graphviz
        ]

        for code in test_codes:
            html = renderer.render_diagram_auto(code)
            # Should not crash and should produce HTML
            assert html is not None
            assert len(html) > 10

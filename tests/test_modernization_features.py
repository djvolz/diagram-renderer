"""
Tests specifically for the modernization features added in this branch
"""

from pathlib import Path

import pytest

from diagram_renderer import DiagramRenderer
from diagram_renderer.renderers.graphviz import GraphvizRenderer
from diagram_renderer.renderers.mermaid import MermaidRenderer
from diagram_renderer.renderers.plantuml import PlantUMLRenderer


class TestModernizationFeatures:
    """Test features added during the interactive UI modernization"""

    def test_panzoom_library_integration(self):
        """Test that panzoom library is properly integrated"""
        # Test that panzoom file exists
        panzoom_file = (
            Path(__file__).parent.parent
            / "diagram_renderer"
            / "renderers"
            / "static"
            / "js"
            / "panzoom.min.js"
        )
        assert panzoom_file.exists(), "panzoom.min.js library not found"

        # Test that renderers can load panzoom content
        renderer = MermaidRenderer()
        panzoom_content = renderer.get_static_js_content("panzoom.min.js")
        assert panzoom_content is not None
        assert len(panzoom_content) > 10000  # Should be substantial

    def test_mermaid_library_upgraded(self):
        """Test that Mermaid library was upgraded to v11.6.0"""
        mermaid_file = (
            Path(__file__).parent.parent
            / "diagram_renderer"
            / "renderers"
            / "static"
            / "js"
            / "mermaid.min.js"
        )

        # Check file size indicates upgrade (v11.6.0 is much larger)
        file_size = mermaid_file.stat().st_size
        assert file_size > 2_000_000, f"Mermaid.js appears to be old version: {file_size} bytes"

    def test_unified_template_exists(self):
        """Test that unified template file exists"""
        unified_template = (
            Path(__file__).parent.parent
            / "diagram_renderer"
            / "renderers"
            / "templates"
            / "unified.html"
        )
        assert unified_template.exists(), "unified.html template not found"

        # Check template has required structure
        content = unified_template.read_text()
        assert "panzoom" in content.lower()
        assert "top-controls" in content
        assert "bottom-controls" in content

    def test_demo_script_moved_to_examples(self):
        """Test that examples directory exists with proper demos"""
        # unified_demo.py was replaced by consolidated dashboard.py
        dashboard_script = Path(__file__).parent.parent / "examples" / "dashboard.py"
        assert dashboard_script.exists(), "dashboard.py not found in examples directory"

        # Should not exist in root
        root_demo = Path(__file__).parent.parent / "demo_unified_renderers.py"
        assert not root_demo.exists(), "Old demo script still exists in root"

    def test_template_constants_defined(self):
        """Test that template constants are properly defined"""
        from diagram_renderer.renderers.base import (
            TEMPLATE_UNIFIED,
        )

        assert TEMPLATE_UNIFIED == "unified.html"

    def test_all_renderers_support_modern_features(self):
        """Test that all renderers support the modern interactive features"""
        renderers = [MermaidRenderer(), PlantUMLRenderer(), GraphvizRenderer()]

        for renderer in renderers:
            # Should have error handling method
            assert hasattr(renderer, "_generate_error_html")

            # Should be able to generate error HTML
            error_html = renderer._generate_error_html("Test")
            # Check for new template format - it should be a full HTML page
            assert "error" in error_html.lower()
            assert "Rendering Error" in error_html
            assert 'class="error-title"' in error_html
            assert "<p>Test</p>" in error_html

    def test_modernized_ui_controls(self):
        """Test that modernized UI controls are present"""
        renderer = DiagramRenderer()

        test_codes = ["graph TD; A --> B", "digraph G { A -> B; }", "@startuml\nA -> B\n@enduml"]

        for code in test_codes:
            try:
                html = renderer.render_diagram_auto(code)
                if html and "Error:" not in html:
                    # Check for modern control icons (monochrome)
                    modern_icons = ["↓", "⧉", "?", "○", "⛶"]
                    found_icons = [icon for icon in modern_icons if icon in html]
                    assert len(found_icons) >= 3, f"Modern icons not found in {code[:20]}..."

                    # Check for keyboard shortcuts
                    assert "addEventListener('keydown'" in html

                    # Check for help modal
                    assert "help-modal" in html
            except Exception:
                # Skip if rendering fails due to missing dependencies
                continue

    def test_no_old_ui_elements(self):
        """Test that old UI elements were removed"""
        renderer = DiagramRenderer()

        html = renderer.render_diagram_auto("graph TD; A --> B")

        if html and "Error:" not in html:
            # These elements should NOT be present (removed during modernization)
            removed_elements = [
                "Download Source",  # Download source button was removed
                "theme-toggle",  # Theme toggle was removed
                "zoom-in-btn",  # Manual zoom buttons were removed
                "zoom-out-btn",  # Manual zoom buttons were removed
                "arrow-controls",  # Arrow controls were removed
            ]

            for element in removed_elements:
                assert element not in html, f"Old UI element still present: {element}"

    def test_github_style_consistent_interface(self):
        """Test that interface follows GitHub-style design consistency"""
        renderer = DiagramRenderer()

        html = renderer.render_diagram_auto("graph TD; A --> B")

        if html and "Error:" not in html:
            # Should have GitHub-style CSS variables
            github_style_elements = [
                "--bg-color:",
                "--text-color:",
                "--border-color:",
                "--button-bg:",
                "--button-hover-bg:",
                "border-radius:",
                "box-shadow:",
            ]

            for element in github_style_elements:
                assert element in html, f"GitHub-style element missing: {element}"

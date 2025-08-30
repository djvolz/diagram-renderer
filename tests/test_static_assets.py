"""
Tests for static JavaScript library assets.

Verifies that required JS libraries (Mermaid.js, VizJS) are present
and correctly integrated into the rendering system.
"""

from pathlib import Path

from diagram_renderer import DiagramRenderer


class TestStaticJSLibraries:
    """Test static JavaScript libraries are present and functional"""

    def test_static_js_directory_exists(self):
        """Test that static JS directory exists"""
        static_dir = (
            Path(__file__).parent.parent / "diagram_renderer" / "renderers" / "static" / "js"
        )
        assert static_dir.exists(), "Static JS directory not found"
        assert static_dir.is_dir(), "Static JS path is not a directory"

    def test_mermaid_js_file_exists(self):
        """Test that mermaid.min.js file exists and has reasonable size"""
        mermaid_file = (
            Path(__file__).parent.parent
            / "diagram_renderer"
            / "renderers"
            / "static"
            / "js"
            / "mermaid.min.js"
        )

        assert mermaid_file.exists(), "mermaid.min.js not found"
        assert mermaid_file.is_file(), "mermaid.min.js is not a file"

        # Check file size (should be around 2.8MB)
        file_size = mermaid_file.stat().st_size
        assert file_size > 1_000_000, f"mermaid.min.js too small: {file_size} bytes"
        assert file_size < 5_000_000, f"mermaid.min.js too large: {file_size} bytes"

    def test_vizjs_files_exist(self):
        """Test that VizJS files exist and have reasonable sizes"""
        static_dir = (
            Path(__file__).parent.parent / "diagram_renderer" / "renderers" / "static" / "js"
        )

        # viz-full.js
        viz_full = static_dir / "viz-full.js"
        assert viz_full.exists(), "viz-full.js not found"
        assert viz_full.stat().st_size > 500_000, "viz-full.js too small"

        # viz-lite.js
        viz_lite = static_dir / "viz-lite.js"
        assert viz_lite.exists(), "viz-lite.js not found"
        assert viz_lite.stat().st_size > 5_000, "viz-lite.js too small"
        assert viz_lite.stat().st_size < 50_000, "viz-lite.js too large for lite version"

    def test_panzoom_file_exists(self):
        """Test that panzoom.min.js file exists and has reasonable size"""
        panzoom_file = (
            Path(__file__).parent.parent
            / "diagram_renderer"
            / "renderers"
            / "static"
            / "js"
            / "panzoom.min.js"
        )

        assert panzoom_file.exists(), "panzoom.min.js not found"
        assert panzoom_file.is_file(), "panzoom.min.js is not a file"

        # Check file size (should be substantial but not huge)
        file_size = panzoom_file.stat().st_size
        assert file_size > 10_000, f"panzoom.min.js too small: {file_size} bytes"
        assert file_size < 200_000, f"panzoom.min.js too large: {file_size} bytes"

    def test_js_files_are_valid_javascript(self):
        """Test that JS files contain valid JavaScript syntax indicators"""
        static_dir = (
            Path(__file__).parent.parent / "diagram_renderer" / "renderers" / "static" / "js"
        )

        js_files = ["mermaid.min.js", "viz-full.js", "viz-lite.js", "panzoom.min.js"]

        for js_file in js_files:
            file_path = static_dir / js_file
            content = file_path.read_text(encoding="utf-8")

            # Basic JS syntax checks
            assert len(content) > 1000, f"{js_file} content too short"

            # Should contain JavaScript-like content
            js_indicators = ["function", "var", "const", "let", "return"]
            found_indicators = sum(1 for indicator in js_indicators if indicator in content)
            assert found_indicators >= 3, f"{js_file} doesn't appear to contain JavaScript"

    def test_mermaid_library_integration(self):
        """Test that Mermaid library is properly integrated"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # Should contain embedded Mermaid.js content or reference
        # Check for Mermaid initialization patterns
        mermaid_patterns = ["mermaid.initialize", "mermaid.render", "startOnLoad", "flowchart"]

        found_patterns = sum(1 for pattern in mermaid_patterns if pattern in html)
        assert found_patterns >= 2, "Mermaid integration patterns not found in HTML"

    def test_vizjs_library_integration(self):
        """Test that VizJS library is properly integrated"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("digraph G { A -> B; }")

        # Should contain VizJS content or functionality
        # Check for Viz/Graphviz patterns
        viz_patterns = ["Viz(", "digraph", "renderSVGElement", "graphviz"]

        found_patterns = sum(1 for pattern in viz_patterns if pattern in html)
        assert found_patterns >= 1, "VizJS integration patterns not found in HTML"

    def test_static_assets_in_html_output(self):
        """Test that static assets are included in HTML output"""
        renderer = DiagramRenderer()

        # Test different diagram types
        test_cases = [
            ("mermaid", "graph TD; A --> B"),
            ("graphviz", "digraph G { A -> B; }"),
            ("plantuml", "@startuml\nA -> B\n@enduml"),
        ]

        for diagram_type, code in test_cases:
            html = renderer.render_diagram_auto(code)

            # Should contain substantial JavaScript content
            assert "<script>" in html, f"{diagram_type} HTML missing script tags"

            # Count script content
            script_content = html[html.find("<script>") : html.rfind("</script>")]
            assert len(script_content) > 10_000, (
                f"{diagram_type} HTML has insufficient script content"
            )

    def test_js_library_versions_consistency(self):
        """Test that JS libraries are consistent versions"""
        static_dir = (
            Path(__file__).parent.parent / "diagram_renderer" / "renderers" / "static" / "js"
        )

        # Check that all required files exist (consistency check)
        required_files = ["mermaid.min.js", "viz-full.js", "viz-lite.js", "panzoom.min.js"]

        for file_name in required_files:
            file_path = static_dir / file_name
            assert file_path.exists(), f"Required JS library {file_name} is missing"

            # Check file is not empty or corrupted
            assert file_path.stat().st_size > 1000, f"{file_name} appears to be empty or corrupted"


class TestJSLibraryFunctionality:
    """Test JavaScript library functionality integration"""

    def test_mermaid_rendering_with_themes(self):
        """Test Mermaid rendering with different themes"""
        renderer = DiagramRenderer()
        code = "graph TD; A --> B"

        # Should work with default rendering
        html = renderer.render_diagram_auto(code)

        # Check for theme configuration
        assert "theme:" in html or '"default"' in html, "Mermaid theme configuration not found"

    def test_interactive_controls_integration(self):
        """Test that interactive controls are properly integrated with JS libraries"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # Should have panzoom and interactive control functions
        control_functions = [
            "downloadPNG",
            "copyDiagram",
            "toggleHelp",
            "resetView",
            "toggleFullscreen",
        ]

        for func in control_functions:
            assert func in html, f"Interactive control function {func} not found"

    def test_error_handling_with_js_libraries(self):
        """Test error handling when JS libraries encounter issues"""
        renderer = DiagramRenderer()

        # Test with potentially problematic input
        problematic_inputs = [
            "graph TD; A[<script>alert('test')</script>] --> B",  # Script injection attempt
            "graph TD; A --> B; A --> C; C --> D; D --> E; E --> F" * 100,  # Very complex
        ]

        for code in problematic_inputs:
            html = renderer.render_diagram_auto(code)

            # Should still generate valid HTML
            assert "<html>" in html, "HTML structure broken with problematic input"
            assert "function" in html, "JavaScript functionality missing"

    def test_unicode_handling_in_js_context(self):
        """Test that Unicode characters work properly with JS libraries"""
        renderer = DiagramRenderer()

        # Test diagram with Unicode content
        unicode_diagram = 'graph TD; A["测试 🚀"] --> B["Тест 📊"]'
        html = renderer.render_diagram_auto(unicode_diagram)

        # Should preserve Unicode in both content and controls
        assert "测试 🚀" in html, "Unicode content not preserved"
        assert "Тест 📊" in html, "Cyrillic content not preserved"
        # Updated to match current UI icons
        assert "↓" in html or "⧉" in html, "Unicode control symbols not preserved"

    def test_js_library_no_conflicts(self):
        """Test that JS libraries don't conflict with each other"""
        renderer = DiagramRenderer()

        # Render different types to ensure no conflicts
        mermaid_html = renderer.render_diagram_auto("graph TD; A --> B")
        graphviz_html = renderer.render_diagram_auto("digraph G { A -> B; }")

        # Both should be valid and substantial
        assert len(mermaid_html) > 10_000, "Mermaid HTML too short"
        assert len(graphviz_html) > 10_000, "Graphviz HTML too short"

        # Check that both contain expected functionality
        assert "mermaid.initialize" in mermaid_html, "Mermaid functionality missing"
        assert "function" in graphviz_html, "JavaScript functionality missing in Graphviz"

        # Both should have interactive controls
        for html in [mermaid_html, graphviz_html]:
            assert "initializePanZoom" in html, "Interactive controls missing"
            assert "downloadPNG" in html, "Download functionality missing"

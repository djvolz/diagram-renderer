"""
Tests for UTF-8 charset encoding in HTML templates.

Ensures that all generated HTML includes proper charset declaration
to prevent Unicode symbol corruption in downloaded files.
"""

from diagram_renderer import DiagramRenderer


class TestCharsetEncoding:
    """Test charset encoding in HTML output"""

    def test_mermaid_html_has_charset(self):
        """Test that Mermaid HTML includes UTF-8 charset declaration"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # Check for charset declaration
        assert '<meta charset="utf-8">' in html

    def test_plantuml_html_has_charset(self):
        """Test that PlantUML HTML includes UTF-8 charset declaration"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("@startuml\nA -> B\n@enduml")

        # Check for charset declaration
        assert '<meta charset="utf-8">' in html

    def test_graphviz_html_has_charset(self):
        """Test that Graphviz HTML includes UTF-8 charset declaration"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("digraph G { A -> B; }")

        # Check for charset declaration
        assert '<meta charset="utf-8">' in html

    def test_unicode_symbols_preserved(self):
        """Test that Unicode symbols are preserved in HTML output"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # Check for GitHub-style Unicode control symbols (actual ones used in UI)
        unicode_symbols = ["⧉", "↓", "?", "○", "⛶"]

        for symbol in unicode_symbols:
            assert symbol in html, f"Unicode symbol '{symbol}' not found in HTML"

    def test_charset_declaration_position(self):
        """Test that charset declaration is in the correct position"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # Find positions
        head_pos = html.find("<head>")
        charset_pos = html.find('<meta charset="utf-8">')
        style_pos = html.find("<style>")

        # Charset should be after <head> but before <style>
        assert head_pos < charset_pos < style_pos, (
            "Charset declaration should be immediately after <head> and before <style>"
        )

    def test_charset_encoding_with_special_characters(self):
        """Test charset handling with diagrams containing special characters"""
        renderer = DiagramRenderer()

        # Test with special characters in diagram content
        mermaid_with_special = (
            'graph TD; A["Special: àáâãäåæçèé"] --> B["More: 中文 русский العربية"]'
        )
        html = renderer.render_diagram_auto(mermaid_with_special)

        # Should have charset and preserve special characters
        assert '<meta charset="utf-8">' in html
        assert "àáâãäåæçèé" in html
        assert "中文" in html
        assert "русский" in html
        assert "العربية" in html


class TestHTMLTemplateStructure:
    """Test HTML template structure and compliance"""

    def test_html_doctype_declaration(self):
        """Test that HTML includes proper DOCTYPE declaration"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        assert html.startswith("<!DOCTYPE html>")

    def test_html_lang_attribute_could_be_added(self):
        """Test that we could add lang attribute for accessibility (informational)"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # This is informational - we don't currently add lang but could
        # For better accessibility, we could add: <html lang="en">
        assert "<html>" in html

    def test_html_validation_structure(self):
        """Test basic HTML structure is valid"""
        renderer = DiagramRenderer()
        html = renderer.render_diagram_auto("graph TD; A --> B")

        # Check basic HTML structure (main document structure)
        assert html.startswith("<!DOCTYPE html>")
        assert "<html>" in html
        assert "<head>" in html
        assert "</head>" in html
        assert "<body>" in html
        assert "</body>" in html
        assert html.rstrip().endswith("</html>")

        # Check that we have the main document structure
        assert html.count("<head>") >= 1
        assert html.count("<body>") >= 1

    def test_charset_consistency_across_renderers(self):
        """Test that all renderer types produce consistent charset declarations"""
        renderer = DiagramRenderer()

        test_cases = [
            ("mermaid", "graph TD; A --> B"),
            ("plantuml", "@startuml\nA -> B\n@enduml"),
            ("graphviz", "digraph G { A -> B; }"),
        ]

        for diagram_type, code in test_cases:
            html = renderer.render_diagram_auto(code)

            # All should have the same charset declaration
            assert '<meta charset="utf-8">' in html, (
                f"{diagram_type} HTML missing charset declaration"
            )

            # Should be early in the head section
            head_content = html[html.find("<head>") : html.find("</head>")]
            assert '<meta charset="utf-8">' in head_content, (
                f"{diagram_type} charset not in head section"
            )

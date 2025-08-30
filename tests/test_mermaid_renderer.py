"""
Tests for MermaidRenderer functionality
"""

import pytest


class TestMermaidRenderer:
    """Test cases for MermaidRenderer"""

    def test_init(self, mermaid_renderer):
        """Test MermaidRenderer initialization"""
        assert mermaid_renderer.js_filename == "mermaid.min.js"
        assert hasattr(mermaid_renderer, "static_dir")
        assert mermaid_renderer.use_local_rendering is True

    def test_detect_diagram_type_strong_indicators(self, mermaid_renderer):
        """Test detection with strong Mermaid indicators"""
        test_cases = [
            "graph TD\n  A --> B",
            "flowchart LR\n  Start --> End",
            "sequenceDiagram\n  A->>B: Hello",
            "classDiagram\n  class User",
            "stateDiagram\n  [*] --> Active",
            "erDiagram\n  USER ||--o{ ORDER : places",
            "journey\n  title My Journey",
            "gantt\n  title Project Timeline",
            "pie title Pie Chart",
            "gitgraph:",
            "requirement test",
            "mindmap",
        ]

        for code in test_cases:
            assert mermaid_renderer.detect_diagram_type(code) is True

    def test_detect_diagram_type_participant_cases(self, mermaid_renderer):
        """Test detection with participant/actor indicators"""
        # Should detect as Mermaid
        mermaid_cases = [
            "sequenceDiagram\nparticipant A",
            "participant User as U\nparticipant Server",
            "actor User\nUser --> System",
        ]

        for code in mermaid_cases:
            assert mermaid_renderer.detect_diagram_type(code) is True

    def test_detect_diagram_type_non_mermaid(self, mermaid_renderer):
        """Test detection with non-Mermaid code"""
        non_mermaid_cases = [
            "@startuml\nAlice -> Bob\n@enduml",
            "participant Alice\nparticipant Bob\nAlice -> Bob",  # PlantUML style
            "class User {\n  +name: String\n}",  # Could be PlantUML
            "def function():\n    pass",  # Random code
            "",
        ]

        for code in non_mermaid_cases:
            assert mermaid_renderer.detect_diagram_type(code) is False

    def test_clean_code_basic(self, mermaid_renderer):
        """Test basic code cleaning"""
        code = "  graph TD\n    A --> B  "
        result = mermaid_renderer.clean_code(code)
        assert result == "graph TD\n    A --> B"

    def test_clean_code_markdown_mermaid(self, mermaid_renderer, sample_markdown_mermaid):
        """Test cleaning Mermaid code that has been stripped of markdown"""
        # Simulate code that has already been stripped of markdown fences by DiagramRenderer
        code_without_markdown = "graph LR\n    A --> B\n    B --> C"
        result = mermaid_renderer.clean_code(code_without_markdown)
        assert result == "graph LR\n    A --> B\n    B --> C"

    def test_clean_code_generic_markdown(self, mermaid_renderer):
        """Test cleaning code that has been stripped of markdown"""
        # Simulate code that has already been stripped of markdown fences by DiagramRenderer
        code_without_markdown = "graph TD\n  A --> B"
        result = mermaid_renderer.clean_code(code_without_markdown)
        assert result == "graph TD\n  A --> B"

    @pytest.mark.requires_js
    def test_render_html_with_js(
        self, mermaid_renderer, sample_mermaid_flowchart, static_js_exists
    ):
        """Test HTML rendering when Mermaid.js is available"""
        if not static_js_exists["mermaid"]:
            pytest.skip("Mermaid.js file not found")

        result = mermaid_renderer.render_html(sample_mermaid_flowchart)

        assert "<!DOCTYPE html>" in result
        assert "mermaid" in result
        assert "graph TD" in result
        assert "mermaid.initialize" in result

    def test_render_html_without_js(self, mermaid_renderer, sample_mermaid_flowchart, monkeypatch):
        """Test HTML rendering when Mermaid.js is not available"""
        # Mock get_static_js_content to return None
        monkeypatch.setattr(mermaid_renderer, "get_static_js_content", lambda x: None)

        result = mermaid_renderer.render_html(sample_mermaid_flowchart)

        assert "Error: Mermaid.js not available" in result


class TestMermaidRendererIntegration:
    """Integration tests for MermaidRenderer"""

    @pytest.mark.integration
    def test_end_to_end_flowchart(self, mermaid_renderer, sample_mermaid_flowchart):
        """Test complete flowchart rendering workflow"""
        # Test detection
        assert mermaid_renderer.detect_diagram_type(sample_mermaid_flowchart) is True

        # Test cleaning
        cleaned = mermaid_renderer.clean_code(sample_mermaid_flowchart)
        assert "graph TD" in cleaned

        # Test rendering (with mocked JS to avoid file dependency)
        import unittest.mock

        with unittest.mock.patch.object(
            mermaid_renderer, "get_static_js_content", return_value="// mock"
        ):
            html = mermaid_renderer.render_html(cleaned)
            assert "graph TD" in html
            assert "<!DOCTYPE html>" in html

    @pytest.mark.integration
    def test_end_to_end_sequence(self, mermaid_renderer, sample_mermaid_sequence):
        """Test complete sequence diagram rendering workflow"""
        # Test detection
        assert mermaid_renderer.detect_diagram_type(sample_mermaid_sequence) is True

        # Test cleaning
        cleaned = mermaid_renderer.clean_code(sample_mermaid_sequence)
        assert "sequenceDiagram" in cleaned

        # Test rendering
        import unittest.mock

        with unittest.mock.patch.object(
            mermaid_renderer, "get_static_js_content", return_value="// mock"
        ):
            html = mermaid_renderer.render_html(cleaned)
            assert "sequenceDiagram" in html

    @pytest.mark.integration
    @pytest.mark.requires_js
    def test_real_js_rendering(self, mermaid_renderer, sample_mermaid_flowchart, static_js_exists):
        """Test rendering with real Mermaid.js file"""
        if not static_js_exists["mermaid"]:
            pytest.skip("Mermaid.js file not found")

        html = mermaid_renderer.render_html(sample_mermaid_flowchart)

        # Should contain actual Mermaid.js code
        assert len(html) > 1000  # Real file should be substantial
        assert "mermaid" in html.lower()
        assert "graph TD" in html

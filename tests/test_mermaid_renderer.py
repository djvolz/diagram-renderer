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

        assert (
            "JavaScript Library Missing" in result
            or "Mermaid.js library is not available" in result
        )


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


class TestMermaidDebugCases:
    """Test cases derived from debug files"""

    @pytest.mark.integration
    def test_gantt_chart_rendering(self, mermaid_renderer):
        """Test gantt chart rendering from debug_gantt.py"""
        gantt_code = """gantt
    title Project Development Timeline
    dateFormat YYYY-MM-DD
    section Planning
    Requirements Analysis :done, req, 2024-01-01, 2024-01-07
    System Design :done, design, 2024-01-05, 2024-01-12

    section Development
    Backend Development :active, backend, 2024-01-10, 2024-02-15
    Frontend Development :frontend, 2024-01-20, 2024-02-20"""

        # Test detection
        assert mermaid_renderer.detect_diagram_type(gantt_code) is True

        # Test rendering produces HTML
        html_output = mermaid_renderer.render_html(gantt_code)
        assert html_output is not None
        assert "gantt" in html_output.lower()
        assert "mermaid" in html_output.lower()

    @pytest.mark.integration
    def test_block_diagram_external_handling(self, mermaid_renderer):
        """Test block diagram external handling from test_block.py"""
        block_code = """block-beta
    columns 1
    A
    B
    A --> B"""

        # Test detection
        assert mermaid_renderer.detect_diagram_type(block_code) is True

        # Test that it shows proper external diagram error
        html_output = mermaid_renderer.render_html(block_code)
        assert html_output is not None
        assert "Unsupported Diagram Type" in html_output
        assert "block-beta" in html_output
        assert "diagram-render-status" in html_output


class TestPlantUMLRendererCoverage:
    """Test cases for PlantUML renderer to match Mermaid coverage"""

    @pytest.mark.integration
    def test_plantuml_sequence_diagram_rendering(self):
        """Test PlantUML sequence diagram rendering"""
        from diagram_renderer.renderers.plantuml import PlantUMLRenderer

        renderer = PlantUMLRenderer()

        sequence_code = """@startuml
actor User
participant System
User -> System: Login
System --> User: Success
@enduml"""

        # Test detection
        assert renderer.detect_diagram_type(sequence_code) is True

        # Test rendering produces HTML
        html_output = renderer.render_html(sequence_code)
        assert html_output is not None
        assert "VizJS" in html_output
        assert "User" in html_output

    @pytest.mark.integration
    def test_plantuml_class_diagram_rendering(self):
        """Test PlantUML class diagram rendering"""
        from diagram_renderer.renderers.plantuml import PlantUMLRenderer

        renderer = PlantUMLRenderer()

        class_code = """@startuml
class User {
  +login()
}
class System {
  +authenticate()
}
User --> System
@enduml"""

        # Test detection
        assert renderer.detect_diagram_type(class_code) is True

        # Test rendering produces HTML
        html_output = renderer.render_html(class_code)
        assert html_output is not None
        assert "VizJS" in html_output
        assert "User" in html_output

    @pytest.mark.integration
    def test_plantuml_unsupported_diagram_error(self):
        """Test PlantUML unsupported diagram error handling"""
        from diagram_renderer.renderers.plantuml import PlantUMLRenderer

        renderer = PlantUMLRenderer()

        activity_code = """@startuml
start
:Step 1;
if (condition?) then (yes)
  :Step 2;
else (no)
  :Step 3;
endif
stop
@enduml"""

        # Test detection still works
        assert renderer.detect_diagram_type(activity_code) is True

        # Test that it shows proper unsupported diagram error
        html_output = renderer.render_html(activity_code)
        assert html_output is not None
        assert "Unsupported Diagram Type" in html_output
        assert "Activity diagrams" in html_output
        assert "diagram-render-status" in html_output

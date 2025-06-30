"""
Tests for PlantUMLRenderer functionality
"""
import pytest
from diagram_renderer.renderers.plantuml import PlantUMLRenderer


class TestPlantUMLRenderer:
    """Test cases for PlantUMLRenderer"""
    
    def test_detect_diagram_type_strong_indicators(self, plantuml_renderer):
        """Test detection with strong PlantUML indicators"""
        test_cases = [
            "@startuml\nAlice -> Bob\n@enduml",
            "@startmindmap\n* Root\n@endmindmap",
            "@startgantt\nProject starts 2023-01-01\n@endgantt",
            "@startclass\nclass User\n@endclass",
            "skinparam backgroundColor white",
            "!theme dark",
            "!include common.puml"
        ]
        
        for code in test_cases:
            assert plantuml_renderer.detect_diagram_type(code) is True
    
    def test_detect_diagram_type_participant_cases(self, plantuml_renderer):
        """Test detection with participant/actor indicators"""
        # Should detect as PlantUML (not Mermaid-style)
        plantuml_cases = [
            "participant Alice\nparticipant Bob\nAlice -> Bob",
            "actor User\nparticipant System\nUser -> System"
        ]
        
        for code in plantuml_cases:
            assert plantuml_renderer.detect_diagram_type(code) is True
        
        # Should NOT detect Mermaid-style sequences
        mermaid_cases = [
            "sequenceDiagram\nparticipant A",
            "participant User as U\nUser->>Server: Request"
        ]
        
        for code in mermaid_cases:
            assert plantuml_renderer.detect_diagram_type(code) is False
    
    def test_detect_diagram_type_weak_indicators(self, plantuml_renderer):
        """Test detection with weak PlantUML indicators"""
        test_cases = [
            "boundary UserInterface",
            "control UserController", 
            "entity UserData",
            "database UserDB",
            "collections UserList",
            "queue MessageQueue",
            "class User { +name: String }"
        ]
        
        for code in test_cases:
            assert plantuml_renderer.detect_diagram_type(code) is True
    
    def test_detect_diagram_type_non_plantuml(self, plantuml_renderer):
        """Test detection with non-PlantUML code"""
        non_plantuml_cases = [
            "graph TD\n  A --> B",
            "flowchart LR\n  Start --> End",
            "def function():\n    pass",
            ""
        ]
        
        for code in non_plantuml_cases:
            assert plantuml_renderer.detect_diagram_type(code) is False
    
    def test_clean_code_basic(self, plantuml_renderer):
        """Test basic code cleaning"""
        code = "  Alice -> Bob  "
        result = plantuml_renderer.clean_code(code)
        assert result == "@startuml\nAlice -> Bob\n@enduml"
    
    def test_clean_code_with_tags(self, plantuml_renderer, sample_plantuml_sequence):
        """Test cleaning code that already has @startuml/@enduml tags"""
        result = plantuml_renderer.clean_code(sample_plantuml_sequence)
        assert result.startswith("@startuml")
        assert result.endswith("@enduml")
        # Should not duplicate tags
        assert result.count("@startuml") == 1
        assert result.count("@enduml") == 1
    
    def test_clean_code_markdown_plantuml(self, plantuml_renderer):
        """Test cleaning PlantUML code that has been stripped of markdown"""
        # Simulate code that has already been stripped of markdown fences by DiagramRenderer
        code_without_markdown = "@startuml\nAlice -> Bob: Hello\n@enduml"
        result = plantuml_renderer.clean_code(code_without_markdown)
        assert "```" not in result # Ensure clean_code doesn't introduce them
        assert "@startuml" in result
        assert "@enduml" in result
        assert "Alice -> Bob: Hello" in result
    
    def test_convert_plantuml_to_dot_sequence(self, plantuml_renderer, sample_plantuml_sequence):
        """Test PlantUML to DOT conversion for sequence diagrams"""
        result = plantuml_renderer.convert_plantuml_to_dot(sample_plantuml_sequence)
        
        assert "digraph sequence" in result
        assert "rankdir=LR" in result
        assert "User" in result
        assert "Browser" in result
        assert "Server" in result
        assert "Database" in result
        assert "->" in result
    
    def test_convert_plantuml_to_dot_class(self, plantuml_renderer, sample_plantuml_class):
        """Test PlantUML to DOT conversion for class diagrams"""
        result = plantuml_renderer.convert_plantuml_to_dot(sample_plantuml_class)
        
        assert "digraph classes" in result
        assert "User" in result
        assert "Admin" in result
        assert "shape=record" in result
    
    def test_convert_plantuml_to_dot_default(self, plantuml_renderer):
        """Test PlantUML to DOT conversion for unknown diagram types"""
        code = "@startuml\nsome unknown syntax\n@enduml"
        result = plantuml_renderer.convert_plantuml_to_dot(code)
        
        assert "digraph G" in result
        assert "PlantUML" in result
        assert "Local Rendering" in result
    
    def test_convert_sequence_to_dot(self, plantuml_renderer):
        """Test sequence diagram to DOT conversion logic"""
        lines = [
            "@startuml",
            "participant User",
            "participant System", 
            "User -> System: Login",
            "System -> User: Welcome",
            "@enduml"
        ]
        
        result = plantuml_renderer._convert_sequence_to_dot(lines)
        
        assert "digraph sequence" in result
        assert "\"User\"" in result
        assert "\"System\"" in result
        assert 'label="Login"' in result
        assert 'label="Welcome"' in result
    
    def test_convert_class_to_dot(self, plantuml_renderer):
        """Test class diagram to DOT conversion logic"""
        lines = [
            "@startuml",
            "class User {",
            "  +name: String",
            "}",
            "class Admin {",
            "  +permissions: List",
            "}",
            "User <|-- Admin",
            "@enduml"
        ]
        
        result = plantuml_renderer._convert_class_to_dot(lines)
        
        assert "digraph classes" in result
        assert "\"User\"" in result
        assert "\"Admin\"" in result
        assert "arrowhead=empty" in result
    
    def test_render_html_disabled_local_rendering(self, plantuml_renderer, sample_plantuml_sequence):
        """Test HTML rendering with local rendering disabled"""
        plantuml_renderer.use_local_rendering = False
        
        with pytest.raises(Exception, match="Local rendering disabled"):
            plantuml_renderer.render_html(sample_plantuml_sequence)


class TestPlantUMLRendererIntegration:
    """Integration tests for PlantUMLRenderer"""
    
    @pytest.mark.integration
    def test_end_to_end_sequence(self, plantuml_renderer, sample_plantuml_sequence):
        """Test complete sequence diagram rendering workflow"""
        # Test detection
        assert plantuml_renderer.detect_diagram_type(sample_plantuml_sequence) is True
        
        # Test cleaning
        cleaned = plantuml_renderer.clean_code(sample_plantuml_sequence)
        assert "@startuml" in cleaned
        assert "@enduml" in cleaned
        
        # Test DOT conversion
        dot_code = plantuml_renderer.convert_plantuml_to_dot(cleaned)
        assert "digraph sequence" in dot_code
        assert "User" in dot_code
        
        # Test rendering (with mocked VizJS)
        import unittest.mock
        with unittest.mock.patch.object(plantuml_renderer, 'get_static_js_content', return_value="// mock"):
            html = plantuml_renderer.render_html(cleaned)
            assert "<!DOCTYPE html>" in html
    
    @pytest.mark.integration
    def test_end_to_end_class(self, plantuml_renderer, sample_plantuml_class):
        """Test complete class diagram rendering workflow"""
        # Test detection
        assert plantuml_renderer.detect_diagram_type(sample_plantuml_class) is True
        
        # Test cleaning
        cleaned = plantuml_renderer.clean_code(sample_plantuml_class)
        assert "class User" in cleaned
        
        # Test DOT conversion
        dot_code = plantuml_renderer.convert_plantuml_to_dot(cleaned)
        assert "digraph classes" in dot_code
        assert "User" in dot_code
        assert "Admin" in dot_code
    
    @pytest.mark.integration
    @pytest.mark.requires_js
    def test_real_viz_rendering(self, plantuml_renderer, sample_plantuml_sequence, static_js_exists):
        """Test rendering with real VizJS files"""
        if not static_js_exists['plantuml']:
            pytest.skip("VizJS files not found")
        
        html = plantuml_renderer.render_html(sample_plantuml_sequence)
        
        # Should contain actual VizJS code
        assert len(html) > 1000  # Real files should be substantial
        assert "Viz" in html
    
    @pytest.mark.integration
    def test_markdown_to_html_workflow(self, plantuml_renderer, sample_markdown_plantuml):
        """Test complete workflow from markdown to HTML"""
        # Should detect as PlantUML
        assert plantuml_renderer.detect_diagram_type(sample_markdown_plantuml) is True
        
        # Clean and render
        import unittest.mock
        with unittest.mock.patch.object(plantuml_renderer, 'get_static_js_content', return_value="// mock"):
            html = plantuml_renderer.render_html(sample_markdown_plantuml)
            assert "Alice" in html
            assert "Bob" in html
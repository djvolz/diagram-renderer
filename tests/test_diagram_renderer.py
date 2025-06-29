import pytest
from diagram import DiagramRenderer


class TestDiagramRenderer:
    """Test cases for main DiagramRenderer class"""
    
    def test_init(self, diagram_renderer):
        """Test DiagramRenderer initialization"""
        assert isinstance(diagram_renderer.renderers, list)
        assert len(diagram_renderer.renderers) == 3
        
        # Verify renderer types and order
        from diagram.renderers.graphviz import GraphvizRenderer
        from diagram.renderers.plantuml import PlantUMLRenderer
        from diagram.renderers.mermaid import MermaidRenderer
        
        assert diagram_renderer.renderers[0][0] == "graphviz"
        assert isinstance(diagram_renderer.renderers[0][1], GraphvizRenderer)
        
        assert diagram_renderer.renderers[1][0] == "plantuml"
        assert isinstance(diagram_renderer.renderers[1][1], PlantUMLRenderer)
        
        assert diagram_renderer.renderers[2][0] == "mermaid"
        assert isinstance(diagram_renderer.renderers[2][1], MermaidRenderer)

    def test_detect_diagram_type_mermaid(self, diagram_renderer, sample_mermaid_flowchart):
        """Test diagram type detection for Mermaid"""
        result = diagram_renderer.detect_diagram_type(sample_mermaid_flowchart)
        assert result == "mermaid"
    
    def test_detect_diagram_type_plantuml(self, diagram_renderer, sample_plantuml_sequence):
        """Test diagram type detection for PlantUML"""
        result = diagram_renderer.detect_diagram_type(sample_plantuml_sequence)
        assert result == "plantuml"
    
    def test_detect_diagram_type_graphviz(self, diagram_renderer, sample_graphviz_simple):
        """Test Graphviz diagram type detection"""
        result = diagram_renderer.detect_diagram_type(sample_graphviz_simple)
        assert result == "graphviz"
    
    def test_detect_diagram_type_precedence(self, diagram_renderer):
        """Test diagram type detection precedence"""
        # Graphviz code should be detected as graphviz
        graphviz_code = "digraph G {\n    A -> B\n    B -> C\n}"
        result = diagram_renderer.detect_diagram_type(graphviz_code)
        assert result == "graphviz"
        
        # PlantUML should still take precedence when it has strong indicators
        plantuml_code = "@startuml\nparticipant User\nUser -> System\n@enduml"
        result = diagram_renderer.detect_diagram_type(plantuml_code)
        assert result == "plantuml"
    
    def test_detect_diagram_type_default_mermaid(self, diagram_renderer):
        """Test that unclear code returns None"""
        unclear_code = "some random text"
        result = diagram_renderer.detect_diagram_type(unclear_code)
        assert result is None
    
    def test_render_diagram_auto_mermaid(self, diagram_renderer, sample_mermaid_flowchart, monkeypatch):
        """Test automatic rendering for Mermaid diagrams"""
        # Mock the Mermaid renderer to avoid JS file dependency
        mock_html_content = "<svg>Mermaid Mock SVG</svg>"
        mermaid_renderer_instance = diagram_renderer.renderers[2][1]
        monkeypatch.setattr(mermaid_renderer_instance, 'render_html', lambda code, **kwargs: f"<html><body>{mock_html_content}</body></html>")
        
        result = diagram_renderer.render_diagram_auto(sample_mermaid_flowchart)
        assert mock_html_content in result
    
    def test_render_diagram_auto_plantuml(self, diagram_renderer, sample_plantuml_sequence, monkeypatch):
        """Test automatic rendering for PlantUML diagrams"""
        # Mock the PlantUML renderer to avoid VizJS dependency
        mock_html_content = "<svg>PlantUML Mock SVG</svg>"
        plantuml_renderer_instance = diagram_renderer.renderers[1][1]
        monkeypatch.setattr(plantuml_renderer_instance, 'render_html', lambda code, **kwargs: f"<html><body>{mock_html_content}</body></html>")
        
        result = diagram_renderer.render_diagram_auto(sample_plantuml_sequence)
        assert mock_html_content in result
    
    def test_render_diagram_auto_graphviz(self, diagram_renderer, sample_graphviz_simple, monkeypatch):
        """Test automatic rendering for Graphviz diagrams"""
        # Mock the Graphviz renderer to avoid VizJS dependency
        mock_html_content = "<svg>Graphviz Mock SVG</svg>"
        graphviz_renderer_instance = diagram_renderer.renderers[0][1]
        monkeypatch.setattr(graphviz_renderer_instance, 'render_html', lambda code, **kwargs: f"<html><body>{mock_html_content}</body></html>")
        
        result = diagram_renderer.render_diagram_auto(sample_graphviz_simple)
        assert mock_html_content in result

class TestDiagramRendererIntegration:
    """Integration tests for DiagramRenderer"""
    
    @pytest.mark.integration
    def test_end_to_end_mermaid_workflow(self, diagram_renderer, sample_mermaid_flowchart):
        """Test complete Mermaid workflow from detection to rendering"""
        # Mock to avoid JS file dependency
        import unittest.mock
        mermaid_renderer_instance = diagram_renderer.renderers[2][1]
        with unittest.mock.patch.object(mermaid_renderer_instance, 'get_static_js_content', return_value="// mock"):
            # Detect type
            diagram_type = diagram_renderer.detect_diagram_type(sample_mermaid_flowchart)
            assert diagram_type == "mermaid"
            
            # Render
            html = diagram_renderer.render_diagram_auto(sample_mermaid_flowchart)
            assert "graph TD" in html
            assert "<!DOCTYPE html>" in html
    
    @pytest.mark.integration
    def test_end_to_end_plantuml_workflow(self, diagram_renderer, sample_plantuml_sequence):
        """Test complete PlantUML workflow from detection to rendering"""
        # Mock to avoid VizJS dependency
        import unittest.mock
        plantuml_renderer_instance = diagram_renderer.renderers[1][1]
        with unittest.mock.patch.object(plantuml_renderer_instance, 'get_static_js_content', return_value="// mock"):
            # Detect type
            diagram_type = diagram_renderer.detect_diagram_type(sample_plantuml_sequence)
            assert diagram_type == "plantuml"
            
            # Render
            html = diagram_renderer.render_diagram_auto(sample_plantuml_sequence)
            assert "<!DOCTYPE html>" in html
    
    @pytest.mark.integration
    def test_markdown_input_workflows(self, diagram_renderer, sample_markdown_mermaid, sample_markdown_plantuml):
        """Test workflows with markdown-wrapped diagram code"""
        import unittest.mock
        
        # Mock both renderers
        mermaid_renderer_instance = diagram_renderer.renderers[2][1]
        plantuml_renderer_instance = diagram_renderer.renderers[1][1]
        with unittest.mock.patch.object(mermaid_renderer_instance, 'get_static_js_content', return_value="// mock"):
            with unittest.mock.patch.object(plantuml_renderer_instance, 'get_static_js_content', return_value="// mock"):
                # Test Mermaid markdown
                mermaid_type = diagram_renderer.detect_diagram_type(sample_markdown_mermaid)
                assert mermaid_type == "mermaid"
                
                mermaid_html = diagram_renderer.render_diagram_auto(sample_markdown_mermaid)
                assert "graph LR" in mermaid_html
                
                # Test PlantUML markdown
                plantuml_type = diagram_renderer.detect_diagram_type(sample_markdown_plantuml)
                assert plantuml_type == "plantuml"
                
                plantuml_html = diagram_renderer.render_diagram_auto(sample_markdown_plantuml)
                assert "Alice" in plantuml_html
    
    @pytest.mark.integration
    @pytest.mark.requires_js
    def test_real_files_integration(self, diagram_renderer, sample_mermaid_flowchart, sample_plantuml_sequence, static_js_exists):
        """Test integration with real static JS files"""
        if not static_js_exists['all']:
            pytest.skip("Static JS files not available")
        
        # Test Mermaid with real files
        mermaid_html = diagram_renderer.render_diagram_auto(sample_mermaid_flowchart)
        assert len(mermaid_html) > 1000  # Should be substantial with real JS
        assert "graph TD" in mermaid_html
        
        # Test PlantUML with real files
        plantuml_html = diagram_renderer.render_diagram_auto(sample_plantuml_sequence)
        assert len(plantuml_html) > 1000  # Should be substantial with real VizJS
        assert "User" in plantuml_html


class TestDiagramRendererErrorHandling:
    """Test error handling in DiagramRenderer"""
    
    def test_renderer_exception_propagation(self, diagram_renderer, sample_mermaid_flowchart, monkeypatch):
        """Test that renderer exceptions are properly propagated"""
        # Mock renderer to raise an exception
        def mock_render_error(code, **kwargs):
            raise Exception("Mock renderer error")
        
        mermaid_renderer_instance = diagram_renderer.renderers[2][1]
        monkeypatch.setattr(mermaid_renderer_instance, 'render_html', mock_render_error)
        
        with pytest.raises(Exception, match="Mock renderer error"):
            diagram_renderer.render_diagram_auto(sample_mermaid_flowchart)
    
    def test_empty_code_handling(self, diagram_renderer):
        """Test handling of empty or whitespace-only code"""
        empty_cases = ["", "   ", "\n\n\n", "\t\t"]
        
        for empty_code in empty_cases:
            # Should not crash, should default to mermaid
            diagram_type = diagram_renderer.detect_diagram_type(empty_code)
            assert diagram_type is None
    
    def test_very_long_code_handling(self, diagram_renderer, monkeypatch):
        """Test handling of very long diagram code"""
        # Create a very long diagram
        long_code = "graph TD\n" + "\n".join([f"  A{i} --> A{i+1}" for i in range(1000)])
        
        # Mock to avoid actual rendering
        mermaid_renderer_instance = diagram_renderer.renderers[2][1]
        monkeypatch.setattr(mermaid_renderer_instance, 'render_html', lambda code, **kwargs: "<html>Long diagram</html>")
        
        # Should detect as mermaid
        diagram_type = diagram_renderer.detect_diagram_type(long_code)
        assert diagram_type == "mermaid"
        
        # Should render without issues
        result = diagram_renderer.render_diagram_auto(long_code)
        assert "Long diagram" in result

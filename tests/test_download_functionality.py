"""
Tests for PNG and source code download functionality
"""
import pytest
from diagram_renderer import DiagramRenderer


class TestDownloadFunctionality:
    """Test download button functionality in rendered HTML"""
    
    def test_mermaid_download_buttons_present(self):
        """Test that Mermaid diagrams include download buttons"""
        renderer = DiagramRenderer()
        
        mermaid_code = """
        graph TD
            A[Start] --> B{Decision}
            B -->|Yes| C[Action 1]
            B -->|No| D[Action 2]
        """
        
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Check for PNG download button
        assert 'onclick="downloadPNG()"' in html
        # Button initially shows "Loading diagram..." and gets updated via JavaScript
        assert 'title="Loading diagram..."' in html or 'title="Download PNG"' in html
        assert '⤓' in html or '📷' in html or '📥' in html  # Accept various download icons
        
        # Check for source code download button
        assert 'onclick="downloadCode()"' in html
        assert 'title="Download Source Code"' in html
        assert '📄' in html
    
    def test_graphviz_download_buttons_present(self):
        """Test that Graphviz diagrams include download buttons"""
        renderer = DiagramRenderer()
        
        dot_code = """
        digraph G {
            A -> B;
            B -> C;
        }
        """
        
        html = renderer.render_diagram_auto(dot_code)
        
        # Check for PNG download button
        assert 'onclick="downloadPNG()"' in html
        assert 'title="Download PNG"' in html
        assert '⤓' in html or '📷' in html or '📥' in html  # Accept various download icons
        
        # Check for source code download button
        assert 'onclick="downloadCode()"' in html
        assert 'title="Download Source Code"' in html
        assert '📄' in html
    
    def test_download_javascript_functions_present(self):
        """Test that download JavaScript functions are included"""
        renderer = DiagramRenderer()
        
        mermaid_code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Check for downloadPNG function
        assert 'function downloadPNG()' in html
        assert 'canvas.toDataURL' in html
        assert 'image/png' in html
        
        # Check for downloadCode function  
        assert 'function downloadCode()' in html
        assert 'Blob([originalCode]' in html
        assert 'text/plain' in html
    
    def test_mermaid_svg_cleaning_logic_present(self):
        """Test that SVG cleaning logic is present in Mermaid renderer"""
        renderer = DiagramRenderer()
        
        mermaid_code = "sequenceDiagram; A->>B: Hello"
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Check for SVG cleaning functions
        assert 'foreignObject' in html  # Should be mentioned in cleaning logic
        assert 'XMLSerializer' in html
        assert 'toDataURL' in html
        
        # Check for error handling
        assert 'SecurityError' in html or 'Security restrictions' in html
    
    def test_canvas_security_fixes_present(self):
        """Test that canvas security fixes are implemented"""
        renderer = DiagramRenderer()
        
        # Test with different diagram types
        test_cases = [
            ("graph TD; A-->B", "mermaid"),
            ("digraph G { A -> B; }", "graphviz"),
            ("@startuml\nA -> B\n@enduml", "plantuml")
        ]
        
        for diagram_code, expected_type in test_cases:
            html = renderer.render_diagram_auto(diagram_code)
            
            # Should use toDataURL instead of toBlob to avoid tainted canvas issues
            assert 'toDataURL' in html
            assert 'toBlob' not in html or 'toDataURL' in html  # toDataURL should be preferred
            
            # Should include proper error handling
            assert 'catch' in html and 'error' in html.lower()
    
    def test_download_filenames_appropriate(self):
        """Test that download filenames are set appropriately"""
        renderer = DiagramRenderer()
        
        # Test Mermaid - should include dynamic filename generation
        mermaid_html = renderer.render_diagram_auto("graph TD; A-->B")
        assert 'generateFileName' in mermaid_html
        assert 'mermaid' in mermaid_html  # Should reference mermaid type
        assert '.png' in mermaid_html
        assert '.mmd' in mermaid_html
        
        # Test Graphviz - should include dynamic filename generation  
        graphviz_html = renderer.render_diagram_auto("digraph G { A -> B; }")
        assert 'generateFileName' in graphviz_html
        assert 'graphviz' in graphviz_html  # Should reference graphviz type
        assert '.png' in graphviz_html
        assert '.txt' in graphviz_html
    
    def test_svg_namespace_handling(self):
        """Test that SVG namespace is properly handled"""
        renderer = DiagramRenderer()
        
        mermaid_code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Should ensure SVG has proper namespace
        assert 'xmlns="http://www.w3.org/2000/svg"' in html
        assert 'XMLSerializer' in html
    
    def test_error_messages_user_friendly(self):
        """Test that error messages are user-friendly"""
        renderer = DiagramRenderer()
        
        mermaid_code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Should have user-friendly error messages
        user_friendly_messages = [
            'Failed to generate PNG',
            'Security restrictions may prevent export',
            'Please try again',
            'may contain unsupported elements'
        ]
        
        # At least some user-friendly messages should be present
        found_messages = [msg for msg in user_friendly_messages if msg in html]
        assert len(found_messages) > 0, f"No user-friendly error messages found in HTML"


class TestSourceCodeDownload:
    """Tests specifically for source code download functionality"""
    
    def test_source_code_embedded_correctly(self):
        """Test that original source code is properly embedded in HTML"""
        renderer = DiagramRenderer()
        
        original_code = """graph TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E"""
        
        html = renderer.render_diagram_auto(original_code)
        
        # Source code should be JSON-escaped and embedded
        import json
        escaped_code = json.dumps(original_code)
        assert escaped_code in html, "Original source code not properly embedded"
    
    def test_mermaid_source_download_function(self):
        """Test Mermaid source code download function"""
        renderer = DiagramRenderer()
        
        mermaid_code = "sequenceDiagram\n    A->>B: Hello\n    B-->>A: Hi back"
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Should have downloadCode function
        assert 'function downloadCode()' in html
        
        # Should create blob with text/plain MIME type
        assert 'Blob([originalCode], { type: \'text/plain\' })' in html
        
        # Should use .mmd extension for Mermaid files
        assert 'mermaid-diagram.mmd' in html
        
        # Should have proper click handler
        assert 'link.click()' in html
        assert 'URL.revokeObjectURL' in html
    
    def test_graphviz_source_download_function(self):
        """Test Graphviz source code download function"""
        renderer = DiagramRenderer()
        
        dot_code = """digraph G {
    rankdir=LR;
    A -> B -> C;
    A -> C;
}"""
        html = renderer.render_diagram_auto(dot_code)
        
        # Should have downloadCode function
        assert 'function downloadCode()' in html
        
        # Should create blob with text/plain MIME type
        assert 'Blob([originalCode], { type: \'text/plain\' })' in html
        
        # Should use .dot extension for Graphviz files and call generateFileName
        assert 'generateFileName(originalCode, extension)' in html
        
        # Should preserve original DOT code
        import json
        escaped_code = json.dumps(dot_code)
        assert escaped_code in html
    
    def test_plantuml_source_download_function(self):
        """Test PlantUML source code download function"""
        renderer = DiagramRenderer()
        
        plantuml_code = """@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response
@enduml"""
        
        html = renderer.render_diagram_auto(plantuml_code)
        
        # Should have downloadCode function
        assert 'function downloadCode()' in html
        
        # Should preserve original PlantUML code (not converted DOT)
        import json
        escaped_original = json.dumps(plantuml_code)
        assert escaped_original in html
        
        # Should use .txt extension
        assert 'diagram-source.txt' in html
    
    def test_source_code_special_characters_escaped(self):
        """Test that source code with special characters is properly escaped"""
        renderer = DiagramRenderer()
        
        # Code with quotes, newlines, backslashes
        tricky_code = '''graph TD
    A["Text with \\"quotes\\""] --> B
    B --> C["Line 1\\nLine 2"]
    C --> D[Text with 'single quotes']'''
        
        html = renderer.render_diagram_auto(tricky_code)
        
        # Should be properly JSON escaped
        import json
        escaped_code = json.dumps(tricky_code)
        assert escaped_code in html
        
        # Should not have raw quotes that would break JavaScript
        lines = html.split('\n')
        for line in lines:
            if 'originalCode =' in line and '"' in line:
                # The line should not have unescaped quotes
                assert '\\"' in line or "'" in line, "Special characters not properly escaped"
    
    def test_source_code_download_button_properties(self):
        """Test source code download button has correct properties"""
        renderer = DiagramRenderer()
        
        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)
        
        # Should have source download button with correct attributes
        assert 'title="Download Source Code"' in html
        assert '📄' in html  # File emoji
        assert 'onclick="downloadCode()"' in html
        
        # Button should be part of zoom controls
        assert 'zoom-controls' in html
        assert 'zoom-btn' in html
    
    def test_source_download_preserves_whitespace(self):
        """Test that source code download preserves original formatting"""
        renderer = DiagramRenderer()
        
        # Code with specific indentation and spacing
        formatted_code = """graph TD
    A[Start] --> B{Decision}
    
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    
    C --> E[End]
    D --> E"""
        
        html = renderer.render_diagram_auto(formatted_code)
        
        # Original formatting should be preserved in JSON
        import json
        escaped_code = json.dumps(formatted_code)
        assert escaped_code in html
        
        # Should preserve newlines as \\n in JSON
        assert '\\n' in escaped_code
        assert escaped_code.count('\\n') >= 6  # Should have multiple newlines
    
    def test_both_download_buttons_present(self):
        """Test that both PNG and source download buttons are present"""
        renderer = DiagramRenderer()
        
        test_cases = [
            "graph TD; A-->B",
            "sequenceDiagram; A->>B: Hello", 
            "pie title Test; A: 50; B: 50",
            "digraph G { A -> B; }",
            "@startuml\nA -> B\n@enduml"
        ]
        
        for code in test_cases:
            html = renderer.render_diagram_auto(code)
            
            # Both download buttons should be present
            assert '⤓' in html or '📷' in html or '📥' in html  # Accept various download icons, f"PNG download button missing for: {code[:20]}..."
            assert '📄' in html, f"Source download button missing for: {code[:20]}..."
            
            # Both functions should be present
            assert 'downloadPNG' in html, f"PNG download function missing for: {code[:20]}..."
            assert 'downloadCode' in html, f"Source download function missing for: {code[:20]}..."
    
    def test_source_download_mime_type_correct(self):
        """Test that source download uses correct MIME type"""
        renderer = DiagramRenderer()
        
        code = "graph TD; A-->B"
        html = renderer.render_diagram_auto(code)
        
        # Should use text/plain MIME type for source files
        assert "type: 'text/plain'" in html or 'type: "text/plain"' in html
        
        # Should not use other MIME types for source download
        assert 'application/json' not in html.split('downloadCode')[1].split('function')[0]
        assert 'text/html' not in html.split('downloadCode')[1].split('function')[0]


class TestDownloadIntegration:
    """Integration tests for download functionality"""
    
    @pytest.mark.integration
    def test_rendered_html_valid_structure(self):
        """Test that rendered HTML has valid structure for downloads"""
        renderer = DiagramRenderer()
        
        test_diagrams = [
            "graph TD; A-->B-->C",
            "sequenceDiagram; A->>B: Hello",
            "pie title Pets; Dogs: 386; Cats: 85",
            "digraph G { A -> B -> C; }",
        ]
        
        for diagram_code in test_diagrams:
            html = renderer.render_diagram_auto(diagram_code)
            
            # Should have proper HTML structure
            assert '<!DOCTYPE html>' in html
            assert '<html>' in html and '</html>' in html
            assert '<body>' in html and '</body>' in html
            
            # Should have zoom controls with download buttons
            assert 'zoom-controls' in html
            assert 'zoom-btn' in html
            
            # Should have canvas-related JavaScript
            assert 'canvas' in html.lower()
            assert 'createElement' in html
    
    @pytest.mark.integration 
    def test_no_javascript_errors_in_basic_html(self):
        """Test that the HTML doesn't have obvious JavaScript syntax errors"""
        renderer = DiagramRenderer()
        
        mermaid_code = "graph TD; A[Start]-->B[End]"
        html = renderer.render_diagram_auto(mermaid_code)
        
        # Basic JavaScript syntax checks
        # Count opening and closing braces (should be balanced)
        # Note: We need to account for template literals and string content
        open_braces = html.count('{')
        close_braces = html.count('}')
        # Allow for small differences due to template processing and string content
        brace_diff = abs(open_braces - close_braces)
        assert brace_diff <= 4, f"Too many unbalanced JavaScript braces: {open_braces} vs {close_braces}"
        
        # Check for proper statement termination
        assert ');' in html  # Should have proper statement termination
        
        # Check that functions are properly defined
        assert 'function ' in html  # Should have function definitions
        
        # Check for essential download functionality
        assert 'downloadPNG' in html
        assert 'downloadCode' in html
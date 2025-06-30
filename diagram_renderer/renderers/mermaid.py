from .base import BaseRenderer


class MermaidRenderer(BaseRenderer):
    """Renderer for Mermaid diagrams"""
    
    def __init__(self):
        super().__init__()
        self.js_filename = "mermaid.min.js"
    
    def detect_diagram_type(self, code):
        """Detect if code is Mermaid"""
        code = code.strip().lower()
        
        # Strong Mermaid indicators (definitive)
        strong_mermaid_indicators = [
            "graph ", "flowchart ", "sequencediagram", "classdiagram",
            "statediagram", "erdiagram", "journey", "gantt", "pie ",
            "gitgraph", "requirement", "mindmap"
        ]
        
        # Check for strong indicators
        for indicator in strong_mermaid_indicators:
            if indicator in code:
                return True
        
        # Weak indicators - check context for participant/actor usage
        if "participant " in code or "actor " in code:
            # Check if it looks like Mermaid sequence diagram
            if ("sequencediagram" in code or 
                "-->" in code or "->>" in code or 
                ("participant " in code and ("as " in code or ":" in code))):
                return True
        
        return False
    
    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        return code.strip()
    
    def render_html(self, code, **kwargs):
        """Generate HTML with embedded Mermaid.js"""
        mermaid_js_content = self.get_static_js_content(self.js_filename)
        
        if not mermaid_js_content:
            return "<div>Error: Mermaid.js not available</div>"
        
        # Clean mermaid code
        clean_code = self.clean_code(code)
        
        # Escape original code for JavaScript
        import json
        escaped_original = json.dumps(code)
        
        # Get template and substitute variables
        template = self.get_template_content("mermaid.html")
        if not template:
            return "<div>Error: Mermaid template not available</div>"
        
        # Use replace instead of format to avoid issues with CSS curly braces
        html = template.replace('{mermaid_js_content}', mermaid_js_content)
        html = html.replace('{clean_code}', clean_code)
        html = html.replace('{escaped_original}', escaped_original)
        return html
    
    
    def render_svg_html(self, code, theme="default"):
        """Generate minimal HTML that renders Mermaid to SVG for extraction"""
        mermaid_js_content = self.get_static_js_content(self.js_filename)
        
        if not mermaid_js_content:
            return "<div>Error: Mermaid.js not available</div>"
        
        # Clean mermaid code
        clean_code = self.clean_code(code)
        
        # Get template and substitute variables
        template = self.get_template_content("mermaid-svg.html")
        if not template:
            return "<div>Error: Mermaid SVG template not available</div>"
        
        # Use replace instead of format to avoid issues with CSS curly braces
        html = template.replace('{mermaid_js_content}', mermaid_js_content)
        html = html.replace('{theme}', theme)
        html = html.replace('{clean_code}', clean_code)
        return html
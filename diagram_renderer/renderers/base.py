from pathlib import Path
from abc import ABC, abstractmethod
import json
import re


class BaseRenderer(ABC):
    """Base class for diagram renderers"""
    
    def __init__(self):
        # Get static directory relative to this module
        module_dir = Path(__file__).parent  # diagram/renderers
        self.static_dir = module_dir / "static"
        self.use_local_rendering = True
    
    @abstractmethod
    def render_html(self, code, **kwargs):
        """Render diagram as HTML"""
        pass
    
    @abstractmethod
    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        pass
    
    def detect_diagram_type(self, code):
        """Detect if code matches this renderer type"""
        # To be implemented by subclasses
        return False
    
    def get_static_js_content(self, filename):
        """Get JavaScript content from static file"""
        js_file = self.static_dir / "js" / filename
        if js_file.exists():
            with open(js_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    

    def get_template_content(self, filename):
        """Get HTML template content from templates directory"""
        template_file = self.static_dir.parent / "templates" / filename
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def _render_vizjs_html(self, dot_code, original_code=None):
        """Generate HTML with VizJS to render DOT notation as SVG"""
        # Use JSON.stringify equivalent escaping to safely embed DOT code
        escaped_dot = json.dumps(dot_code)
        
        # If no original code provided, use the dot code
        if original_code is None:
            original_code = dot_code
        escaped_original = json.dumps(original_code)
        
        # Get VizJS content from local file
        viz_js_content = self.get_static_js_content("viz-lite.js") + "\n" + self.get_static_js_content("viz-full.js")
        if not viz_js_content:
            return f'<div class="error">VizJS not available. DOT code:<br><pre>{dot_code}</pre></div>'
        
        # Get template and substitute variables
        template = self.get_template_content("vizjs.html")
        if not template:
            return f'<div class="error">VizJS template not available. DOT code:<br><pre>{dot_code}</pre></div>'
        
        # Use replace instead of format to avoid issues with CSS curly braces
        html = template.replace('{viz_js_content}', viz_js_content)
        html = html.replace('{escaped_dot}', escaped_dot)
        html = html.replace('{escaped_original}', escaped_original)
        return html
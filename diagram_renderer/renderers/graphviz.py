from .base import BaseRenderer
import json


class GraphvizRenderer(BaseRenderer):
    """Renderer for Graphviz DOT diagrams using VizJS"""
    
    
    
    def detect_diagram_type(self, code):
        """Detect if code is Graphviz DOT notation"""
        code = code.strip().lower()
        
        # Strong Graphviz indicators (must be at start of line)
        lines = code.split('\n')
        first_non_empty = None
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('#'):
                first_non_empty = stripped
                break
        
        if first_non_empty:
            # Must start with exact DOT keywords
            if (first_non_empty.startswith('digraph ') or 
                first_non_empty.startswith('strict graph ') or
                first_non_empty.startswith('strict digraph ') or
                first_non_empty.startswith('subgraph ')):
                return True
            elif first_non_empty.startswith('graph '):
                # "graph" could be Mermaid or DOT, need more specific checks
                # Mermaid: "graph TD", "graph LR", etc.
                # DOT: "graph name {" or "graph {"
                parts = first_non_empty.split()
                if len(parts) >= 2:
                    second_part = parts[1]
                    # Mermaid direction indicators
                    if second_part in ['td', 'lr', 'rl', 'bt', 'tb']:
                        return False  # This is Mermaid
                    # DOT graph name or opening brace
                    if second_part == '{' or (len(parts) >= 3 and parts[2] == '{'):
                        return True  # This is DOT
                return False
        
        # Check for typical DOT syntax patterns
        dot_patterns = [
            " -> ",  # directed edges
            " -- ",  # undirected edges
            "[label=", "[color=", "[shape=", "[style="  # attributes
        ]
        
        # Must have graph declaration AND dot patterns
        strong_graphviz_indicators = ['digraph ', 'strict graph ', 'strict digraph ', 'subgraph ', 'graph ']
        has_graph_decl = any(indicator in code for indicator in strong_graphviz_indicators)
        has_dot_syntax = any(pattern in code for pattern in dot_patterns)
        
        return has_graph_decl and has_dot_syntax
    
    def clean_code(self, code):
        """Remove markdown formatting from DOT code"""
        return code.strip()
    
    
    
    def render_html(self, code, **kwargs):
        """Generate Graphviz diagram as HTML using VizJS"""
        if not self.use_local_rendering:
            raise Exception("Local rendering disabled")
        
        try:
            clean_dot = self.clean_code(code)
            return self._render_vizjs_html(clean_dot, original_code=code)
        except Exception as e:
            raise Exception(f"Error rendering Graphviz diagram: {str(e)}")
import streamlit as st
import streamlit.components.v1 as components
from diagram_renderer import DiagramRenderer

class StreamlitDiagramRenderer:
    """Streamlit-specific wrapper for DiagramRenderer"""
    
    def __init__(self):
        self.renderer = DiagramRenderer()
    
    def render_diagram_auto(self, code, height=600):
        """Automatically detect diagram type and render accordingly"""
        try:
            html_content = self.renderer.render_diagram_auto(code)
            
            if html_content is not None:
                components.html(html_content, height=height, width=None, scrolling=False)
                return True
            else:
                # If html_content is None, it means no diagram was detected/rendered
                return False
        except Exception as e:
            st.error(f"❌ Error rendering diagram: {str(e)}")
            return False

    def detect_diagram_type(self, code):
        """Detect diagram type"""
        return self.renderer.detect_diagram_type(code)
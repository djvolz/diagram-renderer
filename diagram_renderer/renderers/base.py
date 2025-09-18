import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from ..resource_cache import get_cached_resource
from ..template_engine import TemplateEngine

# Template name constants
TEMPLATE_UNIFIED = "unified.html"


class BaseRenderer(ABC):
    """Base class for diagram renderers"""

    def __init__(self) -> None:
        """Initialize the base renderer."""
        # Get static directory relative to this module
        module_dir = Path(__file__).parent  # diagram/renderers
        self.static_dir = module_dir / "static"
        self.use_local_rendering = True
        self.template_engine = TemplateEngine()

    @abstractmethod
    def render_html(self, code: str, **kwargs: Any) -> str:
        """Render diagram as HTML.

        Args:
            code: Diagram source code
            **kwargs: Additional rendering options

        Returns:
            Complete HTML document with rendered diagram
        """
        pass

    @abstractmethod
    def clean_code(self, code: str) -> str:
        """Clean diagram code (remove markdown formatting).

        Args:
            code: Raw diagram code potentially with markdown

        Returns:
            Cleaned diagram code
        """
        pass

    def detect_diagram_type(self, code: str) -> bool:
        """Detect if code matches this renderer type.

        Args:
            code: Diagram code to check

        Returns:
            True if this renderer can handle the code
        """
        # To be implemented by subclasses
        return False

    def get_static_js_content(self, filename: str) -> Optional[str]:
        """Get JavaScript content from static file with caching.

        Args:
            filename: Name of the JavaScript file

        Returns:
            JavaScript content or None if not found
        """
        # Use the resource cache for efficient loading
        fallback_paths = [self.static_dir / "js"]
        return get_cached_resource(
            resource_type="static/js", filename=filename, fallback_paths=fallback_paths
        )

    def get_template_content(self, filename: str) -> Optional[str]:
        """Get HTML template content from templates directory with caching.

        Args:
            filename: Name of the template file

        Returns:
            Template content or None if not found
        """
        # Define fallback paths for template loading
        fallback_paths = [Path(__file__).parent / "templates", self.static_dir.parent / "templates"]

        # Use the resource cache for efficient loading
        return get_cached_resource(
            resource_type="templates", filename=filename, fallback_paths=fallback_paths
        )

    def _generate_error_html(self, error_message: str) -> str:
        """Generate user-friendly error HTML for renderer-level failures.

        Args:
            error_message: The error message to display

        Returns:
            Complete HTML error page
        """
        return self.template_engine.generate_error_html(
            error_type="Rendering Error", error_message=error_message, show_help=True
        )

    def _render_unified_html(
        self, dot_code: str, original_code: str, diagram_type: str = "diagram"
    ) -> str:
        """Generate HTML using unified template with VizJS rendering.

        Args:
            dot_code: GraphViz DOT format code
            original_code: Original diagram code before conversion
            diagram_type: Type of diagram being rendered

        Returns:
            Complete HTML document with rendered diagram
        """
        # Get required JavaScript libraries
        panzoom_js = self.get_static_js_content("panzoom.min.js")
        viz_js = self._get_vizjs_content()

        if not panzoom_js:
            return self._generate_error_html("Panzoom.js not available")
        if not viz_js:
            return self._generate_error_html("VizJS not available")

        # Get and populate template
        template = self.get_template_content(TEMPLATE_UNIFIED)
        if not template:
            return self._generate_error_html("Unified template not available")

        # Generate VizJS rendering script
        vizjs_script = self._generate_vizjs_rendering_script(dot_code)

        # Replace template placeholders
        return self._populate_unified_template(
            template, viz_js, panzoom_js, original_code, vizjs_script
        )

    def _get_vizjs_content(self) -> Optional[str]:
        """Get combined VizJS library content.

        Returns:
            Combined JavaScript content or None if not found
        """
        viz_lite = self.get_static_js_content("viz-lite.js")
        viz_full = self.get_static_js_content("viz-full.js")
        return f"{viz_lite}\n{viz_full}" if viz_lite and viz_full else None

    def _generate_vizjs_rendering_script(self, dot_code: str) -> str:
        """Generate JavaScript for VizJS diagram rendering.

        Args:
            dot_code: GraphViz DOT format code

        Returns:
            JavaScript code for rendering the diagram
        """
        escaped_dot = json.dumps(dot_code)

        return f"""        // VizJS rendering (matches working vizjs.html)
        function renderDiagram() {{
            try {{
                loading.style.display = 'none';
                diagramContent.style.display = 'block';

                if (typeof Viz !== 'undefined') {{
                    const viz = new Viz();
                    const dotString = {escaped_dot};
                    viz.renderSVGElement(dotString).then(function(svgElement) {{
                        diagramContent.innerHTML = '';

                        // Ensure readable styling for Graphviz diagrams
                        if (svgElement && svgElement.tagName === 'svg') {{
                            svgElement.style.backgroundColor = 'white';
                            // Force text to be black for readability
                            const textElements = svgElement.querySelectorAll('text');
                            textElements.forEach(function(text) {{
                                if (!text.getAttribute('fill') || text.getAttribute('fill') === 'black') {{
                                    text.setAttribute('fill', 'black');
                                }}
                            }});
                        }}

                        diagramContent.appendChild(svgElement);

                        // Initialize pan/zoom after SVG is rendered
                        setTimeout(() => {{
                            initializePanZoom();
                            diagramReady = true;
                        }}, 100);

                    }}).catch(function(error) {{
                        console.error('VizJS render error:', error);
                        diagramContent.innerHTML = '<div class="error-message">VizJS Render Error: ' + error.message + '</div>';
                    }});
                }} else {{
                    diagramContent.innerHTML = '<div class="error-message">VizJS not available.</div>';
                }}
            }} catch (error) {{
                console.error('Script error:', error);
                diagramContent.innerHTML = '<div class="error-message">Script Error: ' + error.message + '</div>';
            }}
        }}"""

    def _populate_unified_template(
        self, template: str, viz_js: str, panzoom_js: str, original_code: str, vizjs_script: str
    ) -> str:
        """Replace all placeholders in the unified template.

        Args:
            template: HTML template content
            viz_js: VizJS JavaScript content
            panzoom_js: Panzoom JavaScript content
            original_code: Original diagram code
            vizjs_script: VizJS rendering script

        Returns:
            Populated HTML template
        """
        escaped_original = json.dumps(original_code)

        # Define the default render function to be replaced
        default_render_function = """        // Diagram rendering function - to be overridden by specific renderers
        function renderDiagram() {
            // Default implementation - just show the content
            loading.style.display = 'none';
            diagramContent.style.display = 'block';

            // Initialize pan/zoom after content is ready
            setTimeout(() => {
                initializePanZoom();
                diagramReady = true;
            }, 100);
        }"""

        # Replace all template variables
        html = template.replace("{js_content}", viz_js)
        html = html.replace("{panzoom_js_content}", panzoom_js)
        html = html.replace("{diagram_content}", "")  # Content will be set by JS
        html = html.replace("{escaped_original}", escaped_original)
        html = html.replace(default_render_function, vizjs_script)

        return html

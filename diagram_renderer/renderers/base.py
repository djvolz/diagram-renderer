import json
from abc import ABC, abstractmethod
from pathlib import Path

# Template name constants
TEMPLATE_UNIFIED = "unified.html"


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
        # Try using importlib.resources first (recommended for package data)
        try:
            from importlib.resources import files

            js_dir = files("diagram_renderer.renderers") / "static" / "js"
            js_file = js_dir / filename
            if js_file.is_file():
                return js_file.read_text(encoding="utf-8")
        except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
            pass

        # Fallback to file system path
        js_file = self.static_dir / "js" / filename
        if js_file.exists():
            with open(js_file, encoding="utf-8") as f:
                return f.read()
        return None

    def get_template_content(self, filename):
        """Get HTML template content from templates directory"""
        # Try using importlib.resources first (recommended for package data)
        try:
            from importlib.resources import files

            template_dir = files("diagram_renderer.renderers") / "templates"
            template_file = template_dir / filename
            if template_file.is_file():
                return template_file.read_text(encoding="utf-8")
        except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
            # Try older importlib.resources API (Python 3.8)
            try:
                import importlib.resources as pkg_resources

                with pkg_resources.path(
                    "diagram_renderer.renderers", "templates"
                ) as templates_path:
                    template_file = templates_path / filename
                    if template_file.exists():
                        return template_file.read_text(encoding="utf-8")
            except (ImportError, FileNotFoundError, ModuleNotFoundError, AttributeError):
                pass

        # Fallback to file system paths with more comprehensive search
        possible_paths = [
            # From current module directory
            Path(__file__).parent / "templates" / filename,
            # From static_dir parent (renderers/templates/)
            self.static_dir.parent / "templates" / filename,
            # From package root
            Path(__file__).parent.parent / "renderers" / "templates" / filename,
            # Alternative package structure
            Path(__file__).resolve().parent / "templates" / filename,
        ]

        for template_file in possible_paths:
            try:
                if template_file.exists() and template_file.is_file():
                    with open(template_file, encoding="utf-8") as f:
                        return f.read()
            except OSError:
                continue

        # Debug info for troubleshooting
        import os

        debug_info = f"Template '{filename}' not found. Tried importlib.resources and paths:\n"
        for path in possible_paths:
            try:
                exists = path.exists()
            except Exception:
                exists = "error"
            debug_info += f"  - {path} (exists: {exists})\n"
        debug_info += f"Current working directory: {os.getcwd()}\n"
        debug_info += f"Module file location: {__file__}\n"

        # Try to list what's actually in the templates directory if it exists
        templates_dir = Path(__file__).parent / "templates"
        if templates_dir.exists():
            debug_info += f"Templates directory contents: {list(templates_dir.iterdir())}\n"
        else:
            debug_info += f"Templates directory does not exist at: {templates_dir}\n"

        print(debug_info)  # This will show in test output
        return None

    def _generate_error_html(self, error_message):
        """Generate consistent error HTML"""
        return f"<div>Error: {error_message}</div>"

    def _render_unified_html(self, dot_code, original_code, diagram_type="diagram"):
        """Generate HTML using unified template with VizJS rendering"""
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

    def _get_vizjs_content(self):
        """Get combined VizJS library content"""
        viz_lite = self.get_static_js_content("viz-lite.js")
        viz_full = self.get_static_js_content("viz-full.js")
        return f"{viz_lite}\n{viz_full}" if viz_lite and viz_full else None

    def _generate_vizjs_rendering_script(self, dot_code):
        """Generate JavaScript for VizJS diagram rendering"""
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

    def _populate_unified_template(self, template, viz_js, panzoom_js, original_code, vizjs_script):
        """Replace all placeholders in the unified template"""
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

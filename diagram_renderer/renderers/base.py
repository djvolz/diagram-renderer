import json
from abc import ABC, abstractmethod
from pathlib import Path


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

    def _render_vizjs_html(self, dot_code, original_code=None):
        """Generate HTML with VizJS to render DOT notation as SVG"""
        # Use JSON.stringify equivalent escaping to safely embed DOT code
        escaped_dot = json.dumps(dot_code)

        # If no original code provided, use the dot code
        if original_code is None:
            original_code = dot_code
        escaped_original = json.dumps(original_code)

        # Get VizJS content from local file
        viz_js_content = (
            self.get_static_js_content("viz-lite.js")
            + "\n"
            + self.get_static_js_content("viz-full.js")
        )
        if not viz_js_content:
            return (
                f'<div class="error">VizJS not available. DOT code:<br><pre>{dot_code}</pre></div>'
            )

        # Get template and substitute variables
        template = self.get_template_content("vizjs.html")
        if not template:
            return (
                f'<div class="error">VizJS template not available. '
                f"DOT code:<br><pre>{dot_code}</pre></div>"
            )

        # Use replace instead of format to avoid issues with CSS curly braces
        html = template.replace("{viz_js_content}", viz_js_content)
        html = html.replace("{escaped_dot}", escaped_dot)
        html = html.replace("{escaped_original}", escaped_original)
        return html

    def _render_unified_html(self, dot_code, original_code, diagram_type="diagram"):
        """Generate HTML using unified template with VizJS rendering"""
        panzoom_js_content = self.get_static_js_content("panzoom.min.js")

        # Get VizJS content
        viz_js_content = (
            self.get_static_js_content("viz-lite.js")
            + "\n"
            + self.get_static_js_content("viz-full.js")
        )

        if not panzoom_js_content:
            return "<div>Error: Panzoom.js not available</div>"

        if not viz_js_content:
            return "<div>Error: VizJS not available</div>"

        # Escape original code for JavaScript
        import json

        escaped_original = json.dumps(original_code)
        escaped_dot = json.dumps(dot_code)

        # Get unified template
        template = self.get_template_content("unified.html")
        if not template:
            return "<div>Error: Unified template not available</div>"

        # VizJS rendering script with correct API
        vizjs_rendering_script = f"""        // VizJS rendering
        function renderDiagram() {{
            try {{
                loading.style.display = 'none';

                // Create div for SVG output
                diagramContent.innerHTML = '<div id="svg-output"></div>';
                diagramContent.style.display = 'block';

                // Render DOT to SVG using correct VizJS API
                if (typeof Viz !== 'undefined') {{
                    const dotCode = {escaped_dot};
                    const viz = new Viz();
                    viz.renderSVGElement(dotCode).then(function(svgElement) {{
                        const outputDiv = document.getElementById('svg-output');
                        outputDiv.innerHTML = '';
                        outputDiv.appendChild(svgElement);

                        // Initialize pan/zoom after SVG is rendered
                        setTimeout(() => {{
                            initializePanZoom();
                            diagramReady = true;
                        }}, 200);

                    }}).catch(function(vizError) {{
                        console.error('VizJS error:', vizError);
                        document.getElementById('svg-output').innerHTML =
                            '<div class="error-message"><strong>Error rendering diagram:</strong><br>' +
                            vizError.message + '<br><br><strong>Original code:</strong><br><pre>{escaped_original}</pre></div>';
                    }});
                }} else {{
                    document.getElementById('svg-output').innerHTML =
                        '<div class="error-message"><strong>Error:</strong><br>VizJS not available</div>';
                }}

            }} catch (error) {{
                console.error('Diagram rendering error:', error);
                loading.style.display = 'none';
                diagramContent.innerHTML = `
                    <div class="error-message">
                        <strong>Error rendering diagram:</strong><br>
                        ${{error.message}}
                        <br><br>
                        <strong>Original code:</strong><br>
                        <pre>{escaped_original}</pre>
                    </div>
                `;
                diagramContent.style.display = 'block';
            }}
        }}"""

        # Replace template variables
        html = template.replace("{js_content}", viz_js_content)
        html = html.replace("{panzoom_js_content}", panzoom_js_content)
        html = html.replace("{diagram_content}", "")  # Content will be set by JS
        html = html.replace("{escaped_original}", escaped_original)

        # Replace the default renderDiagram function
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

        html = html.replace(default_render_function, vizjs_rendering_script)

        return html

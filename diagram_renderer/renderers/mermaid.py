import json

from .base import TEMPLATE_UNIFIED, BaseRenderer


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
            "graph ",
            "flowchart ",
            "sequencediagram",
            "classdiagram",
            "statediagram",
            "erdiagram",
            "journey",
            "gantt",
            "pie ",
            "gitgraph",
            "requirement",
            "mindmap",
        ]

        # Check for strong indicators
        for indicator in strong_mermaid_indicators:
            if indicator in code:
                return True

        # Weak indicators - check context for participant/actor usage
        if "participant " in code or "actor " in code:
            # Check if it looks like Mermaid sequence diagram
            if (
                "sequencediagram" in code
                or "-->" in code
                or "->>" in code
                or ("participant " in code and ("as " in code or ":" in code))
            ):
                return True

        return False

    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        return code.strip()

    def render_html(self, code, **kwargs):
        """Generate HTML with improved UI using embedded Mermaid.js and panzoom"""
        # Get required JavaScript libraries
        mermaid_js = self.get_static_js_content(self.js_filename)
        panzoom_js = self.get_static_js_content("panzoom.min.js")

        if not mermaid_js:
            return self._generate_error_html("Mermaid.js not available")
        if not panzoom_js:
            return self._generate_error_html("Panzoom.js not available")

        # Process diagram code
        clean_code = self.clean_code(code)
        escaped_original = json.dumps(code)

        # Get and populate template
        template = self.get_template_content(TEMPLATE_UNIFIED)
        if not template:
            return self._generate_error_html("Unified template not available")

        # Generate Mermaid-specific rendering script
        mermaid_script = self._generate_mermaid_rendering_script(clean_code, escaped_original)

        # Replace template placeholders
        return self._populate_mermaid_template(
            template, mermaid_js, panzoom_js, clean_code, escaped_original, mermaid_script
        )

    def _generate_error_html(self, error_message):
        """Generate consistent error HTML"""
        return f"<div>Error: {error_message}</div>"

    def _generate_mermaid_rendering_script(self, clean_code, escaped_original):
        """Generate JavaScript for Mermaid diagram rendering"""
        return f"""        // Mermaid rendering
        async function renderDiagram() {{
            try {{
                loading.style.display = 'flex';
                diagramContent.style.display = 'none';

                mermaid.initialize({{
                    startOnLoad: false,
                    theme: 'default',
                    securityLevel: 'loose',
                    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
                    flowchart: {{
                        useMaxWidth: false,
                        htmlLabels: true
                    }},
                    sequence: {{
                        useMaxWidth: false
                    }},
                    gantt: {{
                        useMaxWidth: false
                    }}
                }});

                const code = `{clean_code}`;
                const {{ svg }} = await mermaid.render('mermaid-diagram-svg', code);

                diagramContent.innerHTML = svg;
                loading.style.display = 'none';
                diagramContent.style.display = 'block';

                // Initialize pan/zoom after rendering
                setTimeout(() => {{
                    initializePanZoom();
                    diagramReady = true;
                }}, 100);

            }} catch (error) {{
                console.error('Mermaid rendering error:', error);
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

    def _populate_mermaid_template(
        self, template, mermaid_js, panzoom_js, clean_code, escaped_original, mermaid_script
    ):
        """Replace all placeholders in the template for Mermaid rendering"""
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

        # Replace template variables
        html = template.replace("{js_content}", mermaid_js)
        html = html.replace("{panzoom_js_content}", panzoom_js)
        html = html.replace("{diagram_content}", f'<div class="mermaid">{clean_code}</div>')
        html = html.replace("{escaped_original}", escaped_original)
        html = html.replace(default_render_function, mermaid_script)

        return html

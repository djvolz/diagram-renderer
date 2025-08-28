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
        # Use the improved template by default
        use_legacy = kwargs.get("use_legacy", False)

        if use_legacy:
            return self._render_html_legacy(code, **kwargs)
        else:
            return self.render_html_improved(code, **kwargs)

    def render_html_improved(self, code, **kwargs):
        """Generate HTML with improved UI using unified template"""
        mermaid_js_content = self.get_static_js_content(self.js_filename)
        panzoom_js_content = self.get_static_js_content("panzoom.min.js")

        if not mermaid_js_content:
            return "<div>Error: Mermaid.js not available</div>"

        if not panzoom_js_content:
            return "<div>Error: Panzoom.js not available</div>"

        # Clean mermaid code
        clean_code = self.clean_code(code)

        # Escape original code for JavaScript
        import json

        escaped_original = json.dumps(code)

        # Get unified template
        template = self.get_template_content("unified.html")
        if not template:
            return "<div>Error: Unified template not available</div>"

        # Mermaid-specific rendering logic
        mermaid_rendering_script = f"""
        // Mermaid rendering
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

        # Replace template variables
        html = template.replace("{js_content}", mermaid_js_content)
        html = html.replace("{panzoom_js_content}", panzoom_js_content)
        html = html.replace("{diagram_content}", f'<div class="mermaid">{clean_code}</div>')
        html = html.replace("{escaped_original}", escaped_original)

        # Replace the default renderDiagram function with Mermaid-specific one
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

        html = html.replace(default_render_function, mermaid_rendering_script)

        return html

    def _render_html_legacy(self, code, **kwargs):
        """Generate HTML with embedded Mermaid.js (legacy template)"""
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
        html = template.replace("{mermaid_js_content}", mermaid_js_content)
        html = html.replace("{clean_code}", clean_code)
        html = html.replace("{escaped_original}", escaped_original)
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
        html = template.replace("{mermaid_js_content}", mermaid_js_content)
        html = html.replace("{theme}", theme)
        html = html.replace("{clean_code}", clean_code)
        return html

    def render_html_external(
        self, code, static_js_path="diagram_renderer/renderers/static/js/mermaid.min.js", **kwargs
    ):
        """Generate HTML with external script reference instead of embedded JS"""
        # Clean mermaid code
        clean_code = self.clean_code(code)

        # Escape original code for JavaScript
        import json

        escaped_original = json.dumps(code)

        # Get template and substitute variables
        template = self.get_template_content("mermaid-external.html")
        if not template:
            return "<div>Error: Mermaid external template not available</div>"

        # Use replace instead of format to avoid issues with CSS curly braces
        html = template.replace("{static_js_path}", static_js_path)
        html = html.replace("{clean_code}", clean_code)
        html = html.replace("{escaped_original}", escaped_original)
        return html

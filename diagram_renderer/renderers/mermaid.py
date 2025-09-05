import json

from ..error_pages import generate_simple_error_html, generate_unsupported_diagram_error_html
from ..external_diagrams import (
    detect_external_diagram_requirements,
    get_external_diagram_indicators,
)
from .base import TEMPLATE_UNIFIED, BaseRenderer


class MermaidRenderer(BaseRenderer):
    """Renderer for Mermaid diagrams"""

    def __init__(self):
        super().__init__()
        self.js_filename = "mermaid.min.js"

    def detect_diagram_type(self, code):
        """Detect if code is Mermaid"""
        code_lower = code.strip().lower()

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
            "mindmap",
            "timeline",
            "c4context",
            "quadrantchart",
            "requirement",
            "requirementdiagram",
        ]

        # Get external diagram indicators from configuration
        external_diagram_indicators = get_external_diagram_indicators()

        # Check for strong indicators
        for indicator in strong_mermaid_indicators:
            if indicator in code_lower:
                return True

        # Check for external diagrams (still Mermaid but need special handling)
        for indicator in external_diagram_indicators:
            if indicator in code_lower:
                return True

        # Weak indicators - check context for participant/actor usage
        if "participant " in code_lower or "actor " in code_lower:
            # Check if it looks like Mermaid sequence diagram
            if (
                "sequencediagram" in code_lower
                or "-->" in code_lower
                or "->>" in code_lower
                or ("participant " in code_lower and ("as " in code_lower or ":" in code_lower))
            ):
                return True

        return False

    def detect_external_diagram_requirements(self, code):
        """Detect if diagram requires external plugins and return requirement info"""
        # Delegate to centralized external diagram configuration
        return detect_external_diagram_requirements(code)

    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        return code.strip()

    def render_html(self, code, **kwargs):
        """Generate HTML with improved UI using embedded Mermaid.js and panzoom"""
        # Check for external diagram requirements first
        external_requirements = self.detect_external_diagram_requirements(code)

        # Get required JavaScript libraries
        mermaid_js = self.get_static_js_content(self.js_filename)
        panzoom_js = self.get_static_js_content("panzoom.min.js")

        if not mermaid_js:
            return generate_simple_error_html("Mermaid.js not available")
        if not panzoom_js:
            return generate_simple_error_html("Panzoom.js not available")

        # Check for missing external plugins and provide helpful error
        missing_plugins = []
        xychart_js = self.get_static_js_content("mermaid-xychart.min.js")
        sankey_js = self.get_static_js_content("mermaid-sankey.min.js")

        for req in external_requirements:
            if req["type"] == "xychart-beta" and not xychart_js:
                missing_plugins.append(req)
            elif req["type"] == "sankey" and not sankey_js:
                missing_plugins.append(req)
            elif req["type"] == "block-beta":
                # Block diagrams are not fully supported in current Mermaid bundle
                missing_plugins.append(req)
            elif req["type"] == "gitgraph":
                # Git graphs are not fully supported in current Mermaid bundle
                missing_plugins.append(req)
            # Requirement diagrams should work with current Mermaid bundle

        if missing_plugins:
            return generate_unsupported_diagram_error_html(missing_plugins, code)

        # Process diagram code
        clean_code = self.clean_code(code)
        escaped_original = json.dumps(code)

        # Get and populate template
        template = self.get_template_content(TEMPLATE_UNIFIED)
        if not template:
            return generate_simple_error_html("Unified template not available")

        # Generate Mermaid-specific rendering script
        mermaid_script = self._generate_mermaid_rendering_script(clean_code, escaped_original)

        # Include available external plugins
        if xychart_js:
            mermaid_js = f"{mermaid_js}\n\n/* mermaid-xychart plugin */\n{xychart_js}"
        if sankey_js:
            mermaid_js = f"{mermaid_js}\n\n/* mermaid-sankey plugin */\n{sankey_js}"

        return self._populate_mermaid_template(
            template, mermaid_js, panzoom_js, clean_code, escaped_original, mermaid_script
        )

    # Error generation methods moved to shared error_pages module

    def _generate_mermaid_rendering_script(self, clean_code, escaped_original):
        """Generate JavaScript for Mermaid diagram rendering"""
        return f"""        // Mermaid rendering
        async function renderDiagram() {{
            try {{
                loading.style.display = 'flex';
                diagramContent.style.display = 'none';

                // Register external/beta diagrams if available (e.g., xychart-beta, sankey)
                try {{
                    if (typeof mermaid !== 'undefined') {{
                        const plugins = [];
                        // Known globals from plugin UMD builds
                        if (globalThis.mermaidXychart || globalThis.mermaidXYChart) {{
                            plugins.push(globalThis.mermaidXychart || globalThis.mermaidXYChart);
                        }}
                        if (globalThis.mermaidSankey || globalThis.mermaid_sankey) {{
                            plugins.push(globalThis.mermaidSankey || globalThis.mermaid_sankey);
                        }}
                        if (plugins.length && typeof mermaid.registerExternalDiagrams === 'function') {{
                            mermaid.registerExternalDiagrams(plugins);
                        }}
                    }}
                }} catch (e) {{
                    console.warn('Optional Mermaid external diagram registration failed:', e);
                }}

                mermaid.initialize({{
                    startOnLoad: false,
                    theme: 'default',
                    securityLevel: 'loose',
                    suppressErrorRendering: false,
                    externalDiagrams: [],
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
                    }},
                    class: {{
                        useMaxWidth: false
                    }},
                    state: {{
                        useMaxWidth: false
                    }},
                    er: {{
                        useMaxWidth: false
                    }},
                    pie: {{
                        useMaxWidth: false
                    }},
                    journey: {{
                        useMaxWidth: false
                    }},
                    timeline: {{
                        useMaxWidth: false
                    }},
                    quadrantChart: {{
                        useMaxWidth: false
                    }},
                    requirement: {{
                        useMaxWidth: false
                    }},
                    c4: {{
                        useMaxWidth: false
                    }},
                    block: {{
                        useMaxWidth: false
                    }}
                }});

                const code = `{clean_code}`;
                // Helpful guidance when external diagrams are used but plugins aren't bundled
                const lc = code.trim().toLowerCase();
                if (lc.startsWith('xychart-beta') && !(globalThis.mermaidXychart || globalThis.mermaidXYChart)) {{
                    throw new Error('xychart-beta requires mermaid-xychart. Bundle static/js/mermaid-xychart.min.js and ensure registration.');
                }}
                if (lc.startsWith('sankey') && !(globalThis.mermaidSankey || globalThis.mermaid_sankey)) {{
                    throw new Error('sankey requires mermaid-sankey. Bundle static/js/mermaid-sankey.min.js and ensure registration.');
                }}

                // Attempt to render the diagram
                const result = await mermaid.render('mermaid-diagram-svg', code);
                const svg = result && result.svg ? result.svg : '';

                // Check if SVG is valid and contains actual diagram content
                if (!svg || typeof svg !== 'string' || !svg.trim()) {{
                    throw new Error('Mermaid returned no SVG output. This diagram may be unsupported by the bundled Mermaid version.');
                }}

                // Check for common signs of failed rendering
                if (svg.length < 100 || !svg.includes('<svg')) {{
                    throw new Error('Mermaid returned invalid SVG. The diagram type may not be supported.');
                }}

                // Additional validation - check if SVG has meaningful content
                if (!svg.includes('<g') && !svg.includes('<rect') && !svg.includes('<circle') && !svg.includes('<path')) {{
                    throw new Error('Mermaid returned empty diagram. Check diagram syntax and type compatibility.');
                }}

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

import re

from .__version__ import __version__
from .renderers import GraphvizRenderer, MermaidRenderer, PlantUMLRenderer


class DiagramRenderer:
    """Main diagram renderer that delegates to specialized renderers"""

    def __init__(self):
        # Order matters: detect Mermaid first to avoid false positives when
        # Mermaid keywords are present (e.g., gantt, gitgraph).
        self.renderers = [
            ("mermaid", MermaidRenderer()),
            ("plantuml", PlantUMLRenderer()),
            ("graphviz", GraphvizRenderer()),
        ]

    def _extract_all_code_blocks(self, code, prefixes):
        """
        Extracts all code blocks from a markdown string.
        Tries to find ```<prefix>\n...\n``` or ```\n...\n```
        Returns a list of extracted code strings.
        """
        extracted_blocks = []
        for prefix in prefixes:
            pattern = re.compile(
                r"```" + re.escape(prefix) + r"\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE
            )
            extracted_blocks.extend(pattern.findall(code))

        # Fallback for generic ```\n...\n``` if no specific prefix matches
        # Ensure we don't double-extract if a prefixed block was already found
        generic_pattern = re.compile(r"```\s*\n(.*?)\n```", re.DOTALL)
        generic_blocks = generic_pattern.findall(code)

        # Add generic blocks only if they are not already part of a prefixed block
        for g_block in generic_blocks:
            is_duplicate = False
            for p_block in extracted_blocks:
                if g_block in p_block or p_block in g_block:  # Simple check for containment
                    is_duplicate = True
                    break
            if not is_duplicate:
                extracted_blocks.append(g_block)

        return [block.strip() for block in extracted_blocks if block.strip()]

    def detect_diagram_type(self, code):
        """Detect diagram type using modular renderers"""
        # The code passed to detect_diagram_type is already cleaned of markdown fences
        for name, renderer in self.renderers:
            if renderer.detect_diagram_type(code):
                return name
        return None  # Return None if no specific type is detected

    def render_diagram_auto(self, code):
        """
        Automatically detect diagram type and render accordingly.

        Supports multiple diagrams in a single input by extracting markdown code blocks
        and rendering each one individually.

        Args:
            code (str): Input code that may contain one or more diagram definitions

        Returns:
            str: Combined HTML output for all detected diagrams, or empty string if none found
        """
        # Extract all potential code blocks
        all_extracted_codes = self._extract_all_code_blocks(
            code, ["mermaid", "plantuml", "uml", "dot", "graphviz"]
        )

        if not all_extracted_codes:
            # If no code blocks are found, try to process the entire input as a single diagram
            all_extracted_codes = [code]

        # Render each code block individually
        rendered_html_parts = []
        for code_to_process in all_extracted_codes:
            if not code_to_process.strip():
                continue

            rendered_html = self._render_single_diagram(code_to_process)
            if rendered_html:  # Only add non-empty results
                rendered_html_parts.append(rendered_html)

        if rendered_html_parts:
            # Combine all rendered HTML parts into a single HTML string
            return "\n".join(rendered_html_parts)
        else:
            return None  # Return None to indicate no diagrams were successfully rendered

    def _render_single_diagram(self, code_to_process):
        """
        Renders a single diagram code block using the appropriate renderer.

        Args:
            code_to_process (str): The diagram code to render

        Returns:
            str: Rendered HTML content, or error HTML if rendering fails
        """
        try:
            # Attempt to detect the appropriate renderer
            detected_renderer = None

            for name, renderer in self.renderers:
                if renderer.detect_diagram_type(code_to_process):
                    detected_renderer = renderer
                    break

            if detected_renderer:
                # Use the detected renderer
                final_cleaned_code = detected_renderer.clean_code(code_to_process)
                return detected_renderer.render_html(final_cleaned_code)
            else:
                # No specific type detected - generate helpful error
                return self._generate_no_diagram_detected_error_html(code_to_process)

        except Exception as e:
            # Generate user-friendly error HTML instead of None
            return self._generate_rendering_error_html(code_to_process, str(e))

    def _generate_no_diagram_detected_error_html(self, original_code):
        """Generate user-friendly HTML when no diagram type is detected"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Renderer - No Diagram Type Detected</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background-color: #f8f9fa;
            color: #24292e;
        }}
        .error-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        .error-icon {{ font-size: 48px; color: #f85149; margin-bottom: 16px; }}
        h1 {{ color: #f85149; margin: 0 0 16px 0; font-size: 24px; }}
        .code-block {{
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 14px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        .supported-types {{
            background: #e7f3ff;
            border: 1px solid #b6d7ff;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">🤔</div>
        <h1>No Diagram Type Detected</h1>
        <p>The provided code doesn't appear to be a recognized diagram format.</p>

        <p><strong>Your code:</strong></p>
        <div class="code-block">{original_code}</div>

        <div class="supported-types">
            <h3>Supported diagram types:</h3>
            <ul>
                <li><strong>Mermaid:</strong> flowchart, graph, sequenceDiagram, classDiagram, stateDiagram, erDiagram, gantt, pie, journey, gitGraph, requirement, mindmap</li>
                <li><strong>PlantUML:</strong> @startuml...@enduml blocks</li>
                <li><strong>Graphviz:</strong> digraph, graph, strict digraph, strict graph</li>
            </ul>
        </div>

        <p><strong>Common fixes:</strong></p>
        <ul>
            <li>Check that your diagram starts with the correct keyword (e.g., "flowchart TD", "sequenceDiagram", "@startuml")</li>
            <li>Ensure proper syntax for your chosen diagram type</li>
            <li>Remove any extra markdown formatting (backticks, language tags)</li>
        </ul>
    </div>
</body>
</html>"""

    def _generate_rendering_error_html(self, original_code, error_message):
        """Generate user-friendly HTML when rendering fails with an exception"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Renderer - Rendering Error</title>
    <meta name=\"diagram-render-status\" content=\"error\">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background-color: #f8f9fa;
            color: #24292e;
        }}
        .error-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        .error-icon {{ font-size: 48px; color: #f85149; margin-bottom: 16px; }}
        h1 {{ color: #f85149; margin: 0 0 16px 0; font-size: 24px; }}
        .code-block {{
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 14px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        .error-details {{
            background: #fff5f5;
            border: 1px solid #fecaca;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
            color: #991b1b;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">❌</div>
        <h1>Diagram Rendering Error</h1>
        <p>An error occurred while trying to render your diagram.</p>

        <div class="error-details">
            <h3>Error details:</h3>
            <p>{error_message}</p>
        </div>

        <p><strong>Your code:</strong></p>
        <div class="code-block">{original_code}</div>

        <p><strong>Common causes:</strong></p>
        <ul>
            <li>Syntax errors in the diagram code</li>
            <li>Unsupported diagram features</li>
            <li>Missing required plugins or libraries</li>
            <li>Malformed diagram structure</li>
        </ul>

        <p><strong>Suggestions:</strong></p>
        <ul>
            <li>Check the diagram syntax against the official documentation</li>
            <li>Try simplifying the diagram to isolate the issue</li>
            <li>Ensure all required dependencies are available</li>
        </ul>
    </div>
</body>
</html>"""


# Make all components available at package level
__all__ = ["DiagramRenderer", "MermaidRenderer", "PlantUMLRenderer", "GraphvizRenderer"]

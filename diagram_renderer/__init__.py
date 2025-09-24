import re
from typing import Optional

from .__version__ import __version__
from .error_pages import generate_rendering_error_html, generate_type_detection_error_html
from .renderers import GraphvizRenderer, MermaidRenderer, PlantUMLRenderer
from .renderers.base import BaseRenderer


class DiagramRenderer:
    """Main diagram renderer that delegates to specialized renderers"""

    def __init__(self) -> None:
        """Initialize the diagram renderer with available renderers.

        Order matters: detect Mermaid first to avoid false positives when
        Mermaid keywords are present (e.g., gantt, gitgraph).
        """
        self.renderers: list[tuple[str, BaseRenderer]] = [
            ("mermaid", MermaidRenderer()),
            ("plantuml", PlantUMLRenderer()),
            ("graphviz", GraphvizRenderer()),
        ]

    def _extract_all_code_blocks(self, code: str, prefixes: list[str]) -> list[str]:
        """
        Extract all code blocks from a markdown string.

        Tries to find ```<prefix>\n...\n``` or ```\n...\n```

        Args:
            code: Input markdown string
            prefixes: List of language prefixes to look for

        Returns:
            List of extracted code strings
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

    def detect_diagram_type(self, code: str) -> Optional[str]:
        """Detect diagram type using modular renderers.

        Args:
            code: Diagram code to analyze

        Returns:
            Name of detected diagram type or None if not detected
        """
        # The code passed to detect_diagram_type is already cleaned of markdown fences
        for name, renderer in self.renderers:
            if renderer.detect_diagram_type(code):
                return name
        return None  # Return None if no specific type is detected

    def render_diagram_auto(self, code: str) -> Optional[str]:
        """
        Automatically detect diagram type and render accordingly.

        Supports multiple diagrams in a single input by extracting markdown code blocks
        and rendering each one individually.

        Args:
            code: Input code that may contain one or more diagram definitions

        Returns:
            Combined HTML output for all detected diagrams, or None if none found
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

    def _render_single_diagram(self, code_to_process: str) -> str:
        """
        Render a single diagram code block using the appropriate renderer.

        Args:
            code_to_process: The diagram code to render

        Returns:
            Rendered HTML content, or error HTML if rendering fails
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
                return generate_type_detection_error_html(code_to_process)

        except Exception as e:
            # Generate user-friendly error HTML instead of None
            return generate_rendering_error_html(type(e).__name__, str(e), code_to_process)


# Make all components available at package level
__all__ = ["DiagramRenderer", "MermaidRenderer", "PlantUMLRenderer", "GraphvizRenderer"]

"""
Shared error HTML generation utilities for diagram renderers.

This module provides consistent error page generation across all renderer types.
"""

from typing import Any

from .template_engine import TemplateEngine


def generate_unsupported_diagram_error_html(
    missing_plugins: list[dict[str, Any]], original_code: str
) -> str:
    """Generate user-friendly error HTML for missing external plugins."""
    suggestions = []
    for plugin in missing_plugins:
        suggestions.append(f"{plugin['description']}")
        suggestions.append(f"Required file: static/js/{plugin['plugin_needed']}")

    error_message = (
        "This diagram type requires external plugins that are not included "
        "in the standard distribution."
    )

    return TemplateEngine.generate_error_html(
        error_type="Unsupported Diagram Type",
        error_message=error_message,
        original_code=original_code,
        suggestions=suggestions,
        show_help=True,
    )


def generate_simple_error_html(error_type: str, message: str, original_code: str) -> str:
    """Generate simple error HTML with standard formatting."""
    return TemplateEngine.generate_error_html(
        error_type=error_type, error_message=message, original_code=original_code, show_help=True
    )


def generate_rendering_error_html(
    exception_type: str, exception_message: str, diagram_code: str
) -> str:
    """Generate error HTML for rendering exceptions."""
    error_message = f"An error occurred while rendering the diagram: {exception_message}"

    suggestions = [
        "Check that your diagram syntax is correct",
        "Ensure all required dependencies are installed",
        f"Error type: {exception_type}",
    ]

    return TemplateEngine.generate_error_html(
        error_type="Rendering Error",
        error_message=error_message,
        original_code=diagram_code,
        suggestions=suggestions,
        show_help=True,
    )


def generate_type_detection_error_html(content: str) -> str:
    """Generate error HTML for diagram type detection failures."""
    # Truncate content for display if too long
    display_content = content[:500] + "..." if len(content) > 500 else content

    error_message = (
        "Could not determine the diagram type from the provided content. "
        "Please ensure your diagram starts with a valid declaration."
    )

    suggestions = [
        "Mermaid diagrams should start with: graph, flowchart, sequenceDiagram, etc.",
        "PlantUML diagrams should start with: @startuml",
        "Graphviz diagrams should start with: digraph, graph, or strict (di)graph",
    ]

    return TemplateEngine.generate_error_html(
        error_type="Unknown Diagram Type",
        error_message=error_message,
        original_code=display_content,
        suggestions=suggestions,
        show_help=True,
    )

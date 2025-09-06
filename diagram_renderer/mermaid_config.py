"""
Mermaid configuration management for diagram rendering.

This module centralizes Mermaid.js configuration to make it easily customizable
and maintainable across different rendering contexts.
"""

from typing import Any


def get_default_mermaid_config() -> dict[str, Any]:
    """
    Get the default Mermaid configuration for reliable diagram rendering.

    Returns:
        Dictionary containing Mermaid.js initialization configuration
    """
    return {
        "startOnLoad": False,
        "theme": "default",
        "securityLevel": "loose",
        "suppressErrorRendering": False,
        "externalDiagrams": [],
        "fontFamily": '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        # Diagram-specific configurations with consistent useMaxWidth: false
        "flowchart": {"useMaxWidth": False, "htmlLabels": True},
        "sequence": {"useMaxWidth": False},
        "gantt": {"useMaxWidth": False},
        "class": {"useMaxWidth": False},
        "state": {"useMaxWidth": False},
        "er": {"useMaxWidth": False},
        "pie": {"useMaxWidth": False},
        "journey": {"useMaxWidth": False},
        "timeline": {"useMaxWidth": False},
        "quadrantChart": {"useMaxWidth": False},
        "requirement": {"useMaxWidth": False},
        "c4": {"useMaxWidth": False},
        "block": {"useMaxWidth": False},
    }


def format_mermaid_config_for_js(config: dict[str, Any]) -> str:
    """
    Format Mermaid configuration as JavaScript object string for embedding.

    Args:
        config: Mermaid configuration dictionary

    Returns:
        JavaScript object literal string with proper escaping for f-strings
    """

    def format_value(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, list):
            return "[]"
        elif isinstance(value, dict):
            items = []
            for k, v in value.items():
                items.append(f"{k}: {format_value(v)}")
            return "{" + ", ".join(items) + "}"
        else:
            return str(value)

    config_items = []
    for key, value in config.items():
        # Use double braces for f-string escaping in JavaScript templates
        if isinstance(value, dict):
            inner_items = []
            for k, v in value.items():
                inner_items.append(f"{k}: {format_value(v)}")
            config_items.append(f"{key}: {{{', '.join(inner_items)}}}")
        else:
            config_items.append(f"{key}: {format_value(value)}")

    return "{" + ",\n                    ".join(config_items) + "}"


def get_mermaid_config_js() -> str:
    """
    Get Mermaid configuration formatted for JavaScript embedding.

    Returns:
        JavaScript configuration object string ready for f-string insertion
    """
    config = get_default_mermaid_config()
    return format_mermaid_config_for_js(config)

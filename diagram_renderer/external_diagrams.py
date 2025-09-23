"""
External diagram types configuration and requirements.

This module centralizes the configuration for external Mermaid diagram types
that require additional plugins or are not fully supported in the bundled version.
"""

from typing import Any


class ExternalDiagramType:
    """Configuration for an external diagram type"""

    def __init__(
        self, diagram_type: str, plugin_file: str, description: str, detection_patterns: list[str]
    ):
        self.diagram_type = diagram_type
        self.plugin_file = plugin_file
        self.description = description
        self.detection_patterns = detection_patterns


# External diagram types that require additional plugins or support
EXTERNAL_DIAGRAM_TYPES = [
    ExternalDiagramType(
        diagram_type="xychart-beta",
        plugin_file="mermaid-xychart.min.js",
        description="XY Chart (Beta) diagrams require the mermaid-xychart plugin",
        detection_patterns=["xychart-beta"],
    ),
    ExternalDiagramType(
        diagram_type="sankey",
        plugin_file="mermaid-sankey.min.js",
        description="Sankey diagrams require the mermaid-sankey plugin",
        detection_patterns=["sankey", "sankey-beta"],
    ),
    ExternalDiagramType(
        diagram_type="block-beta",
        plugin_file="mermaid-block.min.js",  # Using a proper plugin filename
        description="Block diagrams (beta) may require a newer Mermaid version with full block diagram support",
        detection_patterns=["block-beta"],
    ),
    # Note: gitgraph removed from external types as it's supported by our current Mermaid bundle
]


def detect_external_diagram_requirements(code: str) -> list[dict[str, Any]]:
    """
    Detect if diagram code requires external plugins and return requirement info.

    Args:
        code: The diagram code to analyze

    Returns:
        List of requirement dictionaries for any external diagram types detected
    """
    code_lower = code.strip().lower()
    requirements = []

    for external_type in EXTERNAL_DIAGRAM_TYPES:
        for pattern in external_type.detection_patterns:
            if code_lower.startswith(pattern) or pattern in code_lower:
                requirements.append(
                    {
                        "type": external_type.diagram_type,
                        "plugin_needed": external_type.plugin_file,
                        "description": external_type.description,
                    }
                )
                break  # Only add each type once

    return requirements


def get_external_diagram_indicators() -> list[str]:
    """Get list of all external diagram type indicators for detection"""
    indicators = []
    for external_type in EXTERNAL_DIAGRAM_TYPES:
        indicators.extend(external_type.detection_patterns)
    return indicators


def is_external_diagram_type(diagram_type: str) -> bool:
    """Check if a diagram type is considered external/unsupported"""
    return any(diagram_type == ext_type.diagram_type for ext_type in EXTERNAL_DIAGRAM_TYPES)

#!/usr/bin/env python3
"""
MCP Server for Diagram Renderer

Provides diagram rendering capabilities through the Model Context Protocol (MCP).
AI assistants can use this server to generate interactive HTML diagrams from
Mermaid, PlantUML, and Graphviz code.

Usage:
    # Install MCP dependencies
    uv sync --extra mcp

    # Run the MCP server
    uv run --extra mcp python examples/mcp_server.py

    # Or use via Claude Desktop configuration
"""

import asyncio
import json
import logging
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from mcp.server import NotificationOptions, Server
    from mcp.server.models import InitializationOptions
    from mcp.types import EmbeddedResource, ImageContent, LoggingLevel, Resource, TextContent, Tool
except ImportError:
    print("MCP dependencies not installed. Run: uv sync --extra mcp")
    sys.exit(1)

# Add parent directory to path to import diagram_renderer
sys.path.insert(0, str(Path(__file__).parent.parent))

from diagram_renderer import DiagramRenderer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("diagram-renderer-mcp")

# Initialize the MCP server
server = Server("diagram-renderer")

# Initialize diagram renderer
renderer = DiagramRenderer()


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="diagram://examples",
            name="Diagram Examples",
            description="Example diagrams for Mermaid, PlantUML, and Graphviz",
            mimeType="application/json",
        ),
        Resource(
            uri="diagram://supported-types",
            name="Supported Diagram Types",
            description="Information about supported diagram types and syntax",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource"""
    if uri == "diagram://examples":
        examples = {
            "mermaid": {
                "flowchart": "graph TD\n    A[Start] --> B{Decision}\n    B -->|Yes| C[Process A]\n    B -->|No| D[Process B]\n    C --> E[End]\n    D --> E",
                "sequence": "sequenceDiagram\n    participant A as Alice\n    participant B as Bob\n    A->>B: Hello Bob!\n    B-->>A: Hello Alice!",
                "class": "classDiagram\n    class Animal {\n        +String name\n        +int age\n        +makeSound()\n    }\n    class Dog {\n        +String breed\n        +bark()\n    }\n    Animal <|-- Dog",
            },
            "plantuml": {
                "class": "@startuml\nclass Animal {\n  +String name\n  +int age\n  +makeSound()\n}\nclass Dog {\n  +String breed\n  +bark()\n}\nAnimal <|-- Dog\n@enduml",
                "sequence": '@startuml\nactor User\nparticipant "Web Browser" as Browser\nparticipant "Web Server" as Server\nparticipant Database\n\nUser -> Browser: Enter URL\nBrowser -> Server: HTTP Request\nServer -> Database: Query Data\nDatabase -> Server: Return Data\nServer -> Browser: HTTP Response\nBrowser -> User: Display Page\n@enduml',
                "usecase": '@startuml\nactor Customer\nactor Admin\n\nrectangle "E-commerce System" {\n  Customer -- (Browse Products)\n  Customer -- (Add to Cart)\n  Customer -- (Checkout)\n  Admin -- (Manage Products)\n  Admin -- (View Orders)\n}\n@enduml',
            },
            "graphviz": {
                "simple": "digraph G {\n    A -> B\n    B -> C\n    C -> D\n    D -> A\n}",
                "flowchart": 'digraph workflow {\n    rankdir=TD\n    node [shape=box, style=rounded]\n    \n    Start [shape=ellipse, style=filled, fillcolor=lightgreen]\n    Process [label="Process Data"]\n    Decision [shape=diamond, label="Valid?"]\n    Success [shape=ellipse, style=filled, fillcolor=lightblue, label="Success"]\n    Error [shape=ellipse, style=filled, fillcolor=lightcoral, label="Error"]\n    \n    Start -> Process\n    Process -> Decision\n    Decision -> Success [label="Yes"]\n    Decision -> Error [label="No"]\n}',
                "network": 'graph network {\n    layout=circo\n    node [shape=circle, style=filled]\n    \n    Server [fillcolor=lightblue]\n    DB [fillcolor=lightgreen, label="Database"]\n    API [fillcolor=lightyellow]\n    Client1 [fillcolor=lightcoral, label="Client 1"]\n    Client2 [fillcolor=lightcoral, label="Client 2"]\n    \n    Server -- DB\n    Server -- API\n    API -- Client1\n    API -- Client2\n}',
            },
        }
        return json.dumps(examples, indent=2)

    elif uri == "diagram://supported-types":
        types_info = {
            "supported_types": ["mermaid", "plantuml", "graphviz"],
            "auto_detection": True,
            "mermaid": {
                "description": "Modern diagram and flowchart tool",
                "types": [
                    "flowchart",
                    "sequence",
                    "class",
                    "state",
                    "er",
                    "user-journey",
                    "gantt",
                    "pie",
                ],
                "syntax_url": "https://mermaid.js.org/intro/",
            },
            "plantuml": {
                "description": "UML diagrams with simple text language",
                "types": ["class", "sequence", "usecase", "activity", "component", "deployment"],
                "syntax_url": "https://plantuml.com/",
            },
            "graphviz": {
                "description": "Graph visualization software using DOT language",
                "types": ["directed graphs", "undirected graphs", "network diagrams"],
                "syntax_url": "https://graphviz.org/doc/info/lang.html",
            },
        }
        return json.dumps(types_info, indent=2)

    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="render_diagram",
            description="Render a diagram from Mermaid, PlantUML, or Graphviz code to interactive HTML",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The diagram code (Mermaid, PlantUML, or Graphviz syntax)",
                    },
                    "diagram_type": {
                        "type": "string",
                        "enum": ["auto", "mermaid", "plantuml", "graphviz"],
                        "description": "Diagram type (auto-detect if not specified)",
                        "default": "auto",
                    },
                    "save_to_file": {
                        "type": "boolean",
                        "description": "Whether to save the HTML to a temporary file",
                        "default": False,
                    },
                    "include_controls": {
                        "type": "boolean",
                        "description": "Whether to include interactive zoom/pan controls",
                        "default": True,
                    },
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="detect_diagram_type",
            description="Detect the type of diagram from source code",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The diagram code to analyze"}
                },
                "required": ["code"],
            },
        ),
        Tool(
            name="validate_diagram",
            description="Validate diagram syntax and check for potential issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The diagram code to validate"},
                    "diagram_type": {
                        "type": "string",
                        "enum": ["auto", "mermaid", "plantuml", "graphviz"],
                        "description": "Diagram type (auto-detect if not specified)",
                        "default": "auto",
                    },
                },
                "required": ["code"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Handle tool calls"""
    if arguments is None:
        arguments = {}

    try:
        if name == "render_diagram":
            return await render_diagram_tool(arguments)
        elif name == "detect_diagram_type":
            return await detect_diagram_type_tool(arguments)
        elif name == "validate_diagram":
            return await validate_diagram_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def render_diagram_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Render a diagram to interactive HTML"""
    code = arguments.get("code", "").strip()
    diagram_type = arguments.get("diagram_type", "auto")
    save_to_file = arguments.get("save_to_file", False)
    include_controls = arguments.get("include_controls", True)

    if not code:
        return [TextContent(type="text", text="Error: No diagram code provided")]

    try:
        # Render the diagram
        if diagram_type == "auto":
            detected_type = renderer.detect_diagram_type(code)
            html_content = renderer.render_diagram_auto(code)
        else:
            detected_type = diagram_type
            html_content = renderer.render_diagram_auto(code)

        if not html_content:
            return [TextContent(type="text", text="Error: Failed to render diagram")]

        # Optionally save to file
        file_path = None
        if save_to_file:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
                f.write(html_content)
                file_path = f.name

        # Prepare response
        result_parts = []

        # Add summary
        summary = f"✅ Successfully rendered {detected_type or 'diagram'} ({len(code)} chars → {len(html_content)} chars HTML)"
        if file_path:
            summary += f"\n📁 Saved to: {file_path}"

        result_parts.append(TextContent(type="text", text=summary))

        # Add HTML content (truncated for display)
        if len(html_content) > 2000:
            preview = html_content[:1000] + "\n\n... [truncated] ...\n\n" + html_content[-1000:]
            result_parts.append(
                TextContent(type="text", text=f"HTML Preview (truncated):\n```html\n{preview}\n```")
            )
        else:
            result_parts.append(
                TextContent(type="text", text=f"Full HTML:\n```html\n{html_content}\n```")
            )

        # Add usage instructions
        instructions = """
Usage Instructions:
• Save the HTML to a file (e.g., diagram.html) and open in a browser
• Interactive controls: zoom (+/-), pan (arrow keys), reset (↻)
• Download PNG: click the 🖼 button
• Copy source code: click the ⧉ button
• GitHub-style controls included for optimal user experience
        """.strip()

        result_parts.append(TextContent(type="text", text=instructions))

        return result_parts

    except Exception as e:
        return [TextContent(type="text", text=f"Error rendering diagram: {str(e)}")]


async def detect_diagram_type_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Detect diagram type from source code"""
    code = arguments.get("code", "").strip()

    if not code:
        return [TextContent(type="text", text="Error: No diagram code provided")]

    try:
        detected_type = renderer.detect_diagram_type(code)

        if detected_type:
            result = f"🎯 Detected diagram type: **{detected_type.upper()}**\n\n"

            # Add specific info about the detected type
            if detected_type == "mermaid":
                result += "Mermaid diagrams support flowcharts, sequence diagrams, class diagrams, and more."
            elif detected_type == "plantuml":
                result += "PlantUML diagrams support UML diagrams, network diagrams, and mind maps."
            elif detected_type == "graphviz":
                result += "Graphviz diagrams use DOT language for directed and undirected graphs."

        else:
            result = "❓ Could not detect diagram type.\n\n"
            result += "The code will be rendered as Mermaid (default fallback).\n"
            result += "Consider adding explicit markers like `@startuml` for PlantUML or `digraph` for Graphviz."

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error detecting diagram type: {str(e)}")]


async def validate_diagram_tool(arguments: dict[str, Any]) -> list[TextContent]:
    """Validate diagram syntax"""
    code = arguments.get("code", "").strip()
    diagram_type = arguments.get("diagram_type", "auto")

    if not code:
        return [TextContent(type="text", text="Error: No diagram code provided")]

    try:
        # Detect type if auto
        if diagram_type == "auto":
            detected_type = renderer.detect_diagram_type(code)
        else:
            detected_type = diagram_type

        # Basic validation checks
        issues = []
        warnings = []

        # Check for common issues
        if len(code.strip()) < 10:
            warnings.append("Diagram code is very short")

        if len(code) > 10000:
            warnings.append("Diagram code is very long (may affect performance)")

        # Type-specific validation
        if detected_type == "plantuml":
            if not code.strip().startswith("@start") and "@start" not in code:
                warnings.append("PlantUML diagrams typically start with @startuml")
            if not code.strip().endswith("@end") and "@end" not in code:
                warnings.append("PlantUML diagrams typically end with @enduml")

        elif detected_type == "graphviz":
            if "digraph" not in code and "graph" not in code:
                warnings.append("Graphviz diagrams typically start with 'digraph' or 'graph'")

        elif detected_type == "mermaid":
            if code.count("{") != code.count("}"):
                issues.append("Mismatched braces { } in Mermaid diagram")

        # Try to render to validate
        try:
            html_result = renderer.render_diagram_auto(code)
            if not html_result:
                issues.append("Diagram failed to render")
            elif len(html_result) < 1000:
                warnings.append("Rendered output is unusually small")
        except Exception as render_error:
            issues.append(f"Rendering failed: {str(render_error)}")

        # Prepare result
        result = f"📋 Validation Results for {detected_type or 'unknown'} diagram:\n\n"

        if not issues and not warnings:
            result += "✅ No issues found! Diagram appears valid.\n"
        else:
            if issues:
                result += "❌ **Issues found:**\n"
                for issue in issues:
                    result += f"  • {issue}\n"
                result += "\n"

            if warnings:
                result += "⚠️ **Warnings:**\n"
                for warning in warnings:
                    result += f"  • {warning}\n"
                result += "\n"

        result += "📊 **Stats:**\n"
        result += f"  • Length: {len(code)} characters\n"
        result += f"  • Lines: {len(code.splitlines())}\n"
        result += f"  • Type: {detected_type or 'auto-detected as Mermaid'}\n"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error validating diagram: {str(e)}")]


async def main():
    """Run the MCP server"""
    # Import here to avoid import errors in non-async context
    from mcp.server.stdio import stdio_server

    logger.info("Starting Diagram Renderer MCP Server")
    logger.info("Capabilities: Mermaid, PlantUML, Graphviz rendering")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="diagram-renderer",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

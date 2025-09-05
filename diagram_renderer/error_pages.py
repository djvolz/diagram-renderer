"""
Shared error HTML generation utilities for diagram renderers.

This module provides consistent error page generation across all renderer types.
"""

from typing import Any


def generate_unsupported_diagram_error_html(
    missing_plugins: list[dict[str, Any]], original_code: str
) -> str:
    """Generate user-friendly error HTML for missing external plugins"""
    plugin_list = []
    for plugin in missing_plugins:
        plugin_list.append(f"• {plugin['description']}")
        plugin_list.append(f"  Required file: static/js/{plugin['plugin_needed']}")

    plugins_text = "\\n".join(plugin_list)

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Renderer - Unsupported Diagram Type</title>
    <meta name="diagram-render-status" content="error">
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
        .error-icon {{
            font-size: 48px;
            color: #f85149;
            margin-bottom: 16px;
        }}
        h1 {{
            color: #f85149;
            margin: 0 0 16px 0;
            font-size: 24px;
        }}
        .code-block {{
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 14px;
            overflow-x: auto;
        }}
        .requirements {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
        }}
        .requirements h3 {{
            margin-top: 0;
            color: #b45309;
        }}
        .requirements pre {{
            background: none;
            border: none;
            padding: 0;
            margin: 8px 0;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <h1>Unsupported Diagram Type</h1>
        <p>This diagram uses external Mermaid features that require additional plugins:</p>

        <div class="requirements">
            <h3>Missing Requirements:</h3>
            <pre>{plugins_text}</pre>
        </div>

        <p><strong>Original diagram code:</strong></p>
        <div class="code-block">{original_code}</div>

        <p><strong>How to fix:</strong></p>
        <ol>
            <li>Download the required plugin files and place them in your <code>static/js/</code> directory</li>
            <li>Ensure the diagram renderer can bundle these plugins with the main Mermaid library</li>
            <li>Alternatively, use a supported diagram type instead</li>
        </ol>

        <p><em>Note: This project requires all JavaScript dependencies to be bundled locally (no CDN dependencies).</em></p>
    </div>
</body>
</html>"""


def generate_no_diagram_detected_error_html(original_code: str) -> str:
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


def generate_rendering_error_html(original_code: str, error_message: str) -> str:
    """Generate user-friendly HTML when rendering fails with an exception"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Renderer - Rendering Error</title>
    <meta name="diagram-render-status" content="error">
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


def generate_simple_error_html(error_message: str) -> str:
    """Generate consistent simple error HTML for basic failures"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Renderer - Error</title>
    <meta name="diagram-render-status" content="error">
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
            text-align: center;
        }}
        .error-icon {{ font-size: 48px; color: #f85149; margin-bottom: 16px; }}
        h1 {{ color: #f85149; margin: 0 0 16px 0; font-size: 24px; }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">❌</div>
        <h1>Error</h1>
        <p>{error_message}</p>
    </div>
</body>
</html>"""

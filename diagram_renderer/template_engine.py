"""
Template engine for generating HTML with consistent styling and structure.

This module provides a centralized template system to eliminate code duplication
and ensure consistent HTML generation across all renderer types.
"""

import html
from typing import Any, Optional


class TemplateEngine:
    """Handles HTML template generation with consistent styling and security."""

    # Common CSS styles used across all error and rendered pages
    BASE_STYLES = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            background-color: #f8f9fa;
            color: #24292e;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        h1 {
            margin: 0 0 16px 0;
            font-size: 24px;
            font-weight: 600;
        }
        h2 {
            margin: 24px 0 12px 0;
            font-size: 18px;
            font-weight: 600;
            color: #586069;
        }
        .icon {
            font-size: 48px;
            margin-bottom: 16px;
        }
        .error-icon { color: #f85149; }
        .warning-icon { color: #f0ad4e; }
        .success-icon { color: #28a745; }
        .error-title { color: #f85149; }
        .warning-title { color: #f0ad4e; }
        .code-block {
            background: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 16px;
            margin: 16px 0;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 13px;
            line-height: 1.45;
            overflow-x: auto;
        }
        .message {
            line-height: 1.6;
            color: #586069;
        }
        ul {
            margin: 16px 0;
            padding-left: 24px;
        }
        li {
            margin: 8px 0;
            line-height: 1.6;
        }
        .help-section {
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #e1e4e8;
        }
    """

    @classmethod
    def generate_html(
        cls,
        title: str,
        icon: str,
        icon_type: str,
        heading: str,
        content: str,
        original_code: Optional[str] = None,
        additional_styles: str = "",
        meta_status: str = "error",
        show_help: bool = True,
    ) -> str:
        """
        Generate a complete HTML page with consistent structure and styling.

        Args:
            title: Page title for browser tab
            icon: Icon symbol to display (e.g., "⚠", "✗", "✓")
            icon_type: Type of icon for styling ("error", "warning", "success")
            heading: Main heading text
            content: Main content HTML (will be escaped if needed)
            original_code: Optional code block to display (will be escaped)
            additional_styles: Additional CSS to include
            meta_status: Status for meta tag (error, warning, success)
            show_help: Whether to show help section

        Returns:
            Complete HTML page as string
        """
        # Escape content to prevent XSS
        heading_safe = html.escape(heading)

        # Build code block if provided
        code_section = ""
        if original_code:
            code_safe = html.escape(original_code)
            code_section = f"""
        <div class="code-block">
            <pre>{code_safe}</pre>
        </div>"""

        # Build help section if requested
        help_section = ""
        if show_help:
            help_section = """
        <div class="help-section">
            <h2>Need Help?</h2>
            <p>Check the documentation at <a href="https://github.com/dannyl1u/diagram-render">github.com/dannyl1u/diagram-render</a></p>
        </div>"""

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{html.escape(title)}</title>
    <meta name="diagram-render-status" content="{html.escape(meta_status)}">
    <style>
        {cls.BASE_STYLES}
        {additional_styles}
    </style>
</head>
<body>
    <div class="container">
        <div class="{icon_type}-icon icon">{icon}</div>
        <h1 class="{icon_type}-title">{heading_safe}</h1>
        <div class="message">
            {content}
        </div>
        {code_section}
        {help_section}
    </div>
</body>
</html>"""

    @classmethod
    def generate_error_html(
        cls,
        error_type: str,
        error_message: str,
        original_code: Optional[str] = None,
        suggestions: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate an error page with consistent formatting.

        Args:
            error_type: Type of error (e.g., "Unsupported Diagram Type")
            error_message: Detailed error message
            original_code: The code that caused the error
            suggestions: List of suggestions for fixing the error
            **kwargs: Additional arguments passed to generate_html

        Returns:
            Complete error HTML page
        """
        # Build content with suggestions if provided
        content = f"<p>{html.escape(error_message)}</p>"

        if suggestions:
            content += "\n<h2>Suggestions:</h2>\n<ul>"
            for suggestion in suggestions:
                content += f"\n    <li>{html.escape(suggestion)}</li>"
            content += "\n</ul>"

        return cls.generate_html(
            title=f"Diagram Renderer - {error_type}",
            icon="✗",
            icon_type="error",
            heading=error_type,
            content=content,
            original_code=original_code,
            meta_status="error",
            **kwargs,
        )

    @classmethod
    def escape_for_javascript(cls, text: str) -> str:
        """
        Safely escape text for inclusion in JavaScript strings.

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for JavaScript
        """
        # First HTML escape, then handle JavaScript special characters
        text = html.escape(text)
        return (
            text.replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )

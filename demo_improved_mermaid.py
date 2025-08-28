#!/usr/bin/env python3
"""Demo script showing the improved Mermaid renderer"""

import tempfile
import webbrowser

from diagram_renderer import DiagramRenderer


def create_demo():
    """Create and open a demo of the improved Mermaid renderer"""

    # Sample Mermaid diagram
    mermaid_code = """
    graph TD
        A[🚀 Improved Mermaid Renderer] --> B{What's New?}
        B --> C[🎨 Modern UI Design]
        B --> D[🌓 Theme Toggle]
        B --> E[📱 Better Controls]
        B --> F[💾 Enhanced Downloads]

        C --> C1[Cleaner Styling]
        C --> C2[Better Tooltips]

        D --> D1[Auto Detection]
        D --> D2[Light/Dark Themes]

        E --> E1[Panzoom Library]
        E --> E2[Mouse Wheel Zoom]
        E --> E3[Keyboard Shortcuts]

        F --> F1[PNG Export]
        F --> F2[SVG Export]
        F --> F3[Source Copy]

        style A fill:#e1f5fe
        style B fill:#f3e5f5
        style C fill:#e8f5e8
        style D fill:#fff3e0
        style E fill:#fce4ec
        style F fill:#f1f8e9
    """

    renderer = DiagramRenderer()

    # Generate the improved HTML
    html_result = renderer.render_diagram_auto(mermaid_code)

    # Create temporary file and open in browser
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_result)
        temp_path = f.name

    print("🎉 Demo created! Opening in browser...")
    print(f"📄 File: {temp_path}")
    print("\n✨ Key improvements:")
    print("   🎨 Modern UI with better styling")
    print("   🌓 Theme toggle (auto/light/dark)")
    print("   🖱️  Enhanced pan/zoom with panzoom library")
    print("   💾 Multiple download formats (PNG, SVG, source)")
    print("   📋 Copy to clipboard functionality")
    print("   🎯 Better error handling and loading states")
    print("   ♿ Improved accessibility with tooltips")
    print("   📱 Responsive design")
    print("   ⚡ All static and offline-capable!")

    # Open in browser
    webbrowser.open(f"file://{temp_path}")

    return temp_path


if __name__ == "__main__":
    demo_path = create_demo()
    print(f"\n🔍 You can also manually open: {demo_path}")
    print("🧹 Remember to delete the temp file when done!")

#!/usr/bin/env python3
"""Generate demo HTML with external JS references for README display"""

from diagram_renderer import MermaidRenderer

def generate_external_demo():
    """Generate a demo diagram using external JS references"""
    renderer = MermaidRenderer()
    
    # Create a sample flowchart diagram
    demo_diagram = """flowchart LR
    A[diagram-renderer] --> B{Auto-detect}
    B -->|Mermaid| C[Mermaid.js]
    B -->|PlantUML| D[PlantUML → DOT]
    B -->|Graphviz| E[VizJS]
    C --> F[Interactive HTML]
    D --> F
    E --> F
    F --> G[📱 Responsive]
    F --> H[🖼️ PNG Export]
    F --> I[🔍 Zoom/Pan]"""
    
    # Render using external script reference
    html_output = renderer.render_html_external(demo_diagram)
    
    if html_output:
        # Save to file
        with open('demo_external.html', 'w') as f:
            f.write(html_output)
        print("External demo HTML generated successfully!")
        print("File size is much smaller - no embedded JavaScript!")
        print("View at: demo_external.html")
        return html_output
    else:
        print("Failed to generate external demo")
        return None

if __name__ == "__main__":
    generate_external_demo()
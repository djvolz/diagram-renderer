#!/usr/bin/env python3
"""Generate demo HTML for README display"""

from diagram_renderer import DiagramRenderer

def generate_demo():
    """Generate a demo diagram and save as HTML"""
    renderer = DiagramRenderer()
    
    # Create a sample flowchart diagram
    demo_diagram = """
flowchart LR
    A[diagram-renderer] --> B{Auto-detect}
    B -->|Mermaid| C[Mermaid.js]
    B -->|PlantUML| D[PlantUML → DOT]
    B -->|Graphviz| E[VizJS]
    C --> F[Interactive HTML]
    D --> F
    E --> F
    F --> G[📱 Responsive]
    F --> H[🖼️ PNG Export]
    F --> I[🔍 Zoom/Pan]
    """
    
    # Render the diagram
    html_output = renderer.render_diagram_auto(demo_diagram)
    
    if html_output:
        # Save to file
        with open('demo_output.html', 'w') as f:
            f.write(html_output)
        print("Demo HTML generated successfully!")
        print("View at: demo_output.html")
        return html_output
    else:
        print("Failed to generate demo")
        return None

if __name__ == "__main__":
    generate_demo()
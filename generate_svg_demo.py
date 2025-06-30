#!/usr/bin/env python3
"""Generate demo SVG for README display"""

from diagram_renderer import DiagramRenderer
import re

def generate_svg_demo():
    """Generate a demo diagram and extract SVG for README"""
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
        # Extract SVG from HTML
        svg_match = re.search(r'<svg[^>]*>.*?</svg>', html_output, re.DOTALL)
        if svg_match:
            svg_content = svg_match.group(0)
            
            # Save SVG to file
            with open('demo.svg', 'w') as f:
                f.write(svg_content)
            
            print("Demo SVG generated successfully!")
            print("SVG saved to: demo.svg")
            return svg_content
        else:
            print("Could not extract SVG from HTML")
            return None
    else:
        print("Failed to generate demo")
        return None

if __name__ == "__main__":
    generate_svg_demo()
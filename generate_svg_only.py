#!/usr/bin/env python3
"""Generate SVG only from Mermaid diagram by opening in browser and extracting"""

from diagram_renderer import MermaidRenderer
import tempfile
import os
import time

def generate_svg():
    """Generate SVG by creating a minimal HTML page and extracting the SVG"""
    renderer = MermaidRenderer()
    
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
    
    # Create a minimal HTML page that will render and expose the SVG
    mermaid_js_content = renderer.get_static_js_content("mermaid.min.js")
    
    minimal_html = f"""<!DOCTYPE html>
<html>
<head>
    <script>{mermaid_js_content}</script>
</head>
<body>
    <div id="diagram" class="mermaid">
{demo_diagram}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: false,
            theme: 'default',
            securityLevel: 'loose'
        }});
        
        window.addEventListener('load', async function() {{
            try {{
                const element = document.getElementById('diagram');
                const {{svg}} = await mermaid.render('demo-svg', element.textContent);
                
                // Create a clean SVG without extra HTML
                const svgElement = new DOMParser().parseFromString(svg, 'image/svg+xml').documentElement;
                
                // Add some basic styling for better GitHub rendering
                svgElement.setAttribute('style', 'max-width: 100%; height: auto;');
                
                // Replace the content with just the SVG
                document.body.innerHTML = svgElement.outerHTML;
                
                // Also log it to console for extraction
                console.log('SVG_START');
                console.log(svgElement.outerHTML);
                console.log('SVG_END');
            }} catch (error) {{
                console.error('Error rendering SVG:', error);
                document.body.innerHTML = '<p>Error rendering diagram: ' + error.message + '</p>';
            }}
        }});
    </script>
</body>
</html>"""
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(minimal_html)
        temp_file = f.name
    
    print(f"Created temporary HTML file: {temp_file}")
    print("Open this file in a browser, then:")
    print("1. Open browser developer tools (F12)")
    print("2. Go to Console tab") 
    print("3. Look for the SVG content between SVG_START and SVG_END")
    print("4. Copy that SVG content and save it as demo.svg")
    
    return temp_file

if __name__ == "__main__":
    temp_file = generate_svg()
    print(f"\nTemporary file created: {temp_file}")
    print("Remember to delete it when done!")
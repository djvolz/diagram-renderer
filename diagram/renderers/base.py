from pathlib import Path
from abc import ABC, abstractmethod
import json
import re


class BaseRenderer(ABC):
    """Base class for diagram renderers"""
    
    def __init__(self):
        # Get static directory relative to this module
        module_dir = Path(__file__).parent  # diagram/renderers
        self.static_dir = module_dir / "static"
        self.use_local_rendering = True
    
    @abstractmethod
    def render_html(self, code, **kwargs):
        """Render diagram as HTML"""
        pass
    
    @abstractmethod
    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        pass
    
    def detect_diagram_type(self, code):
        """Detect if code matches this renderer type"""
        # To be implemented by subclasses
        return False
    
    def get_static_js_content(self, filename):
        """Get JavaScript content from static file"""
        js_file = self.static_dir / "js" / filename
        if js_file.exists():
            with open(js_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    

    def _render_vizjs_html(self, dot_code, original_code=None):
        """Generate HTML with VizJS to render DOT notation as SVG"""
        # Use JSON.stringify equivalent escaping to safely embed DOT code
        escaped_dot = json.dumps(dot_code)
        
        # If no original code provided, use the dot code
        if original_code is None:
            original_code = dot_code
        escaped_original = json.dumps(original_code)
        
        # Get VizJS content from local file
        viz_js_content = self.get_static_js_content("viz-lite.js") + "\n" + self.get_static_js_content("viz-full.js")
        if not viz_js_content:
            return f'<div class="error">VizJS not available. DOT code:<br><pre>{dot_code}</pre></div>'
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: white;
            height: 100vh;
            width: 100%;
            min-height: 500px;
            overflow: hidden;
            position: relative;
        }}
        .diagram-container {{
            position: relative;
            width: 100%;
            height: 100%;
            overflow: hidden;
            cursor: grab;
        }}
        .diagram-container:active {{
            cursor: grabbing;
        }}
        .zoom-controls {{
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .zoom-btn {{
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            width: 32px;
            height: 32px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .zoom-btn:hover {{
            background: #0056b3;
        }}
        .zoom-level {{
            font-size: 11px;
            text-align: center;
            color: #666;
            margin: 2px 0;
        }}
        #graph {{
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            transform-origin: center center;
            transition: transform 0.1s ease;
        }}
        #graph svg {{
            max-width: 100%;
            max-height: 100%;
            height: auto;
        }}
        #graph svg text {{
            font-family: Arial, Helvetica, sans-serif !important;
            font-style: normal !important;
            font-weight: normal !important;
        }}
        .error {{
            color: red;
            padding: 20px;
            border: 1px solid red;
            background-color: #ffe6e6;
            border-radius: 4px;
        }}
        .loading {{
            color: #666;
            font-style: italic;
        }}
    </style>
    <script>
{viz_js_content}
    </script>
</head>
<body>
    <div class="diagram-container">
        <div class="zoom-controls">
            <button class="zoom-btn" onclick="zoomIn()">+</button>
            <div class="zoom-level" id="zoom-level">100%</div>
            <button class="zoom-btn" onclick="zoomOut()">−</button>
            <button class="zoom-btn" onclick="resetZoom()" title="Reset">⌂</button>
            <button class="zoom-btn" onclick="downloadPNG()" title="Download PNG">📥</button>
            <button class="zoom-btn" onclick="downloadCode()" title="Download Source Code">📄</button>
        </div>
        <div id="graph" class="loading">Rendering diagram...</div>
    </div>
    
    <script>
        const dotString = {escaped_dot};
        const graphDiv = document.getElementById('graph');
        const zoomLevelDisplay = document.getElementById('zoom-level');
        
        let currentZoom = 1.0;
        let currentPanX = 0;
        let currentPanY = 0;
        let isDragging = false;
        let lastMouseX = 0;
        let lastMouseY = 0;
        
        function updateTransform() {{
            graphDiv.style.transform = `translate(${{currentPanX}}px, ${{currentPanY}}px) scale(${{currentZoom}})`;
            zoomLevelDisplay.textContent = Math.round(currentZoom * 100) + '%';
        }}
        
        function zoomIn() {{
            currentZoom = Math.min(currentZoom * 1.2, 3.0);
            updateTransform();
        }}
        
        function zoomOut() {{
            currentZoom = Math.max(currentZoom / 1.2, 0.1);
            updateTransform();
        }}
        
        function resetZoom() {{
            currentZoom = 1.0;
            currentPanX = 0;
            currentPanY = 0;
            updateTransform();
        }}
        
        function downloadPNG() {{
            const svgElement = graphDiv.querySelector('svg');
            if (!svgElement) {{
                alert('No diagram to download');
                return;
            }}
            
            // Clone the SVG to avoid modifying the original
            const svgClone = svgElement.cloneNode(true);
            
            // Get SVG dimensions
            const bbox = svgElement.getBBox();
            const width = bbox.width || svgElement.clientWidth || 800;
            const height = bbox.height || svgElement.clientHeight || 600;
            
            // Set explicit dimensions on the clone
            svgClone.setAttribute('width', width);
            svgClone.setAttribute('height', height);
            svgClone.setAttribute('viewBox', `${{bbox.x}} ${{bbox.y}} ${{width}} ${{height}}`);
            
            // Create a canvas
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = width * 2; // 2x for better quality
            canvas.height = height * 2;
            ctx.scale(2, 2);
            
            // Convert SVG to data URL (avoids CORS issues with blob URLs)
            let svgData = new XMLSerializer().serializeToString(svgClone);
            
            // Ensure SVG has proper namespace
            if (!svgData.includes('xmlns="http://www.w3.org/2000/svg"')) {{
                svgData = svgData.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
            }}
            
            // Use data URL instead of blob URL to avoid CORS issues
            const dataUrl = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
            
            // Create image and draw to canvas
            const img = new Image();
            img.onload = function() {{
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, width, height);
                ctx.drawImage(img, 0, 0, width, height);
                
                // Download the PNG using toDataURL (avoids tainted canvas issues)
                try {{
                    const pngDataUrl = canvas.toDataURL('image/png');
                    const link = document.createElement('a');
                    link.download = 'diagram.png';
                    link.href = pngDataUrl;
                    link.click();
                }} catch (error) {{
                    console.error('Failed to create PNG:', error);
                    alert('Failed to create PNG. Security restrictions may prevent export.');
                }}
            }};
            img.onerror = function() {{
                alert('Failed to generate PNG. Please try again.');
            }};
            img.src = dataUrl;
        }}
        
        function downloadCode() {{
            const originalCode = {escaped_original};
            const blob = new Blob([originalCode], {{ type: 'text/plain' }});
            const link = document.createElement('a');
            link.download = 'diagram-source.txt';
            link.href = URL.createObjectURL(blob);
            link.click();
            URL.revokeObjectURL(link.href);
        }}
        
        
        // Mouse drag pan
        graphDiv.addEventListener('mousedown', function(e) {{
            isDragging = true;
            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
            e.preventDefault();
        }});
        
        document.addEventListener('mousemove', function(e) {{
            if (isDragging) {{
                const deltaX = e.clientX - lastMouseX;
                const deltaY = e.clientY - lastMouseY;
                currentPanX += deltaX;
                currentPanY += deltaY;
                lastMouseX = e.clientX;
                lastMouseY = e.clientY;
                updateTransform();
            }}
        }});
        
        document.addEventListener('mouseup', function() {{
            isDragging = false;
        }});
        
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                if (typeof Viz !== 'undefined') {{
                    const viz = new Viz();
                    viz.renderSVGElement(dotString).then(function(svgElement) {{
                        graphDiv.innerHTML = '';
                        graphDiv.appendChild(svgElement);
                        updateTransform();
                    }}).catch(function(error) {{
                        console.error('VizJS render error:', error);
                        graphDiv.innerHTML = '<div class="error">VizJS Render Error: ' + error.message + '</div>';
                    }});
                }} else {{
                    graphDiv.innerHTML = '<div class="error">VizJS not available.</div>';
                }}
            }} catch (error) {{
                console.error('Script error:', error);
                graphDiv.innerHTML = '<div class="error">Script Error: ' + error.message + '</div>';
            }}
        }});
    </script>
</body>
</html>
"""
        return html_template
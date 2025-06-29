from .base import BaseRenderer


class MermaidRenderer(BaseRenderer):
    """Renderer for Mermaid diagrams"""
    
    def __init__(self):
        super().__init__()
        self.js_filename = "mermaid.min.js"
    
    def detect_diagram_type(self, code):
        """Detect if code is Mermaid"""
        code = code.strip().lower()
        
        # Strong Mermaid indicators (definitive)
        strong_mermaid_indicators = [
            "graph ", "flowchart ", "sequencediagram", "classdiagram",
            "statediagram", "erdiagram", "journey", "gantt", "pie ",
            "gitgraph", "requirement", "mindmap"
        ]
        
        # Check for strong indicators
        for indicator in strong_mermaid_indicators:
            if indicator in code:
                return True
        
        # Weak indicators - check context for participant/actor usage
        if "participant " in code or "actor " in code:
            # Check if it looks like Mermaid sequence diagram
            if ("sequencediagram" in code or 
                "-->" in code or "->>" in code or 
                ("participant " in code and ("as " in code or ":" in code))):
                return True
        
        return False
    
    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        return code.strip()
    
    def render_html(self, code, **kwargs):
        """Generate HTML with embedded Mermaid.js"""
        mermaid_js_content = self.get_static_js_content(self.js_filename)
        
        if not mermaid_js_content:
            return "<div>Error: Mermaid.js not available</div>"
        
        # Clean mermaid code
        clean_code = self.clean_code(code)
        
        # Escape original code for JavaScript
        import json
        escaped_original = json.dumps(code)
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: transparent;
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
        .zoom-btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
            opacity: 0.6;
        }}
        .zoom-btn:disabled:hover {{
            background: #ccc;
        }}
        .zoom-level {{
            font-size: 11px;
            text-align: center;
            color: #666;
            margin: 2px 0;
        }}
        .mermaid-container {{
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: visible;
            transform-origin: center center;
            transition: transform 0.1s ease;
        }}
        .mermaid {{
            width: auto;
            height: auto;
            text-align: center;
            overflow: visible;
        }}
        .mermaid svg {{
            max-width: 100%;
            max-height: 100%;
            height: auto;
        }}
    </style>
    <script>
{mermaid_js_content}
    </script>
</head>
<body>
    <div class="diagram-container">
        <div class="zoom-controls">
            <button class="zoom-btn" onclick="zoomIn()">+</button>
            <div class="zoom-level" id="zoom-level">100%</div>
            <button class="zoom-btn" onclick="zoomOut()">−</button>
            <button class="zoom-btn" onclick="resetZoom()" title="Reset">⌂</button>
            <button class="zoom-btn" id="download-btn" onclick="downloadPNG()" title="Loading diagram..." disabled>📥</button>
            <button class="zoom-btn" onclick="downloadCode()" title="Download Source Code">📄</button>
        </div>
        <div class="mermaid-container" id="mermaid-container">
            <div class="mermaid">
{clean_code}
            </div>
        </div>
    </div>
    <script>
        const mermaidContainer = document.getElementById('mermaid-container');
        const zoomLevelDisplay = document.getElementById('zoom-level');
        
        let currentZoom = 1.0;
        let currentPanX = 0;
        let currentPanY = 0;
        let isDragging = false;
        let lastMouseX = 0;
        let lastMouseY = 0;
        let diagramReady = false;
        
        function isSVGReady(svgElement) {{
            try {{
                const bbox = svgElement.getBBox();
                return bbox.width > 0 && bbox.height > 0;
            }} catch (e) {{
                return false;
            }}
        }}
        
        function waitForSVGReady(callback, maxAttempts = 20) {{
            let attempts = 0;
            const checkReady = () => {{
                const svgElement = mermaidContainer.querySelector('svg');
                if (svgElement && isSVGReady(svgElement)) {{
                    callback();
                }} else if (attempts < maxAttempts) {{
                    attempts++;
                    setTimeout(checkReady, 100);
                }} else {{
                    console.warn('SVG took longer than expected to become ready');
                    callback(); // Still enable download, but with warning
                }}
            }};
            checkReady();
        }}
        
        function updateTransform() {{
            mermaidContainer.style.transform = `translate(${{currentPanX}}px, ${{currentPanY}}px) scale(${{currentZoom}})`;
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
            if (!diagramReady) {{
                alert('Diagram is still loading. Please wait a moment and try again.');
                return;
            }}
            
            const svgElement = mermaidContainer.querySelector('svg');
            if (!svgElement) {{
                alert('No diagram to download');
                return;
            }}
            
            // Additional validation for SVG readiness
            if (!isSVGReady(svgElement)) {{
                alert('Diagram is still rendering. Please wait a moment and try again.');
                return;
            }}
            
            // Clone the SVG to avoid modifying the original
            const svgClone = svgElement.cloneNode(true);
            
            // Get SVG dimensions with retry logic
            let bbox, width, height;
            try {{
                bbox = svgElement.getBBox();
                width = bbox.width || svgElement.clientWidth || 800;
                height = bbox.height || svgElement.clientHeight || 600;
            }} catch (error) {{
                console.warn('getBBox failed, using fallback dimensions:', error);
                width = svgElement.clientWidth || svgElement.offsetWidth || 800;
                height = svgElement.clientHeight || svgElement.offsetHeight || 600;
                bbox = {{ x: 0, y: 0, width: width, height: height }};
            }}
            
            if (width <= 0 || height <= 0) {{
                alert('Unable to determine diagram dimensions. Please try again in a moment.');
                return;
            }}
            
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
            
            // Convert SVG to data URL with content cleaning
            let svgData = new XMLSerializer().serializeToString(svgClone);
            
            // Clean up any problematic SVG content that prevents PNG conversion
            // Remove foreign objects that contain HTML content
            svgData = svgData.replace(/<foreignObject[^>]*>.*?<\\/foreignObject>/gi, '');
            
            // Remove any remaining HTML elements that might be embedded
            svgData = svgData.replace(/<div[^>]*>.*?<\\/div>/gi, '');
            svgData = svgData.replace(/<span[^>]*>.*?<\\/span>/gi, '');
            svgData = svgData.replace(/<p[^>]*>.*?<\\/p>/gi, '');
            
            // Convert any remaining HTML entities that might cause issues
            svgData = svgData.replace(/&nbsp;/g, ' ');
            svgData = svgData.replace(/&amp;/g, '&');
            svgData = svgData.replace(/&lt;/g, '<');
            svgData = svgData.replace(/&gt;/g, '>');
            
            // Ensure SVG has proper namespace
            if (!svgData.includes('xmlns="http://www.w3.org/2000/svg"')) {{
                svgData = svgData.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
            }}
            
            console.log('SVG data prepared, length:', svgData.length);
            console.log('Full SVG content:', svgData);
            
            // Check for potentially problematic elements
            const hasForeignObject = svgData.includes('foreignObject');
            const hasHTMLContent = svgData.includes('<div') || svgData.includes('<span');
            const hasUndefinedDimensions = !bbox || bbox.width === 0 || bbox.height === 0;
            
            console.log('SVG analysis:', {{
                hasForeignObject: hasForeignObject,
                hasHTMLContent: hasHTMLContent,
                hasUndefinedDimensions: hasUndefinedDimensions,
                width: width,
                height: height
            }});
            
            // Use data URL instead of blob URL to avoid CORS issues
            const dataUrl = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
            
            // Create image and draw to canvas
            const img = new Image();
            img.onload = function() {{
                console.log('Image loaded successfully, dimensions:', img.width, 'x', img.height);
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, width, height);
                ctx.drawImage(img, 0, 0, width, height);
                
                // Download the PNG using toDataURL (avoids tainted canvas issues)
                try {{
                    const pngDataUrl = canvas.toDataURL('image/png');
                    console.log('PNG data URL created successfully, length:', pngDataUrl.length);
                    
                    const link = document.createElement('a');
                    link.download = 'mermaid-diagram.png';
                    link.href = pngDataUrl;
                    link.click();
                }} catch (error) {{
                    console.error('Failed to create PNG:', error);
                    alert('Failed to create PNG. Security restrictions may prevent export.');
                }}
            }};
            img.onerror = function(e) {{
                console.error('Image load error:', e);
                console.error('SVG data length:', svgData.length);
                alert('Failed to generate PNG. The SVG may contain unsupported elements.');
            }};
            console.log('Starting image load with data URL...');
            img.src = dataUrl;
        }}
        
        function downloadCode() {{
            const originalCode = {escaped_original};
            const blob = new Blob([originalCode], {{ type: 'text/plain' }});
            const link = document.createElement('a');
            link.download = 'mermaid-diagram.mmd';
            link.href = URL.createObjectURL(blob);
            link.click();
            URL.revokeObjectURL(link.href);
        }}
        
        
        // Mouse drag pan
        mermaidContainer.addEventListener('mousedown', function(e) {{
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
        
        // Initialize Mermaid with error handling
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                mermaid.initialize({{
                    startOnLoad: false,
                    theme: 'default',
                    securityLevel: 'loose',
                    fontFamily: 'Arial, sans-serif',
                    flowchart: {{
                        useMaxWidth: true,
                        htmlLabels: true
                    }},
                    sequence: {{
                        useMaxWidth: true
                    }},
                    gantt: {{
                        useMaxWidth: true
                    }}
                }});
                
                // Find all mermaid elements and render them
                const mermaidElements = document.querySelectorAll('.mermaid');
                let renderPromises = [];
                
                mermaidElements.forEach(async (element, index) => {{
                    const renderPromise = (async () => {{
                        try {{
                            const id = 'mermaid-' + index;
                            const {{svg}} = await mermaid.render(id, element.textContent);
                            element.innerHTML = svg;
                            updateTransform();
                        }} catch (error) {{
                            console.error('Mermaid rendering error:', error);
                            element.innerHTML = '<div style="color: red; padding: 20px; border: 1px solid red; background-color: #ffe6e6;">Error rendering diagram: ' + error.message + '</div>';
                        }}
                    }})();
                    renderPromises.push(renderPromise);
                }});
                
                // Wait for all diagrams to finish rendering
                Promise.all(renderPromises).then(() => {{
                    console.log('All Mermaid diagrams rendered, waiting for SVG layout...');
                    // Wait for SVG to be fully ready before enabling downloads
                    waitForSVGReady(() => {{
                        diagramReady = true;
                        const downloadBtn = document.getElementById('download-btn');
                        if (downloadBtn) {{
                            downloadBtn.disabled = false;
                            downloadBtn.title = 'Download PNG';
                        }}
                        console.log('Mermaid diagram fully ready for download');
                    }});
                }}).catch((error) => {{
                    console.error('Error during Mermaid rendering:', error);
                    // On error, still try to enable downloads after a delay
                    setTimeout(() => {{
                        diagramReady = true;
                        const downloadBtn = document.getElementById('download-btn');
                        if (downloadBtn) {{
                            downloadBtn.disabled = false;
                            downloadBtn.title = 'Download PNG (may have issues)';
                        }}
                    }}, 500);
                }});
            }} catch (error) {{
                console.error('Mermaid initialization error:', error);
                document.querySelector('.mermaid').innerHTML = '<div style="color: red; padding: 20px;">Failed to initialize Mermaid: ' + error.message + '</div>';
            }}
        }});
    </script>
</body>
</html>
"""
        return html_template
    
    
    def render_svg_html(self, code, theme="default"):
        """Generate minimal HTML that renders Mermaid to SVG for extraction"""
        mermaid_js_content = self.get_static_js_content(self.js_filename)
        
        if not mermaid_js_content:
            return "<div>Error: Mermaid.js not available</div>"
        
        # Clean mermaid code
        clean_code = self.clean_code(code)
        
        # Minimal HTML template for SVG extraction
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <script>
{mermaid_js_content}
    </script>
</head>
<body>
    <div id="mermaid-output"></div>
    <script>
        document.addEventListener('DOMContentLoaded', async function() {{
            try {{
                mermaid.initialize({{
                    startOnLoad: false,
                    theme: '{theme}',
                    securityLevel: 'loose'
                }});
                
                const {{svg}} = await mermaid.render('diagram', `{clean_code}`);
                document.getElementById('mermaid-output').innerHTML = svg;
                
                // For CLI extraction, we'll just show the SVG
                console.log('SVG_START');
                console.log(svg);
                console.log('SVG_END');
            }} catch (error) {{
                console.error('Mermaid rendering error:', error);
                document.getElementById('mermaid-output').innerHTML = '<div>Error: ' + error.message + '</div>';
            }}
        }});
    </script>
</body>
</html>
"""
        return html_template
#!/usr/bin/env python3
"""
Simple FastAPI web application demonstrating diagram-renderer REST API

This provides both a REST API and a web interface for rendering diagrams.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Literal
from io import BytesIO
import base64

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import HTMLResponse, Response
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("FastAPI dependencies not installed. Run: uv sync --extra webapp")
    exit(1)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from diagram_renderer import DiagramRenderer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Diagram Renderer API",
    description="REST API for rendering Mermaid, PlantUML, and Graphviz diagrams",
    version="1.0.0"
)

# Initialize the diagram renderer
renderer = DiagramRenderer()


class DiagramRequest(BaseModel):
    """Request model for diagram rendering"""
    code: str = Field(..., description="Diagram source code")
    type: Optional[Literal["auto", "mermaid", "plantuml", "graphviz"]] = Field(
        "auto", description="Diagram type (auto-detect if not specified)"
    )
    format: Literal["html"] = Field("html", description="Output format")
    theme: Optional[str] = Field("default", description="Theme for Mermaid diagrams")


class DiagramResponse(BaseModel):
    """Response model for successful diagram rendering"""
    success: bool
    diagram_type: str
    format: str
    content: Optional[str] = None  # HTML content or base64 PNG
    error: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Diagram Renderer</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f6f8fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            overflow: hidden;
        }
        .header {
            background: #24292e;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
            min-height: 600px;
        }
        .editor-panel, .preview-panel {
            display: flex;
            flex-direction: column;
        }
        .panel-header {
            font-weight: 600;
            margin-bottom: 10px;
            color: #24292e;
        }
        textarea {
            flex: 1;
            padding: 12px;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            font-family: 'SF Mono', Monaco, 'Consolas', monospace;
            font-size: 14px;
            resize: vertical;
            min-height: 300px;
        }
        .controls {
            margin: 10px 0;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        select, button {
            padding: 6px 12px;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            background: white;
            font-size: 14px;
        }
        button {
            background: #2da44e;
            color: white;
            border-color: #2da44e;
            cursor: pointer;
        }
        button:hover {
            background: #2c974b;
        }
        button:disabled {
            background: #94d3a2;
            cursor: not-allowed;
        }
        .preview-container {
            flex: 1;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            background: white;
            overflow: hidden;
            min-height: 400px;
        }
        .preview-iframe {
            width: 100%;
            height: 100%;
            border: none;
            min-height: 400px;
        }
        .status {
            padding: 8px 12px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 14px;
        }
        .status.success {
            background: #dafbe1;
            color: #1a7f37;
            border: 1px solid #acd2a8;
        }
        .status.error {
            background: #ffeef0;
            color: #cf222e;
            border: 1px solid #ffb3ba;
        }
        .examples {
            margin-top: 10px;
        }
        .example-btn {
            background: #f6f8fa;
            color: #24292e;
            border: 1px solid #d0d7de;
            margin-right: 5px;
            margin-bottom: 5px;
            font-size: 12px;
            padding: 4px 8px;
        }
        .example-btn:hover {
            background: #e1e7ef;
        }
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Diagram Renderer</h1>
            <p>Create beautiful diagrams with Mermaid, PlantUML, and Graphviz</p>
        </div>
        
        <div class="content">
            <div class="editor-panel">
                <div class="panel-header">📝 Diagram Editor</div>
                
                <div class="controls">
                    <select id="diagramType">
                        <option value="auto">Auto-detect</option>
                        <option value="mermaid">Mermaid</option>
                        <option value="plantuml">PlantUML</option>
                        <option value="graphviz">Graphviz</option>
                    </select>
                    <select id="outputFormat">
                        <option value="html">Interactive HTML</option>
                    </select>
                    <button id="renderBtn" onclick="renderDiagram()">🚀 Render</button>
                    <button id="downloadBtn" onclick="downloadResult()" disabled>📥 Download</button>
                </div>
                
                <textarea id="diagramCode" placeholder="Enter your diagram code here...">graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E</textarea>
                
                <div class="examples">
                    <strong>Examples:</strong><br>
                    <button class="example-btn" onclick="loadExample('mermaid-flow')">Mermaid Flow</button>
                    <button class="example-btn" onclick="loadExample('mermaid-sequence')">Mermaid Sequence</button>
                    <button class="example-btn" onclick="loadExample('plantuml-class')">PlantUML Class</button>
                    <button class="example-btn" onclick="loadExample('graphviz-network')">Graphviz Network</button>
                </div>
                
                <div id="status"></div>
            </div>
            
            <div class="preview-panel">
                <div class="panel-header">📊 Preview</div>
                <div class="preview-container">
                    <iframe id="previewFrame" class="preview-iframe" 
                            src="data:text/html,<div style='padding:20px;text-align:center;color:#666;'>Click 'Render' to preview your diagram</div>">
                    </iframe>
                </div>
            </div>
        </div>
    </div>

    <script>
        const examples = {
            'mermaid-flow': `graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E`,
            'mermaid-sequence': `sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob!
    B-->>A: Hello Alice!
    A->>B: How are you?
    B-->>A: I'm doing well, thanks!`,
            'plantuml-class': `@startuml
class Animal {
  +String name
  +int age
  +makeSound()
}
class Dog {
  +String breed
  +bark()
}
Animal <|-- Dog
@enduml`,
            'graphviz-network': `digraph network {
    rankdir=LR
    node [shape=circle, style=filled]
    
    Server [fillcolor=lightblue]
    DB [fillcolor=lightgreen, label="Database"]
    API [fillcolor=lightyellow]
    Client [fillcolor=lightcoral]
    
    Server -> DB
    Server -> API
    API -> Client
}`
        };

        let lastResult = null;

        function loadExample(exampleId) {
            document.getElementById('diagramCode').value = examples[exampleId];
            // Auto-select diagram type based on example
            const typeSelect = document.getElementById('diagramType');
            if (exampleId.startsWith('mermaid')) {
                typeSelect.value = 'mermaid';
            } else if (exampleId.startsWith('plantuml')) {
                typeSelect.value = 'plantuml';
            } else if (exampleId.startsWith('graphviz')) {
                typeSelect.value = 'graphviz';
            }
        }

        function showStatus(message, isError = false) {
            const status = document.getElementById('status');
            status.innerHTML = message;
            status.className = `status ${isError ? 'error' : 'success'}`;
            status.style.display = 'block';
        }

        function hideStatus() {
            document.getElementById('status').style.display = 'none';
        }

        async function renderDiagram() {
            const code = document.getElementById('diagramCode').value.trim();
            const type = document.getElementById('diagramType').value;
            
            if (!code) {
                showStatus('Please enter diagram code', true);
                return;
            }

            const renderBtn = document.getElementById('renderBtn');
            const downloadBtn = document.getElementById('downloadBtn');
            
            renderBtn.disabled = true;
            renderBtn.textContent = '⏳ Rendering...';
            downloadBtn.disabled = true;
            hideStatus();

            try {
                const response = await fetch('/api/render', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        type: type,
                        format: 'html'
                    })
                });

                const result = await response.json();
                lastResult = result;

                if (result.success) {
                    const iframe = document.getElementById('previewFrame');
                    const blob = new Blob([result.content], { type: 'text/html' });
                    const url = URL.createObjectURL(blob);
                    iframe.src = url;
                    
                    showStatus(`✅ ${result.diagram_type.toUpperCase()} diagram rendered successfully!`);
                    downloadBtn.disabled = false;
                } else {
                    showStatus(`❌ Error: ${result.error}`, true);
                    lastResult = null;
                }
            } catch (error) {
                showStatus(`❌ Network error: ${error.message}`, true);
                lastResult = null;
            } finally {
                renderBtn.disabled = false;
                renderBtn.textContent = '🚀 Render';
            }
        }

        function downloadResult() {
            if (!lastResult || !lastResult.success) {
                showStatus('No result to download', true);
                return;
            }

            const code = document.getElementById('diagramCode').value;
            
            // Generate filename
            const cleanCode = code.toLowerCase().replace(/[^a-z0-9\\s]/g, ' ').replace(/\\s+/g, ' ').trim();
            const words = cleanCode.split(' ').filter(word => word.length > 2).slice(0, 3);
            let filename = `${lastResult.diagram_type}-diagram`;
            if (words.length > 0) {
                filename = `${lastResult.diagram_type}-${words.join('-')}`;
            }

            const blob = new Blob([lastResult.content], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${filename}.html`;
            a.click();
            URL.revokeObjectURL(url);
        }

        // Auto-render on page load
        window.addEventListener('load', () => {
            renderDiagram();
        });
    </script>
</body>
</html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "diagram-renderer"}


@app.post("/api/render", response_model=DiagramResponse)
async def render_diagram(request: DiagramRequest):
    """
    Render a diagram from source code
    
    Returns HTML content or base64-encoded PNG based on format parameter
    """
    try:
        logger.info(f"Rendering diagram: type={request.type}, format={request.format}")
        
        # Detect diagram type if auto
        detected_type = request.type
        if request.type == "auto":
            detected_type = renderer.detect_diagram_type(request.code)
            if not detected_type:
                raise HTTPException(
                    status_code=400, 
                    detail="Could not auto-detect diagram type. Please specify type explicitly."
                )
        
        # Render based on format
        if request.format == "html":
            # Use the unified render_diagram_auto method
            html_content = renderer.render_diagram_auto(request.code)
            if not html_content:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to render {detected_type} diagram"
                )
            
            return DiagramResponse(
                success=True,
                diagram_type=detected_type,
                format="html",
                content=html_content
            )
            
            
    except Exception as e:
        logger.error(f"Error rendering diagram: {str(e)}")
        return DiagramResponse(
            success=False,
            diagram_type=detected_type or "unknown",
            format=request.format,
            error=str(e)
        )


@app.get("/api/examples")
async def get_examples():
    """Get example diagrams for each type"""
    return {
        "mermaid": {
            "flowchart": "graph TD\\n    A[Start] --> B{Decision}\\n    B -->|Yes| C[End]",
            "sequence": "sequenceDiagram\\n    Alice->>Bob: Hello\\n    Bob-->>Alice: Hi!"
        },
        "plantuml": {
            "class": "@startuml\\nclass Animal {\\n  +name: String\\n}\\n@enduml",
            "sequence": "@startuml\\nAlice -> Bob: Hello\\nBob --> Alice: Hi!\\n@enduml"
        },
        "graphviz": {
            "simple": "digraph G {\\n    A -> B\\n    B -> C\\n}",
            "network": "graph network {\\n    Server -- Database\\n    Server -- Client\\n}"
        }
    }


def main():
    """Run the web application"""
    print("🚀 Starting Diagram Renderer Web App...")
    print("📍 Web Interface: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("💡 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "webapp:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
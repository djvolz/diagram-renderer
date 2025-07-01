# Diagram Renderer Web App

A simple FastAPI web application that provides both a REST API and interactive web interface for rendering diagrams.

## Features

- **Interactive Web Interface** - Browser-based diagram editor with live preview
- **REST API** - Programmatic access for integrations
- **Multi-format Support** - Mermaid, PlantUML, and Graphviz diagrams
- **Auto-detection** - Automatically detects diagram type from source code
- **Export Options** - HTML with interactive controls or PNG images
- **Example Gallery** - Built-in examples for each diagram type

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync --extra webapp
   ```

2. **Run the web app:**
   ```bash
   uv run --extra webapp python examples/webapp.py
   ```

3. **Open in browser:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Web Interface

The web interface provides:

- **Split-pane editor** with syntax highlighting
- **Live preview** of rendered diagrams
- **Format selection** (Interactive HTML or PNG)
- **Example library** with common diagram patterns
- **Download functionality** for generated diagrams
- **Responsive design** that works on mobile and desktop

## REST API

### Render Diagram
```http
POST /api/render
Content-Type: application/json

{
  "code": "graph TD\\n    A --> B",
  "type": "auto",     // auto, mermaid, plantuml, graphviz
  "format": "html",   // html, png
  "theme": "default"  // for Mermaid diagrams
}
```

**Response:**
```json
{
  "success": true,
  "diagram_type": "mermaid",
  "format": "html",
  "content": "<!DOCTYPE html>...",
  "error": null
}
```

### Other Endpoints

- `GET /health` - Health check
- `GET /api/examples` - Get example diagrams
- `GET /docs` - Interactive API documentation

## Example Usage

### Web Interface
1. Paste diagram code in the editor
2. Select diagram type (or use auto-detect)
3. Choose output format (HTML or PNG)
4. Click "Render" to preview
5. Download the result

### API Integration
```python
import requests

response = requests.post('http://localhost:8000/api/render', json={
    'code': '''
    graph TD
        A[Start] --> B{Decision}
        B -->|Yes| C[End]
        B -->|No| A
    ''',
    'type': 'mermaid',
    'format': 'html'
})

result = response.json()
if result['success']:
    with open('diagram.html', 'w') as f:
        f.write(result['content'])
```

### cURL Example
```bash
curl -X POST "http://localhost:8000/api/render" \\
     -H "Content-Type: application/json" \\
     -d '{
       "code": "digraph G { A -> B; B -> C; }",
       "type": "graphviz", 
       "format": "html"
     }'
```

## Supported Diagram Types

### Mermaid
- Flowcharts, sequence diagrams, class diagrams
- State diagrams, ER diagrams, user journeys
- Gantt charts, pie charts, and more

### PlantUML  
- UML diagrams (class, sequence, use case, activity)
- Network diagrams, mind maps
- Gantt charts, work breakdown structure

### Graphviz
- DOT language diagrams
- Directed and undirected graphs
- Network diagrams, organizational charts

## Development

The webapp is built with:
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server
- **Pure HTML/CSS/JS** - No frontend framework dependencies

To extend the webapp:
1. Add new endpoints in `webapp.py`
2. Modify the HTML template for UI changes
3. Update the API models for new features

## Deployment

For production deployment:

1. **Use production ASGI server:**
   ```bash
   uvicorn webapp:app --host 0.0.0.0 --port 8000
   ```

2. **Docker deployment:**
   ```dockerfile
   FROM python:3.11-slim
   COPY . /app
   WORKDIR /app
   RUN pip install uv && uv sync --extra webapp
   CMD ["uv", "run", "--extra", "webapp", "uvicorn", "webapp:app", "--host", "0.0.0.0"]
   ```

3. **Environment variables:**
   - `HOST` - Bind host (default: 0.0.0.0)
   - `PORT` - Bind port (default: 8000)
   - `LOG_LEVEL` - Logging level (default: info)

## Limitations

- PNG export currently returns a placeholder (HTML export with browser download recommended)
- PlantUML uses local DOT conversion (not full PlantUML server)
- No authentication or rate limiting (add for production use)
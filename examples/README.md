# Examples

This directory contains example applications and interfaces that demonstrate different ways to use the diagram-renderer library.

## Overview

The `examples/` directory contains various **interfaces** (or "frontends") that expose the core diagram rendering functionality in different ways:

- **CLI** (`cli.py`) - Command-line interface for batch processing and scripting
- **Web Dashboard** (`dashboard.py`) - Interactive Streamlit app for visual editing
- **REST API** (`webapp.py`) - FastAPI server for HTTP-based rendering
- **MCP Server** (`mcp_server.py`) - Model Context Protocol server for AI assistant integration

Each interface serves different use cases and user needs, but all use the same core `diagram_renderer` library.

## Applications

### 1. Streamlit Dashboard (`dashboard.py`)

An interactive web application built with Streamlit that provides:
- Visual diagram editor with sample templates
- Real-time diagram preview with zoom/pan controls
- Auto-detection of diagram types (Mermaid, PlantUML, Graphviz)
- PNG download functionality
- Wide layout with side-by-side editor and preview

**Setup:**
```bash
# Install optional dependencies
uv sync --extra all
```

**Usage:**
```bash
# Run directly
uv run --extra dashboard python -m streamlit run examples/dashboard.py
```

### 2. Command Line Interface (`cli.py`)

A standalone CLI utility for batch processing and automation:
- Render diagrams from files to HTML
- Quick inline diagram rendering
- Serve diagrams via local HTTP server
- Diagram type detection and analysis
- File information and preview
- Example code generation

**Usage:**
```bash
# Render a diagram file
uv run examples/cli.py render diagram.mmd

# Quick render from command line
uv run examples/cli.py quick "graph TD; A-->B"

# Serve a diagram with HTTP server
uv run examples/cli.py serve diagram.mmd

# Show examples
uv run examples/cli.py examples

# Get file info
uv run examples/cli.py info diagram.mmd

# Show help
uv run examples/cli.py --help
```

### 3. Web API Server (`webapp.py`)

A FastAPI-based REST API server that provides:
- HTTP endpoints for diagram rendering
- Support for all diagram types (Mermaid, PlantUML, Graphviz)
- JSON request/response format
- Automatic API documentation (Swagger UI)
- CORS support for web integration

**Setup:**
```bash
# Install webapp dependencies
uv sync --extra webapp
```

**Usage:**
```bash
# Run the server
uv run --extra webapp python examples/webapp.py

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Example API call:**
```bash
curl -X POST "http://localhost:8000/render" \
  -H "Content-Type: application/json" \
  -d '{"code": "graph TD; A-->B", "diagram_type": "mermaid"}'
```

### 4. MCP Server (`mcp_server.py`)

A Model Context Protocol (MCP) server that exposes diagram rendering as a tool for AI assistants:
- Allows AI assistants (like Claude) to render diagrams
- Supports all diagram types with automatic detection
- Provides both synchronous and async interfaces
- Includes error handling and validation

**What is MCP?**
MCP (Model Context Protocol) is a standard for exposing tools and functions that AI assistants can use. This server allows AI systems to generate and render diagrams as part of their responses.

**Setup:**
```bash
# Install MCP dependencies
uv sync --extra mcp
```

**Usage:**
```bash
# Run the MCP server
uv run --extra mcp python examples/mcp_server.py

# The server can then be configured in MCP-compatible AI tools
```

**Use cases:**
- AI-powered documentation generation
- Chatbot diagram rendering
- Automated diagram creation from natural language
- Integration with AI development tools

## Use Cases by Interface

### Streamlit Dashboard
- **Interactive development** - Visual editing and immediate feedback
- **Demonstrations** - Showcasing diagram capabilities
- **Prototyping** - Quick diagram creation and testing
- **Educational** - Learning diagram syntax with examples
- **Non-technical users** - User-friendly web interface

### CLI Tool
- **Batch processing** - Convert multiple diagram files
- **Local serving** - Quick preview with HTTP server
- **CI/CD integration** - Automated diagram generation
- **Documentation builds** - Generate diagrams for docs
- **Scripting** - Programmatic diagram creation
- **Developer workflows** - Command-line integration

### Web API (FastAPI)
- **Microservices** - Diagram rendering as a service
- **Web applications** - Backend for web-based diagram tools
- **Cross-platform** - Language-agnostic HTTP API
- **Scalable deployment** - Can be containerized and scaled
- **Integration** - Easy integration with existing systems

### MCP Server
- **AI assistants** - Enable AI tools to render diagrams
- **Chatbots** - Add diagram capabilities to conversational AI
- **Automated documentation** - AI-generated technical diagrams
- **Natural language to diagram** - Convert descriptions to visuals
- **Tool augmentation** - Extend AI capabilities with visualization

## Integration Examples

Both examples show different patterns for using the core `diagram` library:

```python
from diagram_renderer import DiagramRenderer

# Basic usage
renderer = DiagramRenderer()
html = renderer.render_diagram_auto(diagram_code)

# Type detection
diagram_type = renderer.detect_diagram_type(code)
```

The examples demonstrate:
- Error handling and user feedback
- File I/O operations
- Integration with web frameworks (Streamlit)
- Command-line argument processing (Click)
- Progress indication and status reporting

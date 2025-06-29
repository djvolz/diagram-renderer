# Examples

This directory contains example applications that demonstrate how to use the diagram-render library.

## Applications

### 1. Streamlit Dashboard (`dashboard.py`)

An interactive web application built with Streamlit that provides:
- Visual diagram editor with sample templates
- Real-time diagram preview with zoom/pan controls
- Auto-detection of diagram types (Mermaid, PlantUML, Graphviz)
- PNG download functionality
- Wide layout with side-by-side editor and preview

**Usage:**
```bash
# Launch via main entry point
uv run main.py dashboard

# Or run directly
uv run streamlit run examples/dashboard.py
```

### 2. Command Line Interface (`cli.py`)

A standalone CLI utility for batch processing and automation:
- Render diagrams from files to HTML
- Quick inline diagram rendering
- Diagram type detection and analysis
- File information and preview
- Example code generation

**Usage:**
```bash
# Render a diagram file
uv run python examples/cli.py render diagram.mmd

# Quick render from command line
uv run python examples/cli.py quick "graph TD; A-->B"

# Show examples
uv run python examples/cli.py examples

# Get file info
uv run python examples/cli.py info diagram.mmd

# Show help
uv run python examples/cli.py --help
```

## Use Cases

### Streamlit Dashboard
- **Interactive development** - Visual editing and immediate feedback
- **Demonstrations** - Showcasing diagram capabilities
- **Prototyping** - Quick diagram creation and testing
- **Educational** - Learning diagram syntax with examples

### CLI Tool
- **Batch processing** - Convert multiple diagram files
- **CI/CD integration** - Automated diagram generation
- **Documentation builds** - Generate diagrams for docs
- **Scripting** - Programmatic diagram creation

## Integration Examples

Both examples show different patterns for using the core `diagram` library:

```python
from diagram import DiagramRenderer

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
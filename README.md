# Diagram Renderer

A comprehensive diagram rendering service supporting Mermaid, PlantUML, and Graphviz diagrams with an interactive web interface:

- **Streamlit Dashboard** - Interactive web interface for diagram rendering

## Features

- Automatic diagram type detection (Mermaid, PlantUML, Graphviz)
- **Self-contained rendering** - All JavaScript libraries hosted locally
- Static Mermaid.js assets (version controlled, 2.8MB)
- VizJS for Graphviz/DOT rendering (locally hosted, 1.9MB)
- PlantUML to DOT conversion and rendering
- Multiple themes for Mermaid diagrams
- Interactive Streamlit dashboard, FastAPI web app, and MCP server
- **No external CDN dependencies** - Works offline
- **AI Assistant Integration** - MCP server for Claude Desktop and other AI tools

## Installation

Install from PyPI:

```bash
# Using uv (recommended)
uv add diagram-renderer

# Using pip
pip install diagram-renderer
```

For development setup:
```bash
git clone https://github.com/djvolz/diagram-renderer.git
cd diagram-renderer
uv install
```

## Usage

### Examples

The `examples/` directory contains four demonstration applications:

**Streamlit Dashboard** - Interactive web interface:
```bash
uv sync --extra dashboard
# Run directly
uv run --extra dashboard python -m streamlit run examples/dashboard.py
# Or use the convenience script
uv run --extra dashboard ./examples/run-dashboard.py
```

**FastAPI Web App** - REST API and web interface:
```bash
uv sync --extra webapp
uv run --extra webapp python examples/cli.py webapp
# or directly: uv run --extra webapp python examples/webapp.py
```

**MCP Server** - AI assistant integration via Model Context Protocol:
```bash
uv sync --extra mcp
uv run --extra mcp python examples/cli.py mcp
# or directly: uv run --extra mcp python examples/mcp_server.py
```

**Command Line Interface** - Batch processing and automation:
```bash
# Render diagram from file
uv run python examples/cli.py render diagram.mmd

# Quick inline rendering
uv run python examples/cli.py quick "graph TD; A-->B"

# Serve a diagram with HTTP server
uv run python examples/cli.py serve diagram.mmd

# Show examples and help
uv run python examples/cli.py examples
uv run python examples/cli.py --help
```

## Supported Diagram Types

The visual-regression baselines cover the following diagram families:

### Mermaid
- Flowchart, Sequence, Class, State, and ER diagrams
- User Journey, Timeline, Requirement, and C4 Context diagrams
- Quadrant Charts, Pie Charts, and Gantt Charts
- Git Graphs plus beta features: XY Chart, Sankey, and Block diagrams

### PlantUML
- Sequence, Class, Use Case, Component, and State diagrams
- Deployment, Object, and Network diagrams

### Graphviz (DOT)
- Directed and Undirected graphs, Flowcharts, and Dependency graphs
- Organizational Charts, State Machines, Network Diagrams, and Cluster diagrams

## Visual Gallery

Interactive screenshots from our baseline suite are available below. Expand any section to preview the rendered output.

<details>
  <summary><strong>Mermaid Gallery</strong></summary>

  <p align="center">
    <img src="tests/visual/baselines/mermaid/demo_flowchart.png" alt="Mermaid Flowchart" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_sequence_diagram.png" alt="Mermaid Sequence Diagram" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_class_diagram.png" alt="Mermaid Class Diagram" width="280" />
    <br />
    <img src="tests/visual/baselines/mermaid/demo_state_diagram.png" alt="Mermaid State Diagram" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_entity_relationship_diagram.png" alt="Mermaid ER Diagram" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_user_journey.png" alt="Mermaid User Journey" width="280" />
    <br />
    <img src="tests/visual/baselines/mermaid/demo_timeline.png" alt="Mermaid Timeline" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_requirement_diagram.png" alt="Mermaid Requirement Diagram" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_c4_context_diagram.png" alt="Mermaid C4 Context Diagram" width="280" />
    <br />
    <img src="tests/visual/baselines/mermaid/demo_quadrant_chart.png" alt="Mermaid Quadrant Chart" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_pie_chart.png" alt="Mermaid Pie Chart" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_gantt_chart.png" alt="Mermaid Gantt Chart" width="280" />
    <br />
    <img src="tests/visual/baselines/mermaid/demo_git_graph.png" alt="Mermaid Git Graph" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_xy_chart.png" alt="Mermaid XY Chart" width="280" />
    <img src="tests/visual/baselines/mermaid/demo_sankey_diagram.png" alt="Mermaid Sankey Diagram" width="280" />
    <br />
    <img src="tests/visual/baselines/mermaid/demo_block_diagram.png" alt="Mermaid Block Diagram" width="280" />
  </p>
</details>

<details>
  <summary><strong>PlantUML Gallery</strong></summary>

  <p align="center">
    <img src="tests/visual/baselines/plantuml/plantuml_sequence_diagram.png" alt="PlantUML Sequence Diagram" width="280" />
    <img src="tests/visual/baselines/plantuml/plantuml_class_diagram.png" alt="PlantUML Class Diagram" width="280" />
    <img src="tests/visual/baselines/plantuml/plantuml_use_case_diagram.png" alt="PlantUML Use Case Diagram" width="280" />
    <br />
    <img src="tests/visual/baselines/plantuml/plantuml_component_diagram.png" alt="PlantUML Component Diagram" width="280" />
    <img src="tests/visual/baselines/plantuml/plantuml_state_diagram.png" alt="PlantUML State Diagram" width="280" />
    <img src="tests/visual/baselines/plantuml/plantuml_deployment_diagram.png" alt="PlantUML Deployment Diagram" width="280" />
    <br />
    <img src="tests/visual/baselines/plantuml/plantuml_object_diagram.png" alt="PlantUML Object Diagram" width="280" />
    <img src="tests/visual/baselines/plantuml/plantuml_network_diagram.png" alt="PlantUML Network Diagram" width="280" />
  </p>
</details>

<details>
  <summary><strong>Graphviz Gallery</strong></summary>

  <p align="center">
    <img src="tests/visual/baselines/graphviz/graphviz_directed_graph.png" alt="Graphviz Directed Graph" width="280" />
    <img src="tests/visual/baselines/graphviz/graphviz_undirected_graph.png" alt="Graphviz Undirected Graph" width="280" />
    <img src="tests/visual/baselines/graphviz/graphviz_flowchart.png" alt="Graphviz Flowchart" width="280" />
    <br />
    <img src="tests/visual/baselines/graphviz/graphviz_dependency_graph.png" alt="Graphviz Dependency Graph" width="280" />
    <img src="tests/visual/baselines/graphviz/graphviz_cluster_diagram.png" alt="Graphviz Cluster Diagram" width="280" />
    <img src="tests/visual/baselines/graphviz/graphviz_state_machine.png" alt="Graphviz State Machine" width="280" />
    <br />
    <img src="tests/visual/baselines/graphviz/graphviz_network_diagram.png" alt="Graphviz Network Diagram" width="280" />
    <img src="tests/visual/baselines/graphviz/graphviz_hierarchy.png" alt="Graphviz Organizational Chart" width="280" />
  </p>
</details>

## Configuration

### Mermaid Themes
- `default` - Default theme
- `base` - Base theme
- `dark` - Dark theme
- `forest` - Forest theme
- `neutral` - Neutral theme

## Development

The main components are:

- `diagram_renderer/` - Core diagram rendering logic and renderers
- `st_diagram.py` - Streamlit diagram component wrapper
- `examples/cli.py` - Command-line interface and app launcher
- `examples/dashboard.py` - Streamlit web interface
- `examples/webapp.py` - FastAPI REST API and web interface
- `examples/mcp_server.py` - MCP server for AI assistant integration
- `diagram_renderer/renderers/static/js/` - **Local JavaScript libraries**
  - `mermaid.min.js` (2.8MB) - Mermaid diagram rendering
  - `viz-full.js` (1.9MB) - Graphviz/DOT rendering
  - `viz-lite.js` (11KB) - Lightweight VizJS alternative

## Demo

**Input:**
```mermaid
flowchart LR
    A[diagram-renderer] --> B{Auto-detect}
    B -->|Mermaid| C[Mermaid.js]
    B -->|PlantUML| D[PlantUML → DOT]
    B -->|Graphviz| E[VizJS]
    C --> F[Interactive HTML]
    D --> F
    E --> F
    F --> G[📱 Responsive]
    F --> H[🖼 PNG Export]
    F --> I[🔍 Zoom/Pan]
```

**Output:** The generated HTML includes:
- 🔍 **Interactive zoom and pan controls**
- 📱 **Responsive design**
- 🖼 **PNG export functionality**
- 🎨 **Automatic diagram type detection**
- 🔒 **Self-contained** - All JS libraries included locally (no CDN dependencies)
- ⚡ **Two output modes** - Lightweight external JS (14KB) or fully embedded (4.7MB)

Try it yourself:
```bash
uv run python examples/cli.py quick "graph TD; A-->B-->C"
```

## Examples

### Mermaid Flowchart
```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E
```

### PlantUML Class Diagram
```plantuml
@startuml
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
@enduml
```

### Graphviz DOT Diagram
```dot
digraph G {
    A -> B;
    B -> C;
    C -> A;
}
```

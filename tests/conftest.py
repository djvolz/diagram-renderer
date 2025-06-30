"""
Pytest configuration and fixtures for diagram-renderer tests
"""
import pytest
from pathlib import Path
import tempfile
import os
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from diagram_renderer.renderers import MermaidRenderer, PlantUMLRenderer, GraphvizRenderer
from diagram_renderer import DiagramRenderer


@pytest.fixture
def mermaid_renderer():
    """Create a MermaidRenderer instance for testing"""
    return MermaidRenderer()


@pytest.fixture
def plantuml_renderer():
    """Create a PlantUMLRenderer instance for testing"""
    return PlantUMLRenderer()


@pytest.fixture
def graphviz_renderer():
    """Create a GraphvizRenderer instance for testing"""
    return GraphvizRenderer()


@pytest.fixture
def diagram_renderer():
    """Create a DiagramRenderer instance for testing"""
    return DiagramRenderer()


@pytest.fixture
def sample_mermaid_flowchart():
    """Sample Mermaid flowchart code"""
    return """
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
"""


@pytest.fixture
def sample_mermaid_sequence():
    """Sample Mermaid sequence diagram code"""
    return """
sequenceDiagram
    participant User
    participant Browser
    participant Server
    User->>Browser: Click button
    Browser->>Server: HTTP Request
    Server-->>Browser: Response
    Browser-->>User: Update UI
"""


@pytest.fixture
def sample_plantuml_sequence():
    """Sample PlantUML sequence diagram code"""
    return """
@startuml
participant User
participant Browser
participant Server
participant Database

User -> Browser: Enter URL
Browser -> Server: HTTP Request
Server -> Database: Query Data
Database -> Server: Return Data
Server -> Browser: HTTP Response
Browser -> User: Display Page
@enduml
"""


@pytest.fixture
def sample_plantuml_class():
    """Sample PlantUML class diagram code"""
    return """
@startuml
class User {
    +name: String
    +email: String
    +login()
}

class Admin {
    +permissions: List
    +manageUsers()
}

User <|-- Admin
@enduml
"""


@pytest.fixture
def sample_markdown_mermaid():
    """Sample Mermaid code wrapped in markdown"""
    return """
```mermaid
graph LR
    A --> B
    B --> C
```
"""


@pytest.fixture
def sample_markdown_plantuml():
    """Sample PlantUML code wrapped in markdown"""
    return """
```plantuml
@startuml
Alice -> Bob: Hello
@enduml
```
"""


@pytest.fixture
def sample_graphviz_simple():
    """Sample simple Graphviz diagram code"""
    return """
digraph G {
    A -> B
    B -> C
    C -> A
}
"""


@pytest.fixture
def sample_graphviz_flowchart():
    """Sample Graphviz flowchart code"""
    return """
digraph workflow {
    rankdir=TD
    node [shape=box]
    
    Start [shape=ellipse]
    Process [label="Process Data"]
    End [shape=ellipse]
    
    Start -> Process
    Process -> End
}
"""


@pytest.fixture
def sample_graphviz_undirected():
    """Sample undirected Graphviz graph"""
    return """
graph network {
    A -- B
    B -- C
    C -- D
    D -- A
}
"""


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def static_js_exists():
    """Check if static JS files exist (skip tests if missing)"""
    static_dir = project_root / "diagram_renderer" / "static" / "js"
    mermaid_exists = (static_dir / "mermaid.min.js").exists()
    viz_lite_exists = (static_dir / "viz-lite.js").exists()
    viz_full_exists = (static_dir / "viz-full.js").exists()
    
    return {
        'mermaid': mermaid_exists,
        'plantuml': viz_lite_exists and viz_full_exists,
        'graphviz': viz_lite_exists and viz_full_exists,
        'all': mermaid_exists and viz_lite_exists and viz_full_exists
    }
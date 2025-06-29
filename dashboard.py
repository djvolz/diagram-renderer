import streamlit as st
from st_diagram import StreamlitDiagramRenderer

def generate_sample_diagrams():
    """Generate sample Mermaid and PlantUML diagrams"""
    samples = {
        "Mermaid Flowchart": """
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E
""",
        "Mermaid Sequence": """
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob, how are you?
    B-->>A: Great! How about you?
    A->>B: I'm doing well, thanks!
""",
        "Mermaid Class Diagram": """
classDiagram
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
""",
        "PlantUML Class Diagram": """
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
""",
        "PlantUML Sequence": """
@startuml
actor User
participant "Web Browser" as Browser
participant "Web Server" as Server
participant Database

User -> Browser: Enter URL
Browser -> Server: HTTP Request
Server -> Database: Query Data
Database -> Server: Return Data
Server -> Browser: HTTP Response
Browser -> User: Display Page
@enduml
""",
        "PlantUML Use Case": """
@startuml
actor Customer
actor Admin

rectangle "E-commerce System" {
  Customer -- (Browse Products)
  Customer -- (Add to Cart)
  Customer -- (Checkout)
  Admin -- (Manage Products)
  Admin -- (View Orders)
}
@enduml
""",
        "Graphviz Simple Graph": """
digraph G {
    A -> B
    B -> C
    C -> D
    D -> A
}
""",
        "Graphviz Flowchart": """
digraph workflow {
    rankdir=TD
    node [shape=box, style=rounded]
    
    Start [shape=ellipse, style=filled, fillcolor=lightgreen]
    Process [label="Process Data"]
    Decision [shape=diamond, label="Valid?"]
    Success [shape=ellipse, style=filled, fillcolor=lightblue, label="Success"]
    Error [shape=ellipse, style=filled, fillcolor=lightcoral, label="Error"]
    
    Start -> Process
    Process -> Decision
    Decision -> Success [label="Yes"]
    Decision -> Error [label="No"]
}
""",
        "Graphviz Network": """
graph network {
    layout=circo
    node [shape=circle, style=filled]
    
    Server [fillcolor=lightblue]
    DB [fillcolor=lightgreen, label="Database"]
    API [fillcolor=lightyellow]
    Client1 [fillcolor=lightcoral, label="Client 1"]
    Client2 [fillcolor=lightcoral, label="Client 2"]
    
    Server -- DB
    Server -- API
    API -- Client1
    API -- Client2
}
"""
    }
    return samples

def main():
    st.set_page_config(
        page_title="Diagram Generator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Diagram Generator with Mermaid, PlantUML & Graphviz")
    st.markdown("Generate beautiful diagrams using Mermaid.js, PlantUML, and Graphviz with automatic type detection!")
    
    # Initialize renderer
    renderer = StreamlitDiagramRenderer()
    
    
    
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Diagram Code Editor")
        
        # Sample diagrams
        samples = generate_sample_diagrams()
        sample_choice = st.selectbox("Choose a sample diagram:", ["Custom"] + list(samples.keys()))
        
        # Code editor
        if sample_choice != "Custom":
            default_code = samples[sample_choice]
        else:
            default_code = """graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B"""
        
        diagram_code = st.text_area(
            "Enter your diagram code:",
            value=default_code,
            height=300,
            help="Enter valid Mermaid or PlantUML syntax. The system will auto-detect the type."
        )

        
        
        # Validation button
        if st.button("🔍 Validate & Preview"):
            if diagram_code.strip():
                st.session_state.diagram_code = diagram_code
                detected_type = renderer.detect_diagram_type(diagram_code)
                st.session_state.detected_type = detected_type
                
                # Show detected diagram type
                if detected_type:
                    st.info(f"Detected diagram type: {detected_type.upper()}")
                else:
                    st.warning("No specific diagram type detected. Please ensure your code is valid Mermaid, PlantUML, or Graphviz.")
            else:
                st.error("Please enter some diagram code!")
    
    with col2:
        st.header("📊 Diagram Preview")
        st.info("🖱️ Use mouse wheel to zoom, drag to pan, + / - buttons to zoom, ⌂ to reset, and 📥 to download PNG")
        
        # Render diagram
        if hasattr(st.session_state, 'diagram_code'):
            if st.session_state.detected_type:
                with st.container():
                    success = renderer.render_diagram_auto(
                        st.session_state.diagram_code,
                        height=600
                    )
                
                if success:
                    st.success("✅ Diagram rendered successfully!")
                else:
                    st.info("Please check your diagram syntax and try again.")
            else:
                st.warning("No diagram detected in the provided code. Please enter valid diagram syntax.")
        else:
            st.info("👆 Click 'Validate & Preview' to render your diagram")
            st.markdown("**Supported formats:** Mermaid, PlantUML, and Graphviz")
    
    # Footer with additional info
    st.markdown("---")
    with st.expander("ℹ️ About Diagram Support"):
        st.markdown("""
        This application supports both **Mermaid** and **PlantUML** diagram formats with automatic type detection.
        
        **Mermaid Diagram Types:**
        - Flowcharts, Sequence diagrams, Class diagrams
        - State diagrams, ER diagrams, User journey
        - Gantt charts, Pie charts, and more!
        
        **PlantUML Diagram Types:**
        - UML diagrams (Class, Sequence, Use Case, Activity)
        - Network diagrams, Mind maps
        - Gantt charts, Work breakdown structure
        
        **Features:**
        - 🤖 Automatic diagram type detection
        - 📁 Static Mermaid.js assets (version controlled)
        - 🌐 PlantUML server rendering
        - 🎨 Multiple themes for Mermaid diagrams
        
        **Documentation:**
        - [Mermaid.js](https://mermaid.js.org/)
        - [PlantUML](https://plantuml.com/)
        """)

if __name__ == "__main__":
    main()
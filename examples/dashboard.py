"""
Streamlit Dashboard for Diagram Renderer
Showcases all supported diagram types with comprehensive examples
"""

import streamlit as st
import streamlit.components.v1 as components

from diagram_renderer import DiagramRenderer


def get_mermaid_examples():
    """Get all Mermaid diagram examples"""
    return {
        "Flowchart": """flowchart TD
    A[Project Start] --> B{Requirements Clear?}
    B -->|Yes| C[Design Phase]
    B -->|No| D[Gather Requirements]
    D --> B

    C --> E[Development]
    E --> F[Testing]
    F --> G{Tests Pass?}
    G -->|No| E
    G -->|Yes| H[Deployment]

    H --> I[Maintenance]
    I --> J[End of Life]

    style A fill:#e1f5fe
    style H fill:#e8f5e8
    style J fill:#fce4ec""",
        "Sequence Diagram": """sequenceDiagram
    participant User
    participant Frontend
    participant Auth
    participant Database

    User->>Frontend: Login Request
    Frontend->>Auth: Validate Credentials
    Auth->>Database: Query User
    Database-->>Auth: User Data
    Auth-->>Frontend: JWT Token
    Frontend-->>User: Login Success

    User->>Frontend: Access Protected Resource
    Frontend->>Auth: Validate Token
    Auth-->>Frontend: Token Valid
    Frontend->>Database: Fetch Resource
    Database-->>Frontend: Resource Data
    Frontend-->>User: Display Resource""",
        "Class Diagram": """classDiagram
    class User {
        -int id
        -string email
        -string password
        +login()
        +logout()
        +updateProfile()
    }

    class Order {
        -int orderId
        -date orderDate
        -decimal total
        +calculateTotal()
        +addItem()
        +removeItem()
    }

    class Product {
        -int productId
        -string name
        -decimal price
        -int stock
        +updateStock()
        +getPrice()
    }

    class OrderItem {
        -int quantity
        -decimal unitPrice
        +getSubtotal()
    }

    User ||--o{ Order : places
    Order ||--o{ OrderItem : contains
    Product ||--o{ OrderItem : included_in""",
        "State Diagram": """stateDiagram-v2
    [*] --> Idle

    Idle --> Loading : user_action
    Loading --> Success : data_loaded
    Loading --> Error : load_failed

    Success --> Idle : reset
    Error --> Idle : retry
    Error --> Loading : auto_retry

    Success --> Updating : modify_data
    Updating --> Success : update_success
    Updating --> Error : update_failed""",
        "ER Diagram": """erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"

    USER {
        int user_id PK
        string email
        string password
        date created_at
    }

    ORDER {
        int order_id PK
        int user_id FK
        date order_date
        decimal total
    }

    PRODUCT {
        int product_id PK
        string name
        decimal price
        int stock
    }

    ORDER_ITEM {
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }""",
        "Gantt Chart": """gantt
    title Project Development Timeline
    dateFormat  YYYY-MM-DD
    section Planning
    Requirements Analysis    :done, req, 2024-01-01, 2024-01-07
    System Design          :done, design, 2024-01-05, 2024-01-12

    section Development
    Backend Development     :active, backend, 2024-01-10, 2024-02-15
    Frontend Development    :frontend, 2024-01-20, 2024-02-20
    Database Setup         :done, db, 2024-01-08, 2024-01-15

    section Testing
    Unit Testing           :testing, 2024-02-10, 2024-02-25
    Integration Testing    :int-test, 2024-02-20, 2024-03-05

    section Deployment
    Production Deployment  :deployment, 2024-03-01, 2024-03-07""",
        "Pie Chart": """pie title Browser Market Share 2024
    "Chrome" : 65.12
    "Safari" : 18.78
    "Edge" : 5.63
    "Firefox" : 4.23
    "Opera" : 2.87
    "Others" : 3.37""",
        "User Journey": """journey
    title Customer Shopping Experience
    section Discover
      Visit website: 5: Customer
      Browse products: 4: Customer
      View reviews: 3: Customer
    section Purchase
      Add to cart: 5: Customer
      Checkout: 3: Customer
      Payment: 2: Customer
    section Delivery
      Order processing: 3: Customer, Staff
      Shipping: 4: Customer
      Delivery: 5: Customer
    section Post-purchase
      Product usage: 5: Customer
      Leave review: 4: Customer
      Customer support: 2: Customer, Staff""",
        "Quadrant Chart": """quadrantChart
    title Marketing Campaign Analysis
    x-axis Low Cost --> High Cost
    y-axis Low Impact --> High Impact
    quadrant-1 High Impact, High Cost
    quadrant-2 High Impact, Low Cost
    quadrant-3 Low Impact, Low Cost
    quadrant-4 Low Impact, High Cost

    Social Media: [0.2, 0.8]
    Email Marketing: [0.1, 0.7]
    TV Advertising: [0.9, 0.6]
    Influencer Marketing: [0.7, 0.9]
    Print Advertising: [0.8, 0.3]
    Content Marketing: [0.3, 0.8]
    Radio: [0.6, 0.4]
    SEO: [0.2, 0.9]""",
        "Sankey Diagram": """%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ff0000'}}}%%
sankey-beta

%% Energy flow example
Coal,Electricity,30
Natural Gas,Electricity,35
Oil,Transportation,25
Renewable,Electricity,20
Electricity,Residential,25
Electricity,Commercial,20
Electricity,Industrial,45
Transportation,Personal,15
Transportation,Freight,10""",
        "XY Chart": """xychart-beta
    title "Sales Revenue Comparison (Q1 2024)"
    x-axis [Jan, Feb, Mar, Apr, May, Jun]
    y-axis "Revenue (K$)" 0 --> 100
    line [23, 45, 56, 78, 67, 89]
    bar [15, 25, 35, 45, 55, 65]""",
        "Timeline": """timeline
    title Web Development History

    1990s : Static HTML
          : CSS Introduction
          : JavaScript Birth

    2000s : AJAX Revolution
          : Web 2.0
          : jQuery Era

    2010s : Mobile First
          : SPA Frameworks
          : Node.js Rise

    2020s : JAMstack
          : Edge Computing
          : WebAssembly""",
        "Requirement Diagram": """requirementDiagram
    requirement user_auth {
        id: 1
        text: Users must authenticate securely
        risk: high
        verifymethod: test
    }

    requirement data_encryption {
        id: 2
        text: Data must be encrypted
        risk: high
        verifymethod: inspection
    }

    element login_system {
        type: simulation
    }

    user_auth - satisfies -> login_system
    data_encryption - contains -> user_auth""",
        "C4 Context": """C4Context
    title E-commerce System Context Diagram

    Person(customer, "Customer", "A customer who wants to purchase products online")
    Person(admin, "Administrator", "System administrator managing the platform")

    System(ecommerce, "E-commerce Platform", "Allows customers to browse and purchase products")

    System_Ext(payment, "Payment Gateway", "External payment processing system")
    System_Ext(shipping, "Shipping Service", "External shipping and logistics provider")
    System_Ext(inventory, "Inventory System", "External inventory management system")

    Rel(customer, ecommerce, "Browses products and places orders")
    Rel(admin, ecommerce, "Manages products and orders")
    Rel(ecommerce, payment, "Processes payments")
    Rel(ecommerce, shipping, "Arranges delivery")
    Rel(ecommerce, inventory, "Checks stock levels")""",
    }


def get_plantuml_examples():
    """Get all PlantUML diagram examples"""
    return {
        "Sequence Diagram": """@startuml
!theme plain
title User Authentication Flow

actor User
participant "Web App" as App
participant "Auth Service" as Auth
database "User DB" as DB

User -> App: Login Request
App -> Auth: Validate Credentials
Auth -> DB: Query User Data
DB --> Auth: User Found
Auth --> App: JWT Token
App --> User: Login Success

User -> App: Access Protected Resource
App -> Auth: Validate Token
Auth --> App: Token Valid
App -> DB: Fetch User Data
DB --> App: User Data
App --> User: Display Resource
@enduml""",
        "Class Diagram": """@startuml
!theme plain
title E-commerce System Classes

class User {
    -id: int
    -email: string
    -password: string
    +login()
    +logout()
    +updateProfile()
}

class Order {
    -orderId: int
    -orderDate: date
    -total: decimal
    +calculateTotal()
    +addItem()
    +removeItem()
}

class Product {
    -productId: int
    -name: string
    -price: decimal
    -stock: int
    +updateStock()
    +getPrice()
}

class OrderItem {
    -quantity: int
    -unitPrice: decimal
    +getSubtotal()
}

User "1" --> "0..*" Order : places
Order "1" --> "1..*" OrderItem : contains
Product "1" --> "0..*" OrderItem : "included in"
@enduml""",
        "Use Case Diagram": """@startuml
!theme plain
title E-commerce System Use Cases

left to right direction

actor Customer
actor Administrator
actor "Payment Gateway" as PG

rectangle "E-commerce System" {
    usecase "Browse Products" as UC1
    usecase "Add to Cart" as UC2
    usecase "Checkout" as UC3
    usecase "Process Payment" as UC4
    usecase "Manage Inventory" as UC5
    usecase "View Orders" as UC6
    usecase "Generate Reports" as UC7
}

Customer --> UC1
Customer --> UC2
Customer --> UC3
UC4 --> PG
Administrator --> UC5
Administrator --> UC6
Administrator --> UC7
UC3 ..> UC4 : includes
@enduml""",
        "Component Diagram": """@startuml
!theme plain
title System Architecture Components

package "Frontend" {
    [Web Application] as webapp
    [Mobile App] as mobile
}

package "API Gateway" {
    [Load Balancer] as lb
    [API Router] as router
}

package "Microservices" {
    [User Service] as user
    [Order Service] as order
    [Product Service] as product
    [Payment Service] as payment
}

package "Data Layer" {
    database "User DB" as userdb
    database "Order DB" as orderdb
    database "Product DB" as productdb
    cloud "Payment Gateway" as paymentgateway
}

webapp --> lb
mobile --> lb
lb --> router
router --> user
router --> order
router --> product
router --> payment

user --> userdb
order --> orderdb
product --> productdb
payment --> paymentgateway
@enduml""",
        "State Diagram": """@startuml
!theme plain
title Order State Machine

[*] --> Draft

Draft : Order being created
Draft --> Submitted : submit()

Submitted : Awaiting validation
Submitted --> Processing : validate()
Submitted --> Cancelled : cancel()

Processing : Payment processing
Processing --> Confirmed : payment_success()
Processing --> Failed : payment_failed()

Failed : Payment failed
Failed --> Submitted : retry()
Failed --> Cancelled : cancel()

Confirmed : Order confirmed
Confirmed --> Shipped : ship()
Confirmed --> Cancelled : cancel()

Shipped : Order in transit
Shipped --> Delivered : deliver()

Delivered : Order completed
Cancelled : Order cancelled

Delivered --> [*]
Cancelled --> [*]
@enduml""",
        "Deployment Diagram": """@startuml
!theme plain
title System Deployment Architecture

node "Load Balancer" {
    [nginx] as nginx
}

node "Web Servers" {
    [Web Server 1] as web1
    [Web Server 2] as web2
}

node "Application Servers" {
    [App Server 1] as app1
    [App Server 2] as app2
    [Background Jobs] as jobs
}

node "Database Cluster" {
    database "Primary DB" as primarydb
    database "Replica DB" as replicadb
    database "Cache" as cache
}

cloud "External Services" {
    [Payment API] as payment
    [Email Service] as email
    [Analytics] as analytics
}

nginx --> web1
nginx --> web2
web1 --> app1
web2 --> app2
app1 --> primarydb
app2 --> primarydb
primarydb --> replicadb
app1 --> cache
app2 --> cache
jobs --> payment
jobs --> email
jobs --> analytics
@enduml""",
        "Simple Object Diagram": """@startuml
title Sample E-commerce Order

object user1 {
    id = 123
    email = "john@example.com"
    name = "John Doe"
}

object order1 {
    orderId = 789
    orderDate = "2024-01-15"
    total = 89.97
    status = "shipped"
}

object product1 {
    productId = 456
    name = "Laptop"
    price = 899.99
    stock = 15
}

object orderItem1 {
    quantity = 1
    unitPrice = 899.99
}

user1 --> order1 : placed
order1 --> orderItem1 : contains
orderItem1 --> product1 : references
@enduml""",
    }


def get_graphviz_examples():
    """Get all Graphviz diagram examples"""
    return {
        "Directed Graph": """digraph system_architecture {
    rankdir=TB;
    bgcolor=white;
    node [shape=box, style=filled, fillcolor=lightblue, fontcolor=black];
    edge [color=darkblue, fontcolor=black];

    // Frontend Layer
    subgraph cluster_frontend {
        label="Frontend Layer";
        style=filled;
        fillcolor=lightyellow;
        "React App" -> "API Gateway";
        "Mobile App" -> "API Gateway";
    }

    // Backend Services
    subgraph cluster_backend {
        label="Backend Services";
        style=filled;
        fillcolor=lightgreen;
        "API Gateway" -> "User Service";
        "API Gateway" -> "Order Service";
        "API Gateway" -> "Product Service";
    }

    // Data Layer
    subgraph cluster_data {
        label="Data Layer";
        style=filled;
        fillcolor=lightcoral;
        "User Service" -> "User DB";
        "Order Service" -> "Order DB";
        "Product Service" -> "Product DB";
    }
}""",
        "Undirected Network": """graph network_topology {
    layout=neato;
    bgcolor=white;
    node [shape=circle, style=filled, fillcolor=lightblue, fontcolor=black];
    edge [color=gray, penwidth=2, fontcolor=black];

    // Core network nodes
    Router1 [fillcolor=orange, fontcolor=black, label="Core Router"];
    Router2 [fillcolor=orange, fontcolor=black, label="Edge Router"];

    // Switches
    Switch1 [fillcolor=lightblue, fontcolor=black, shape=box];
    Switch2 [fillcolor=lightblue, fontcolor=black, shape=box];
    Switch3 [fillcolor=lightblue, fontcolor=black, shape=box];

    // End devices
    Server1 [fillcolor=yellow, fontcolor=black, shape=box];
    Server2 [fillcolor=yellow, fontcolor=black, shape=box];
    PC1 [fillcolor=lightcyan, fontcolor=black];
    PC2 [fillcolor=lightcyan, fontcolor=black];
    PC3 [fillcolor=lightcyan, fontcolor=black];

    // Network connections
    Router1 -- Router2;
    Router1 -- Switch1;
    Router2 -- Switch2;
    Router2 -- Switch3;

    Switch1 -- Server1;
    Switch1 -- Server2;
    Switch2 -- PC1;
    Switch2 -- PC2;
    Switch3 -- PC3;
}""",
        "Process Flowchart": """digraph order_process {
    rankdir=TD;
    bgcolor=white;
    node [shape=box, style=rounded, fillcolor=white, style="filled,rounded", fontcolor=black];
    edge [fontcolor=black];

    start [shape=ellipse, fillcolor=lightgreen, fontcolor=black, label="Start"];
    end [shape=ellipse, fillcolor=lightcoral, fontcolor=black, label="End"];

    decision1 [shape=diamond, fillcolor=lightyellow, fontcolor=black, label="Valid Order?"];
    decision2 [shape=diamond, fillcolor=lightyellow, fontcolor=black, label="Payment Success?"];

    process1 [fillcolor=lightblue, fontcolor=black, label="Validate Order"];
    process2 [fillcolor=lightblue, fontcolor=black, label="Process Payment"];
    process3 [fillcolor=lightblue, fontcolor=black, label="Ship Order"];
    process4 [fillcolor=lightblue, fontcolor=black, label="Send Confirmation"];

    error1 [fillcolor=lightpink, fontcolor=black, label="Send Error Message"];
    error2 [fillcolor=lightpink, fontcolor=black, label="Refund Payment"];

    start -> process1;
    process1 -> decision1;

    decision1 -> process2 [label="Yes"];
    decision1 -> error1 [label="No"];

    process2 -> decision2;
    decision2 -> process3 [label="Yes"];
    decision2 -> error2 [label="No"];

    process3 -> process4;
    process4 -> end;
    error1 -> end;
    error2 -> end;
}""",
        "Organizational Chart": """digraph org_chart {
    rankdir=TB;
    bgcolor=white;
    node [shape=box, style=filled, fillcolor=lightblue, fontcolor=black];
    edge [fontcolor=black];

    CEO [fillcolor=gold, label="CEO"];

    // VPs
    VP_Eng [fillcolor=lightgreen, label="VP Engineering"];
    VP_Sales [fillcolor=lightgreen, label="VP Sales"];
    VP_Marketing [fillcolor=lightgreen, label="VP Marketing"];

    // Engineering Team
    Dir_Frontend [fillcolor=lightcyan, label="Frontend Director"];
    Dir_Backend [fillcolor=lightcyan, label="Backend Director"];
    Dir_DevOps [fillcolor=lightcyan, label="DevOps Director"];

    // Sales Team
    Sales_Manager [fillcolor=lightcyan, label="Sales Manager"];
    Account_Manager [fillcolor=lightcyan, label="Account Manager"];

    // Marketing Team
    Product_Manager [fillcolor=lightcyan, label="Product Manager"];
    Content_Manager [fillcolor=lightcyan, label="Content Manager"];

    // Team members
    Dev1 [fillcolor=white, label="Developer"];
    Dev2 [fillcolor=white, label="Developer"];
    Dev3 [fillcolor=white, label="Developer"];
    Dev4 [fillcolor=white, label="Developer"];

    // Hierarchy
    CEO -> {VP_Eng VP_Sales VP_Marketing};
    VP_Eng -> {Dir_Frontend Dir_Backend Dir_DevOps};
    VP_Sales -> {Sales_Manager Account_Manager};
    VP_Marketing -> {Product_Manager Content_Manager};

    Dir_Frontend -> {Dev1 Dev2};
    Dir_Backend -> {Dev3 Dev4};
}""",
        "State Machine": """digraph state_machine {
    rankdir=LR;
    bgcolor=white;
    node [shape=circle, style=filled, fontcolor=black];
    edge [fontcolor=black];

    // Special states
    Start [shape=point, fillcolor=black];
    End [shape=doublecircle, fillcolor=lightgreen, label="End"];

    // States
    Idle [fillcolor=lightblue];
    Processing [fillcolor=lightyellow];
    Waiting [fillcolor=lightcyan];
    Error [fillcolor=lightcoral];

    // Transitions
    Start -> Idle;
    Idle -> Processing [label="start"];
    Processing -> Waiting [label="async"];
    Waiting -> Processing [label="callback"];
    Processing -> Idle [label="complete"];
    Processing -> Error [label="fail"];
    Error -> Idle [label="reset"];
    Idle -> End [label="shutdown"];
}""",
        "Dependency Graph": """digraph dependencies {
    rankdir=BT;
    bgcolor=white;
    node [shape=box, style=filled, fillcolor=lightblue, fontcolor=black];
    edge [fontcolor=black];

    // Core modules
    "app.js" [fillcolor=gold];
    "database.js" [fillcolor=lightgreen];
    "auth.js" [fillcolor=lightgreen];
    "api.js" [fillcolor=lightgreen];

    // Utilities
    "logger.js" [fillcolor=lightcyan];
    "config.js" [fillcolor=lightcyan];
    "utils.js" [fillcolor=lightcyan];

    // External
    "express" [fillcolor=lightgray, shape=ellipse];
    "mongoose" [fillcolor=lightgray, shape=ellipse];
    "jsonwebtoken" [fillcolor=lightgray, shape=ellipse];

    // Dependencies
    "app.js" -> {"database.js" "auth.js" "api.js" "logger.js" "config.js"};
    "api.js" -> {"auth.js" "database.js" "utils.js"};
    "auth.js" -> {"jsonwebtoken" "database.js"};
    "database.js" -> {"mongoose" "config.js"};
    "logger.js" -> "config.js";
    "api.js" -> "express";
}""",
    }


def main():
    st.set_page_config(
        page_title="Diagram Renderer Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("📊 Diagram Renderer Dashboard")
    st.markdown(
        "Interactive diagram generation using **Mermaid**, **PlantUML**, and **Graphviz** with automatic type detection"
    )

    # Initialize renderer
    renderer = DiagramRenderer()

    # Sidebar for diagram selection
    with st.sidebar:
        st.header("📚 Diagram Library")

        diagram_type = st.selectbox(
            "Select Diagram Type:", ["Mermaid", "PlantUML", "Graphviz", "Custom"]
        )

        if diagram_type == "Mermaid":
            examples = get_mermaid_examples()
            selected_example = st.selectbox("Choose Example:", list(examples.keys()))
            default_code = examples[selected_example]

        elif diagram_type == "PlantUML":
            examples = get_plantuml_examples()
            selected_example = st.selectbox("Choose Example:", list(examples.keys()))
            default_code = examples[selected_example]

        elif diagram_type == "Graphviz":
            examples = get_graphviz_examples()
            selected_example = st.selectbox("Choose Example:", list(examples.keys()))
            default_code = examples[selected_example]

        else:  # Custom
            default_code = """graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[End]
    C -->|No| B"""
            selected_example = "Custom Diagram"

        st.markdown("---")
        st.markdown(
            """
            ### 🎯 Features
            - 🔄 **Auto-renders** when you select examples
            - ✨ Auto-detects diagram type
            - 🖱️ Interactive pan & zoom
            - 📥 Download as PNG or source
            - 🎨 Multiple diagram formats
            - 🔧 Error handling & validation
            """
        )

    # Main content area
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.header("✏️ Code Editor")

        # Show current selection info
        if diagram_type != "Custom":
            st.info(f"📝 **{diagram_type}** › {selected_example}")

        # Code editor
        diagram_code = st.text_area(
            "Edit diagram code:",
            value=default_code,
            height=400,
            help="Enter valid Mermaid, PlantUML, or Graphviz syntax. The system will auto-detect the type.",
            key="code_editor",
        )

        # Store the current code and auto-detect type
        if diagram_code.strip():
            st.session_state.diagram_code = diagram_code
            st.session_state.detected_type = renderer.detect_diagram_type(diagram_code)
            st.session_state.should_render = True

        # Show detection status
        if hasattr(st.session_state, "detected_type"):
            if st.session_state.detected_type:
                st.success(f"✅ Detected: **{st.session_state.detected_type.upper()}** diagram")
            else:
                st.warning("⚠️ Could not detect diagram type. Please check syntax.")

        # Action buttons
        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            refresh_btn = st.button(
                "🔄 Refresh",
                type="primary",
                use_container_width=True,
                help="Force re-render the diagram",
            )

        with col_btn2:
            clear_btn = st.button("🗑️ Clear", use_container_width=True, help="Clear the editor")

        if clear_btn:
            st.session_state.diagram_code = ""
            st.session_state.detected_type = None
            st.session_state.should_render = False
            st.rerun()

        if refresh_btn:
            st.session_state.should_render = True

    with col2:
        st.header("🖼️ Preview")

        # Help text
        with st.expander("ℹ️ Interactive Controls", expanded=False):
            st.markdown(
                """
                - **🖱️ Drag** to pan around
                - **⊕ / ⊖** to zoom in/out
                - **↻** to reset view
                - **📷** to download as PNG
                - **</>** to download source code
                - **❓** for keyboard shortcuts
                """
            )

        # Auto-render diagram when code changes or example is selected
        if hasattr(st.session_state, "diagram_code") and hasattr(st.session_state, "should_render"):
            if st.session_state.should_render and st.session_state.detected_type:
                with st.container():
                    try:
                        html_content = renderer.render_diagram_auto(st.session_state.diagram_code)
                        if html_content:
                            components.html(html_content, height=500, width=None, scrolling=False)
                            with st.container():
                                st.success("✅ Rendered successfully!")
                        else:
                            st.error("❌ Rendering failed. Check your syntax.")
                    except Exception as e:
                        st.error(f"❌ Error rendering diagram: {str(e)}")
            elif st.session_state.should_render:
                st.warning("⚠️ No valid diagram detected. Please check your syntax.")
        else:
            st.info(
                "💡 Select an example or paste your diagram code to see it rendered automatically."
            )

        # Show quick stats
        if hasattr(st.session_state, "diagram_code") and st.session_state.diagram_code:
            lines = st.session_state.diagram_code.count("\n") + 1
            chars = len(st.session_state.diagram_code)
            st.caption(f"📊 {lines} lines, {chars} characters")

    # Footer
    st.markdown("---")

    # Documentation section
    with st.expander("📖 Documentation & Resources"):
        doc_col1, doc_col2, doc_col3 = st.columns(3)

        with doc_col1:
            st.markdown(
                """
                ### Mermaid
                - [Official Docs](https://mermaid.js.org/)
                - [Live Editor](https://mermaid.live/)
                - Flowcharts, Sequences
                - Class, State, ER diagrams
                - Gantt, Pie charts
                """
            )

        with doc_col2:
            st.markdown(
                """
                ### PlantUML
                - [Official Docs](https://plantuml.com/)
                - [Online Server](http://www.plantuml.com/plantuml)
                - UML diagrams
                - Network diagrams
                - Mind maps, WBS
                """
            )

        with doc_col3:
            st.markdown(
                """
                ### Graphviz
                - [Official Docs](https://graphviz.org/)
                - [Gallery](https://graphviz.org/gallery/)
                - Directed/undirected graphs
                - Hierarchies, networks
                - State machines
                """
            )

    # About section in sidebar bottom
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            ### 💡 About
            **Diagram Renderer** v2024.9

            Powered by:
            - Mermaid.js v11.6.0
            - PlantUML (VizJS)
            - Graphviz (VizJS)

            [GitHub](https://github.com/djvolz/diagram-renderer) |
            [PyPI](https://pypi.org/project/diagram-renderer/)
            """
        )


if __name__ == "__main__":
    main()

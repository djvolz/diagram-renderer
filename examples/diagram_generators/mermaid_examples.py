"""
Mermaid diagram example definitions.
"""


def get_mermaid_examples():
    """Get all Mermaid diagram examples"""
    return {
        "demo_flowchart.html": {
            "name": "Mermaid Flowchart",
            "type": "mermaid",
            "code": """flowchart TD
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
        },
        "demo_sequence_diagram.html": {
            "name": "Mermaid Sequence Diagram",
            "type": "mermaid",
            "code": """sequenceDiagram
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
        },
        "demo_class_diagram.html": {
            "name": "Mermaid Class Diagram",
            "type": "mermaid",
            "code": """classDiagram
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

    User "1" --> "0..*" Order : places
    Order "1" --> "1..*" OrderItem : contains
    Product "1" --> "0..*" OrderItem : included_in""",
        },
        "demo_state_diagram.html": {
            "name": "Mermaid State Diagram",
            "type": "mermaid",
            "code": """stateDiagram-v2
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
        },
        "demo_entity_relationship_diagram.html": {
            "name": "Mermaid ER Diagram",
            "type": "mermaid",
            "code": """erDiagram
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
        },
        "demo_gantt_chart.html": {
            "name": "Mermaid Gantt Chart",
            "type": "mermaid",
            "code": """gantt
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
        },
        "demo_pie_chart.html": {
            "name": "Mermaid Pie Chart",
            "type": "mermaid",
            "code": """pie title Browser Market Share 2024
    "Chrome" : 65.12
    "Safari" : 18.78
    "Edge" : 5.63
    "Firefox" : 4.23
    "Opera" : 2.87
    "Others" : 3.37""",
        },
        "demo_user_journey.html": {
            "name": "Mermaid User Journey",
            "type": "mermaid",
            "code": """journey
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
        },
        "demo_quadrant_chart.html": {
            "name": "Mermaid Quadrant Chart",
            "type": "mermaid",
            "code": """quadrantChart
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
        },
        "demo_timeline.html": {
            "name": "Mermaid Timeline",
            "type": "mermaid",
            "code": """timeline
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
        },
        "demo_requirement_diagram.html": {
            "name": "Mermaid Requirement Diagram",
            "type": "mermaid",
            "code": """requirementDiagram
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
        },
        "demo_c4_context_diagram.html": {
            "name": "Mermaid C4 Context Diagram",
            "type": "mermaid",
            "code": """C4Context
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
        },
        # External/unsupported diagrams that show error messages
        "demo_xy_chart.html": {
            "name": "Mermaid XY Chart (Beta)",
            "type": "mermaid",
            "code": """xychart-beta
    title "Monthly Sales Performance"
    x-axis [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
    y-axis "Sales (in thousands)" 0 --> 100
    line [20, 35, 45, 38, 52, 68, 75, 80, 65, 58, 70, 85]""",
            "expected_status": "external",
        },
        "demo_sankey_diagram.html": {
            "name": "Mermaid Sankey Diagram",
            "type": "mermaid",
            "code": """sankey-beta
    Energy Sources,Renewable,100
    Energy Sources,Fossil Fuels,200
    Renewable,Solar,50
    Renewable,Wind,30
    Renewable,Hydro,20
    Fossil Fuels,Coal,80
    Fossil Fuels,Natural Gas,90
    Fossil Fuels,Oil,30""",
            "expected_status": "external",
        },
        "demo_block_diagram.html": {
            "name": "Mermaid Block Diagram",
            "type": "mermaid",
            "code": """block-beta
    columns 3
    Frontend:3

    block:APIs:2
        AuthAPI
        DataAPI
    end
    Gateway

    Frontend --> Gateway
    Gateway --> AuthAPI
    Gateway --> DataAPI

    block:Backend:3
        UserService
        OrderService
        ProductService
    end

    AuthAPI --> UserService
    DataAPI --> OrderService
    DataAPI --> ProductService

    Database:3""",
            "expected_status": "external",
        },
        "demo_git_graph.html": {
            "name": "Mermaid Git Graph",
            "type": "mermaid",
            "code": """%%{init: {'gitgraph': {'showBranches': true, 'showCommitLabel': true}} }%%
gitgraph
    commit id: "Initial commit"
    commit id: "Add basic structure"
    branch develop
    checkout develop
    commit id: "Feature A start"
    commit id: "Feature A complete"
    checkout main
    merge develop
    commit id: "Release v1.0"
    branch hotfix
    checkout hotfix
    commit id: "Fix critical bug"
    checkout main
    merge hotfix
    commit id: "Release v1.0.1\"""",
            "expected_status": "external",
        },
    }

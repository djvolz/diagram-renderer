#!/usr/bin/env python3
"""
Regenerate all example HTML files with correct diagram syntax
"""

import os
from pathlib import Path

from diagram_renderer import DiagramRenderer


def get_example_diagrams():
    """Define all example diagrams with corrected syntax"""
    return {
        "demo_flowchart.html": {
            "name": "Mermaid Flowchart",
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
        "demo_git_graph.html": {
            "name": "Mermaid Git Graph",
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
    commit id: "Release v1.0.1""",
        },
        "demo_pie_chart.html": {
            "name": "Mermaid Pie Chart",
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
        "demo_block_diagram.html": {
            "name": "Mermaid Block Diagram",
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
        },
        "demo_timeline.html": {
            "name": "Mermaid Timeline",
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
        "demo_xy_chart.html": {
            "name": "Mermaid XY Chart (Beta)",
            "code": """xychart-beta
    title "Monthly Sales Performance"
    x-axis [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
    y-axis "Sales (in thousands)" 0 --> 100
    line [20, 35, 45, 38, 52, 68, 75, 80, 65, 58, 70, 85]""",
        },
        "demo_sankey_diagram.html": {
            "name": "Mermaid Sankey Diagram",
            "code": """sankey-beta
    Energy Sources,Renewable,100
    Energy Sources,Fossil Fuels,200
    Renewable,Solar,50
    Renewable,Wind,30
    Renewable,Hydro,20
    Fossil Fuels,Coal,80
    Fossil Fuels,Natural Gas,90
    Fossil Fuels,Oil,30""",
        },
    }


def regenerate_all_examples():
    """Regenerate all example HTML files"""
    examples_dir = Path(__file__).parent
    renderer = DiagramRenderer()

    diagrams = get_example_diagrams()
    results = {"success": [], "failed": []}

    print("🚀 Regenerating all example HTML files...\n")

    for filename, diagram_info in diagrams.items():
        file_path = examples_dir / filename
        print(f"📝 Generating {diagram_info['name']}...")

        try:
            html_output = renderer.render_diagram_auto(diagram_info["code"])

            if html_output:
                # Write file regardless so users can see the error UI when present
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_output)

                # Classify status by scanning for our error markers
                lowered = html_output.lower()
                # Prefer explicit server-side error marker to avoid matching error strings inside JS
                has_error_meta = (
                    'name="diagram-render-status" content="error"' in html_output
                    or "name='diagram-render-status' content='error'" in html_output
                )
                is_unsupported = "unsupported diagram type" in lowered
                is_render_error = has_error_meta
                if is_unsupported or is_render_error:
                    print(f"❌ {filename} - Rendered with error UI")
                    results["failed"].append(filename)
                else:
                    print(f"✅ {filename} - Success")
                    results["success"].append(filename)
            else:
                print(f"❌ {filename} - Failed to render (returned None)")
                results["failed"].append(filename)

        except Exception as e:
            print(f"❌ {filename} - Error: {e}")
            results["failed"].append(filename)

    # Summary
    print("\n📊 Regeneration Results:")
    print(f"✅ Success: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")

    if results["failed"]:
        print("\n⚠️  Failed files:")
        for failed_file in results["failed"]:
            print(f"   - {failed_file}")

    print("\n🌐 You can view the examples at: http://localhost:8000/")

    return results


if __name__ == "__main__":
    results = regenerate_all_examples()

    # Generate a simple showcase file
    showcase_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Examples Showcase</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            transition: transform 0.2s;
        }
        .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .card h3 { margin: 0 0 10px 0; color: #2c3e50; }
        .card a {
            display: inline-block;
            padding: 8px 16px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
        }
        .card a:hover { background: #2980b9; }
        .status { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 10px; }
        .working { background: #d4edda; color: #155724; }
        .broken { background: #f8d7da; color: #721c24; }
        .beta { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Diagram Examples Showcase</h1>
        <p style="text-align: center; color: #666; margin-bottom: 40px;">
            Interactive diagram examples with consistent UI, pan/zoom controls, and download options
        </p>

        <div class="grid">"""

    diagrams = get_example_diagrams()
    for filename, diagram_info in diagrams.items():
        status_class = "working" if filename in results["success"] else "broken"
        status_text = "✅ Working" if filename in results["success"] else "❌ Broken"

        if (
            "beta" in diagram_info["code"].lower()
            or "sankey" in diagram_info["code"].lower()
            or "xychart" in diagram_info["code"].lower()
        ):
            status_class = "beta"
            status_text = "⚠️ Beta"

        showcase_content += f"""
            <div class="card">
                <h3>{diagram_info["name"]}<span class="status {status_class}">{status_text}</span></h3>
                <p>Interactive diagram with pan/zoom controls and export options.</p>
                <a href="{filename}">View Example →</a>
            </div>"""

    showcase_content += """
        </div>

        <div style="margin-top: 40px; text-align: center; color: #666;">
            <p><strong>🎯 All examples feature:</strong></p>
            <p>🖱️ Pan/zoom controls • ⌨️ Keyboard shortcuts • 💾 Download options • 📋 Copy to clipboard</p>
        </div>
    </div>
</body>
</html>"""

    showcase_path = Path(__file__).parent / "mermaid_showcase.html"
    with open(showcase_path, "w", encoding="utf-8") as f:
        f.write(showcase_content)

    print(f"📋 Generated showcase at: {showcase_path}")
    print("🎉 All done! Run the server and visit the showcase to see all examples.")

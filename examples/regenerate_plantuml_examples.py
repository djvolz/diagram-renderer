#!/usr/bin/env python3
"""
Generate PlantUML example HTML files with various diagram types
"""

import os
from pathlib import Path

from diagram_renderer import DiagramRenderer


def get_plantuml_example_diagrams():
    """Define all PlantUML example diagrams with various types"""
    return {
        "plantuml_sequence_diagram.html": {
            "name": "PlantUML Sequence Diagram",
            "code": """@startuml
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
        },
        "plantuml_class_diagram.html": {
            "name": "PlantUML Class Diagram",
            "code": """@startuml
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

User ||--o{ Order : places
Order ||--o{ OrderItem : contains
Product ||--o{ OrderItem : "included in"
@enduml""",
        },
        "plantuml_use_case_diagram.html": {
            "name": "PlantUML Use Case Diagram",
            "code": """@startuml
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
        },
        "plantuml_component_diagram.html": {
            "name": "PlantUML Component Diagram",
            "code": """@startuml
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
        },
        "plantuml_state_diagram.html": {
            "name": "PlantUML State Diagram",
            "code": """@startuml
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
        },
        "plantuml_deployment_diagram.html": {
            "name": "PlantUML Deployment Diagram",
            "code": """@startuml
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
        },
        "plantuml_object_diagram.html": {
            "name": "PlantUML Object Diagram",
            "code": """@startuml
title Sample E-commerce Order

class User {
  id = 123
  email = "john@example.com"
}

class Order {
  orderId = 789
  total = 89.97
}

User ||--o{ Order : places
@enduml""",
        },
        "plantuml_network_diagram.html": {
            "name": "PlantUML Network Diagram",
            "code": """@startuml
!theme plain
!include <aws/common>
!include <aws/Storage/AmazonS3/AmazonS3>
!include <aws/Compute/AmazonEC2/AmazonEC2>

title Cloud Infrastructure

package "VPC" {
    package "Public Subnet" {
        [Load Balancer] as lb
        [NAT Gateway] as nat
    }

    package "Private Subnet" {
        [Web Server 1] as web1
        [Web Server 2] as web2
        [Application Server] as app
    }

    package "Database Subnet" {
        database "Primary DB" as db1
        database "Replica DB" as db2
    }
}

cloud "Internet" as internet
cloud "CDN" as cdn

internet --> lb
lb --> web1
lb --> web2
web1 --> app
web2 --> app
app --> db1
db1 --> db2
nat --> internet
cdn --> internet
@enduml""",
        },
    }


def regenerate_all_plantuml_examples():
    """Regenerate all PlantUML example HTML files"""
    examples_dir = Path(__file__).parent
    renderer = DiagramRenderer()

    diagrams = get_plantuml_example_diagrams()
    results = {"success": [], "failed": []}

    print("🚀 Regenerating all PlantUML example HTML files...\n")

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
    print("\n📊 PlantUML Regeneration Results:")
    print(f"✅ Success: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")

    if results["failed"]:
        print("\n⚠️  Failed files:")
        for failed_file in results["failed"]:
            print(f"   - {failed_file}")

    print("\n🌐 You can view the examples at: http://localhost:8000/")

    return results


def generate_plantuml_showcase(results):
    """Generate PlantUML showcase HTML file"""
    showcase_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PlantUML Examples Showcase</title>
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
            background: #2c3e50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
        }
        .card a:hover { background: #1a252f; }
        .status { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 10px; }
        .working { background: #d4edda; color: #155724; }
        .broken { background: #f8d7da; color: #721c24; }
        .beta { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 PlantUML Examples Showcase</h1>
        <p style="text-align: center; color: #666; margin-bottom: 40px;">
            Interactive PlantUML diagrams with consistent UI, pan/zoom controls, and download options
        </p>

        <div class="grid">"""

    diagrams = get_plantuml_example_diagrams()
    for filename, diagram_info in diagrams.items():
        status_class = "working" if filename in results["success"] else "broken"
        status_text = "✅ Working" if filename in results["success"] else "❌ Broken"

        showcase_content += f"""
            <div class="card">
                <h3>{diagram_info["name"]}<span class="status {status_class}">{status_text}</span></h3>
                <p>Interactive PlantUML diagram with pan/zoom controls and export options.</p>
                <a href="{filename}">View Example →</a>
            </div>"""

    showcase_content += """
        </div>

        <div style="margin-top: 40px; text-align: center; color: #666;">
            <p><strong>🎯 All examples feature:</strong></p>
            <p>🖱️ Pan/zoom controls • ⌨️ Keyboard shortcuts • 💾 Download options • 📋 Copy to clipboard</p>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <h3>📚 PlantUML Resources</h3>
            <p><strong>Documentation:</strong> <a href="https://plantuml.com/">PlantUML.com</a></p>
            <p><strong>Diagram Types:</strong> Sequence, Class, Use Case, Activity, Component, State, Deployment, Object, Timing, Network</p>
        </div>
    </div>
</body>
</html>"""

    showcase_path = Path(__file__).parent / "plantuml_showcase.html"
    with open(showcase_path, "w", encoding="utf-8") as f:
        f.write(showcase_content)

    print(f"📋 Generated PlantUML showcase at: {showcase_path}")
    return showcase_path


if __name__ == "__main__":
    results = regenerate_all_plantuml_examples()
    generate_plantuml_showcase(results)
    print(
        "🎉 PlantUML examples complete! Run the server and visit the showcase to see all examples."
    )

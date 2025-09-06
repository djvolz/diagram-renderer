#!/usr/bin/env python3
"""
Generate Graphviz example HTML files with various diagram types
"""

import os
from pathlib import Path

from diagram_renderer import DiagramRenderer


def get_graphviz_example_diagrams():
    """Define all Graphviz example diagrams with various types"""
    return {
        "graphviz_directed_graph.html": {
            "name": "Graphviz Directed Graph",
            "code": """digraph system_architecture {
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
        "User Service" -> "User DB" [shape=cylinder];
        "Order Service" -> "Order DB" [shape=cylinder];
        "Product Service" -> "Product DB" [shape=cylinder];
    }
}""",
        },
        "graphviz_undirected_graph.html": {
            "name": "Graphviz Undirected Graph",
            "code": """graph network_topology {
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
        },
        "graphviz_flowchart.html": {
            "name": "Graphviz Flowchart",
            "code": """digraph order_process {
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
        },
        "graphviz_hierarchy.html": {
            "name": "Graphviz Organizational Chart",
            "code": """digraph org_chart {
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
    Marketing_Manager [fillcolor=lightcyan, label="Marketing Manager"];
    Content_Manager [fillcolor=lightcyan, label="Content Manager"];

    // Hierarchy
    CEO -> VP_Eng;
    CEO -> VP_Sales;
    CEO -> VP_Marketing;

    VP_Eng -> Dir_Frontend;
    VP_Eng -> Dir_Backend;
    VP_Eng -> Dir_DevOps;

    VP_Sales -> Sales_Manager;
    VP_Sales -> Account_Manager;

    VP_Marketing -> Marketing_Manager;
    VP_Marketing -> Content_Manager;
}""",
        },
        "graphviz_state_machine.html": {
            "name": "Graphviz State Machine",
            "code": """digraph user_session {
    rankdir=LR;
    bgcolor=white;
    node [shape=circle, style=filled, fontcolor=black];
    edge [fontcolor=black];

    // States
    Logged_Out [fillcolor=lightgray, label="Logged Out"];
    Logging_In [fillcolor=yellow, label="Logging In"];
    Logged_In [fillcolor=lightgreen, label="Logged In"];
    Session_Expired [fillcolor=orange, label="Session Expired"];
    Locked_Out [fillcolor=red, label="Locked Out"];

    // Entry and exit points
    start [shape=point, fillcolor=black];
    end [shape=doublecircle, fillcolor=black, label=""];

    // Transitions
    start -> Logged_Out;

    Logged_Out -> Logging_In [label="login_attempt"];
    Logging_In -> Logged_In [label="valid_credentials"];
    Logging_In -> Logged_Out [label="invalid_credentials"];
    Logging_In -> Locked_Out [label="too_many_attempts"];

    Logged_In -> Session_Expired [label="timeout"];
    Logged_In -> Logged_Out [label="logout"];

    Session_Expired -> Logged_Out [label="acknowledge"];
    Locked_Out -> Logged_Out [label="admin_unlock"];

    Logged_Out -> end [label="session_end"];
}""",
        },
        "graphviz_network_diagram.html": {
            "name": "Graphviz Network Diagram",
            "code": """graph data_flow {
    layout=dot;
    rankdir=LR;
    bgcolor=white;
    node [shape=box, style=filled, fontcolor=black];
    edge [penwidth=2, fontcolor=black];

    // Data Sources
    subgraph cluster_sources {
        label="Data Sources";
        style=filled;
        fillcolor=lightblue;

        API [fillcolor=lightcyan, label="REST API"];
        Database [shape=cylinder, fillcolor=lightcyan, label="Database"];
        Files [shape=folder, fillcolor=lightcyan, label="File System"];
    }

    // Processing
    subgraph cluster_processing {
        label="Data Processing";
        style=filled;
        fillcolor=lightgreen;

        ETL [fillcolor=lightseagreen, label="ETL Pipeline"];
        Analytics [fillcolor=lightseagreen, label="Analytics Engine"];
        ML [fillcolor=lightseagreen, label="ML Pipeline"];
    }

    // Outputs
    subgraph cluster_outputs {
        label="Outputs";
        style=filled;
        fillcolor=lightyellow;

        Dashboard [fillcolor=gold, label="Dashboard"];
        Reports [fillcolor=gold, label="Reports"];
        Alerts [fillcolor=gold, label="Alerts"];
    }

    // Data flow connections
    API -- ETL;
    Database -- ETL;
    Files -- ETL;

    ETL -- Analytics;
    ETL -- ML;

    Analytics -- Dashboard;
    Analytics -- Reports;
    ML -- Alerts;
}""",
        },
        "graphviz_dependency_graph.html": {
            "name": "Graphviz Dependency Graph",
            "code": """digraph dependencies {
    rankdir=TB;
    bgcolor=white;
    node [shape=box, style=filled, fillcolor=lightblue, fontcolor=black];
    edge [fontcolor=black];

    // Application layers
    UI [fillcolor=lightcyan, label="User Interface"];
    API [fillcolor=lightgreen, label="API Layer"];
    Business [fillcolor=lightyellow, label="Business Logic"];
    Data [fillcolor=lightcoral, label="Data Access"];
    Database [shape=cylinder, fillcolor=gray, label="Database"];

    // External dependencies
    Auth [shape=hexagon, fillcolor=orange, label="Auth Service"];
    Payment [shape=hexagon, fillcolor=orange, label="Payment API"];
    Email [shape=hexagon, fillcolor=orange, label="Email Service"];

    // Dependencies (arrows point from dependent to dependency)
    UI -> API;
    API -> Business;
    API -> Auth;
    Business -> Data;
    Business -> Payment;
    Business -> Email;
    Data -> Database;

    // Group external services
    {rank=same; Auth; Payment; Email;}
}""",
        },
        "graphviz_cluster_diagram.html": {
            "name": "Graphviz Cluster Diagram",
            "code": """digraph microservices {
    compound=true;
    rankdir=TB;
    bgcolor=white;
    node [shape=box, style=filled, fillcolor=lightblue, fontcolor=black];
    edge [fontcolor=black];

    // Frontend Cluster
    subgraph cluster_frontend {
        label="Frontend Services";
        style=filled;
        fillcolor=lightcyan;

        WebApp [label="Web Application"];
        MobileApp [label="Mobile App"];
        AdminPanel [label="Admin Panel"];
    }

    // API Gateway
    Gateway [shape=diamond, fillcolor=orange, label="API Gateway"];

    // Microservices Cluster
    subgraph cluster_services {
        label="Microservices";
        style=filled;
        fillcolor=lightgreen;

        UserSvc [label="User Service"];
        OrderSvc [label="Order Service"];
        ProductSvc [label="Product Service"];
        NotificationSvc [label="Notification Service"];
    }

    // Data Cluster
    subgraph cluster_data {
        label="Data Layer";
        style=filled;
        fillcolor=lightcoral;

        UserDB [shape=cylinder, label="User Database"];
        OrderDB [shape=cylinder, label="Order Database"];
        ProductDB [shape=cylinder, label="Product Database"];
        Cache [shape=cylinder, fillcolor=yellow, label="Redis Cache"];
    }

    // Connections
    WebApp -> Gateway;
    MobileApp -> Gateway;
    AdminPanel -> Gateway;

    Gateway -> UserSvc;
    Gateway -> OrderSvc;
    Gateway -> ProductSvc;

    UserSvc -> UserDB;
    OrderSvc -> OrderDB;
    ProductSvc -> ProductDB;

    UserSvc -> Cache;
    OrderSvc -> Cache;
    ProductSvc -> Cache;

    OrderSvc -> NotificationSvc;
}""",
        },
    }


def regenerate_all_graphviz_examples():
    """Regenerate all Graphviz example HTML files"""
    examples_dir = Path(__file__).parent
    renderer = DiagramRenderer()

    diagrams = get_graphviz_example_diagrams()
    results = {"success": [], "failed": []}

    print("🚀 Regenerating all Graphviz example HTML files...\n")

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
    print("\n📊 Graphviz Regeneration Results:")
    print(f"✅ Success: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")

    if results["failed"]:
        print("\n⚠️  Failed files:")
        for failed_file in results["failed"]:
            print(f"   - {failed_file}")

    print("\n🌐 You can view the examples at: http://localhost:8000/")

    return results


def generate_graphviz_showcase(results):
    """Generate Graphviz showcase HTML file"""
    showcase_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Graphviz Examples Showcase</title>
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
            background: #8B4513;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
        }
        .card a:hover { background: #654321; }
        .status { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 10px; }
        .working { background: #d4edda; color: #155724; }
        .broken { background: #f8d7da; color: #721c24; }
        .beta { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🕸️ Graphviz Examples Showcase</h1>
        <p style="text-align: center; color: #666; margin-bottom: 40px;">
            Interactive Graphviz diagrams with consistent UI, pan/zoom controls, and download options
        </p>

        <div class="grid">"""

    diagrams = get_graphviz_example_diagrams()
    for filename, diagram_info in diagrams.items():
        status_class = "working" if filename in results["success"] else "broken"
        status_text = "✅ Working" if filename in results["success"] else "❌ Broken"

        showcase_content += f"""
            <div class="card">
                <h3>{diagram_info["name"]}<span class="status {status_class}">{status_text}</span></h3>
                <p>Interactive Graphviz diagram with pan/zoom controls and export options.</p>
                <a href="{filename}">View Example →</a>
            </div>"""

    showcase_content += """
        </div>

        <div style="margin-top: 40px; text-align: center; color: #666;">
            <p><strong>🎯 All examples feature:</strong></p>
            <p>🖱️ Pan/zoom controls • ⌨️ Keyboard shortcuts • 💾 Download options • 📋 Copy to clipboard</p>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
            <h3>🕸️ Graphviz Resources</h3>
            <p><strong>Documentation:</strong> <a href="https://graphviz.org/">Graphviz.org</a></p>
            <p><strong>Diagram Types:</strong> Directed Graphs, Undirected Graphs, Flowcharts, Hierarchies, State Machines, Networks, Clusters</p>
            <p><strong>Layouts:</strong> dot, neato, fdp, sfdp, circo, twopi</p>
        </div>
    </div>
</body>
</html>"""

    showcase_path = Path(__file__).parent / "graphviz_showcase.html"
    with open(showcase_path, "w", encoding="utf-8") as f:
        f.write(showcase_content)

    print(f"📋 Generated Graphviz showcase at: {showcase_path}")
    return showcase_path


if __name__ == "__main__":
    results = regenerate_all_graphviz_examples()
    generate_graphviz_showcase(results)
    print(
        "🎉 Graphviz examples complete! Run the server and visit the showcase to see all examples."
    )

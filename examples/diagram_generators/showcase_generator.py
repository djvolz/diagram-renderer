"""
Unified showcase generator for all diagram types.
"""

from pathlib import Path


def generate_unified_showcase(results_by_type, examples_by_type, output_path):
    """Generate unified showcase HTML with all diagram types"""

    # Colors defined in CSS below

    showcase_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Diagram Renderer - Complete Showcase</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        .header h1 {
            font-size: 3em;
            margin: 0 0 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
            margin: 0;
        }

        .stats-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
        }

        .stat-label {
            font-size: 0.9em;
            color: #666;
            margin: 5px 0 0 0;
        }

        .diagram-type-section {
            background: white;
            margin: 30px 0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .section-header {
            padding: 25px 30px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-title {
            font-size: 1.8em;
            font-weight: 600;
            margin: 0;
        }

        .section-stats {
            font-size: 1em;
            opacity: 0.9;
        }

        .examples-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }

        .example-card {
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid #e0e0e0;
        }

        .example-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }

        .card-header {
            padding: 15px 20px;
            border-bottom: 1px solid #e0e0e0;
        }

        .card-title {
            margin: 0 0 8px 0;
            font-weight: 600;
            color: #333;
        }

        .card-description {
            margin: 0;
            color: #666;
            font-size: 0.9em;
        }

        .card-footer {
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .example-link {
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            color: white;
            font-size: 14px;
            font-weight: 500;
            transition: background-color 0.2s;
        }

        .status-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }

        .status-working { background: #d4edda; color: #155724; }
        .status-external { background: #fff3cd; color: #856404; }
        .status-broken { background: #f8d7da; color: #721c24; }

        .mermaid-section .section-header { background: linear-gradient(135deg, #3498db, #2980b9); }
        .mermaid-section .example-link { background: #3498db; }
        .mermaid-section .example-link:hover { background: #2980b9; }

        .plantuml-section .section-header { background: linear-gradient(135deg, #2c3e50, #1a252f); }
        .plantuml-section .example-link { background: #2c3e50; }
        .plantuml-section .example-link:hover { background: #1a252f; }

        .graphviz-section .section-header { background: linear-gradient(135deg, #8B4513, #654321); }
        .graphviz-section .example-link { background: #8B4513; }
        .graphviz-section .example-link:hover { background: #654321; }

        .footer {
            margin-top: 60px;
            text-align: center;
            color: white;
        }

        .footer h3 {
            margin: 0 0 15px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }

        .footer p {
            margin: 10px 0;
            opacity: 0.9;
        }

        .resource-links {
            margin-top: 20px;
        }

        .resource-links a {
            color: #fff;
            text-decoration: none;
            margin: 0 15px;
            padding: 8px 16px;
            background: rgba(255,255,255,0.2);
            border-radius: 6px;
            transition: background 0.2s;
        }

        .resource-links a:hover {
            background: rgba(255,255,255,0.3);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 Complete Diagram Showcase</h1>
        <p>Interactive diagrams with pan/zoom controls, download options, and professional styling</p>
    </div>

    <div class="stats-overview">"""

    # Calculate overall stats
    total_examples = sum(len(examples_by_type[t]) for t in examples_by_type)
    total_working = sum(len(results_by_type[t]["success"]) for t in results_by_type)
    total_failed = sum(len(results_by_type[t]["failed"]) for t in results_by_type)

    showcase_content += f"""
        <div class="stat-card">
            <div class="stat-number">{total_examples}</div>
            <div class="stat-label">Total Examples</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_working}</div>
            <div class="stat-label">Working Examples</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{total_failed}</div>
            <div class="stat-label">External/Unsupported</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{round(total_working / total_examples * 100)}%</div>
            <div class="stat-label">Success Rate</div>
        </div>
    </div>"""

    # Generate sections for each diagram type
    type_info = {
        "mermaid": {
            "icon": "🧜‍♀️",
            "title": "Mermaid Diagrams",
            "desc": "Modern web-friendly diagrams",
        },
        "plantuml": {
            "icon": "🌿",
            "title": "PlantUML Diagrams",
            "desc": "Professional UML diagrams",
        },
        "graphviz": {
            "icon": "🕸️",
            "title": "Graphviz Diagrams",
            "desc": "Technical graphs and networks",
        },
    }

    for diagram_type in ["mermaid", "plantuml", "graphviz"]:
        if diagram_type not in examples_by_type:
            continue

        info = type_info[diagram_type]
        examples = examples_by_type[diagram_type]
        results = results_by_type[diagram_type]

        working_count = len(results["success"])
        total_count = len(examples)

        showcase_content += f"""
    <div class="diagram-type-section {diagram_type}-section">
        <div class="section-header">
            <div>
                <span style="font-size: 1.2em; margin-right: 10px;">{info["icon"]}</span>
                <span class="section-title">{info["title"]}</span>
                <div style="font-size: 0.9em; margin-top: 5px; opacity: 0.9;">{info["desc"]}</div>
            </div>
            <div class="section-stats">{working_count}/{total_count} working</div>
        </div>

        <div class="examples-grid">"""

        for filename, diagram_info in examples.items():
            is_working = filename in results["success"]
            is_external = diagram_info.get("expected_status") == "external"

            status_class = "working" if is_working else ("external" if is_external else "broken")
            status_text = (
                "✅ Working" if is_working else ("⚠️ External" if is_external else "❌ Broken")
            )

            showcase_content += f"""
            <div class="example-card">
                <div class="card-header">
                    <h4 class="card-title">{diagram_info["name"]}</h4>
                    <p class="card-description">Interactive diagram with full pan/zoom controls and export options</p>
                </div>
                <div class="card-footer">
                    <a href="{filename}" class="example-link">View Example →</a>
                    <span class="status-badge status-{status_class}">{status_text}</span>
                </div>
            </div>"""

        showcase_content += """
        </div>
    </div>"""

    showcase_content += """

    <div class="footer">
        <h3>🎯 Every example includes:</h3>
        <p>🖱️ Pan & Zoom Controls • ⌨️ Keyboard Shortcuts • 💾 Download Options • 📋 Copy to Clipboard</p>

        <div class="resource-links">
            <a href="https://mermaid.js.org/">Mermaid Docs</a>
            <a href="https://plantuml.com/">PlantUML Docs</a>
            <a href="https://graphviz.org/">Graphviz Docs</a>
        </div>

        <p style="margin-top: 30px; font-size: 0.9em; opacity: 0.8;">
            All diagrams render locally with no external dependencies • 100% offline capability
        </p>
    </div>
</body>
</html>"""

    # Write the unified showcase
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(showcase_content)

    return output_path


def get_diagram_type_description(diagram_type, working_count, total_count):
    """Get description text for each diagram type section"""
    descriptions = {
        "mermaid": f"Modern web diagrams with {working_count}/{total_count} examples working. Great for flowcharts, sequences, and modern web documentation.",
        "plantuml": f"Professional UML diagrams with {working_count}/{total_count} examples working. Perfect for software architecture and technical documentation.",
        "graphviz": f"Technical graphs with {working_count}/{total_count} examples working. Ideal for networks, dependencies, and complex technical diagrams.",
    }
    return descriptions.get(diagram_type, "Interactive diagrams with pan/zoom controls.")

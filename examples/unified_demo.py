#!/usr/bin/env python3
"""Demo script showing all three diagram renderers with unified template"""

import tempfile
import webbrowser

from diagram_renderer import DiagramRenderer


def create_demo():
    """Create demos for all three diagram types"""

    # Test cases for each diagram type
    test_cases = {
        "mermaid": {
            "name": "Mermaid Flowchart",
            "code": """
            graph TD
                A[🚀 Diagram Renderer] --> B{Choose Type}
                B -->|Interactive| C[🎨 Mermaid]
                B -->|Structured| D[📊 PlantUML]
                B -->|Networks| E[🔗 Graphviz]

                C --> F[Modern UI]
                D --> F
                E --> F

                F --> G[✨ Unified Experience]

                style A fill:#e1f5fe
                style B fill:#f3e5f5
                style C fill:#e8f5e8
                style D fill:#fff3e0
                style E fill:#fce4ec
                style F fill:#f1f8e9
                style G fill:#e0f2f1
            """,
        },
        "plantuml": {
            "name": "PlantUML Sequence",
            "code": """
            @startuml
            actor User
            participant "Diagram Renderer" as DR
            participant "Mermaid" as M
            participant "PlantUML" as P
            participant "Graphviz" as G

            User -> DR: render_diagram_auto(code)
            DR -> DR: detect_diagram_type()

            alt Mermaid detected
                DR -> M: render_html()
                M --> DR: HTML with mermaid.js
            else PlantUML detected
                DR -> P: render_html()
                P -> G: convert to DOT
                P --> DR: HTML with VizJS
            else Graphviz detected
                DR -> G: render_html()
                G --> DR: HTML with VizJS
            end

            DR --> User: Unified HTML template
            @enduml
            """,
        },
        "graphviz": {
            "name": "Graphviz Network",
            "code": """
            digraph Architecture {
                rankdir=TB;
                node [shape=box, style="rounded,filled", fillcolor=white];
                edge [color=gray50];

                subgraph cluster_renderers {
                    label="Diagram Renderers";
                    style=filled;
                    fillcolor=lightgray;

                    Mermaid [fillcolor=lightblue];
                    PlantUML [fillcolor=lightgreen];
                    Graphviz [fillcolor=lightcoral];
                }

                subgraph cluster_output {
                    label="Unified Output";
                    style=filled;
                    fillcolor=lightyellow;

                    "HTML Template" [fillcolor=gold];
                    "Pan/Zoom Controls" [fillcolor=gold];
                    "Download Options" [fillcolor=gold];
                    "Keyboard Shortcuts" [fillcolor=gold];
                }

                User -> DiagramRenderer;
                DiagramRenderer -> {Mermaid PlantUML Graphviz};
                {Mermaid PlantUML Graphviz} -> "HTML Template";
                "HTML Template" -> {"Pan/Zoom Controls" "Download Options" "Keyboard Shortcuts"};
            }
            """,
        },
    }

    renderer = DiagramRenderer()
    results = {}

    print("🚀 Creating demos for all diagram types...\n")

    for diagram_type, info in test_cases.items():
        print(f"🧪 Creating {info['name']} demo...")

        try:
            html_result = renderer.render_diagram_auto(info["code"])

            if html_result:
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=f"-{diagram_type}.html", delete=False
                ) as f:
                    f.write(html_result)
                    temp_path = f.name

                results[diagram_type] = {"name": info["name"], "path": temp_path, "success": True}
                print(f"✅ {info['name']} demo created!")
                print(f"   📂 {temp_path}")
            else:
                print(f"❌ {info['name']} failed - returned None")
                results[diagram_type] = {"success": False}

        except Exception as e:
            print(f"❌ {info['name']} failed: {e}")
            results[diagram_type] = {"success": False}

    # Summary and launch
    print("\n📊 Demo Results:")
    successful_demos = []

    for diagram_type, result in results.items():
        if result.get("success"):
            print(f"   ✅ {result['name']}")
            print(f"     🌐 {result['path']}")
            successful_demos.append(result["path"])
        else:
            print(f"   ❌ {diagram_type.upper()} failed")

    if successful_demos:
        print(f"\n🌐 Opening {len(successful_demos)} demos in browser...")
        for path in successful_demos:
            webbrowser.open(f"file://{path}")

        print("\n✨ All demos use the same unified template with:")
        print("   🎯 Consistent controls and styling")
        print("   🖱️  Pan/zoom with mouse wheel and drag")
        print("   ⌨️  Keyboard shortcuts (+/- zoom, 0 reset, F fullscreen, C copy, ? help)")
        print("   💾 Download PNG and source code")
        print("   📋 Copy to clipboard")
        print("   ❓ Help modal with all shortcuts")

    return results


if __name__ == "__main__":
    results = create_demo()
    print("\n🧹 Remember to delete temp files when done!")
    print(
        "\n🎉 Try the keyboard shortcuts and controls - they work the same across all diagram types!"
    )

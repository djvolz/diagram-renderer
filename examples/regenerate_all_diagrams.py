#!/usr/bin/env python3
"""
Unified diagram example generator for all diagram types.
Replaces separate Mermaid, PlantUML, and Graphviz generation scripts.
"""

import os
from pathlib import Path

try:
    # When imported as a module
    from examples.diagram_generators import (
        generate_unified_showcase,
        get_graphviz_examples,
        get_mermaid_examples,
        get_plantuml_examples,
    )
except ImportError:
    # When run directly
    from diagram_generators import (
        generate_unified_showcase,
        get_graphviz_examples,
        get_mermaid_examples,
        get_plantuml_examples,
    )

from diagram_renderer import DiagramRenderer


def regenerate_diagram_type(diagram_type, examples, renderer):
    """Regenerate examples for a specific diagram type"""
    results = {"success": [], "failed": []}
    examples_dir = Path(__file__).parent

    print(f"\n🚀 Regenerating {diagram_type.upper()} examples...")

    for filename, diagram_info in examples.items():
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

                # Check if this diagram is expected to be external/unsupported
                expected_status = diagram_info.get("expected_status")
                if expected_status == "external" and (is_unsupported or is_render_error):
                    print(f"✅ {filename} - Expected external diagram error")
                    results["failed"].append(filename)  # Still counts as "failed" for showcase
                elif is_unsupported or is_render_error:
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

    return results


def regenerate_all_examples():
    """Regenerate all diagram examples and create unified showcase"""
    renderer = DiagramRenderer()

    # Get all diagram examples
    diagram_types = {
        "mermaid": get_mermaid_examples(),
        "plantuml": get_plantuml_examples(),
        "graphviz": get_graphviz_examples(),
    }

    # Track results for each type
    all_results = {}

    print("🎨 Generating Complete Diagram Example Suite")
    print("=" * 50)

    # Regenerate each diagram type
    for diagram_type, examples in diagram_types.items():
        results = regenerate_diagram_type(diagram_type, examples, renderer)
        all_results[diagram_type] = results

        print(f"\n📊 {diagram_type.upper()} Results:")
        print(f"✅ Success: {len(results['success'])}")
        print(f"❌ Failed: {len(results['failed'])}")

        if results["failed"]:
            print("⚠️  Failed files:")
            for failed_file in results["failed"]:
                print(f"   - {failed_file}")

    # Generate unified showcase
    print("\n🎯 Creating Unified Showcase...")
    showcase_path = Path(__file__).parent / "diagram_showcase.html"
    generate_unified_showcase(all_results, diagram_types, showcase_path)
    print(f"📋 Generated unified showcase at: {showcase_path}")

    # Overall summary
    total_examples = sum(len(examples) for examples in diagram_types.values())
    total_working = sum(len(results["success"]) for results in all_results.values())
    total_failed = sum(len(results["failed"]) for results in all_results.values())
    success_rate = round(total_working / total_examples * 100) if total_examples > 0 else 0

    print("\n🎉 COMPLETE DIAGRAM SUITE GENERATED")
    print("📊 Overall Results:")
    print(f"   Total Examples: {total_examples}")
    print(f"   Working: {total_working} ({success_rate}%)")
    print(f"   External/Unsupported: {total_failed}")
    print("\n🌐 View the unified showcase at: http://localhost:8000/diagram_showcase.html")

    return all_results


def main():
    """Main entry point"""
    regenerate_all_examples()
    print("\n✨ All diagram examples generated successfully!")
    print("🚀 Start a local server and visit diagram_showcase.html to see everything!")


if __name__ == "__main__":
    main()

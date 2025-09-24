#!/usr/bin/env python3
"""
Baseline image generator for visual regression testing.
Captures reference screenshots of all working diagram examples.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import diagram_generators
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from screenshot_capture import DiagramScreenshotCapture

from examples.diagram_generators import (
    get_graphviz_examples,
    get_mermaid_examples,
    get_plantuml_examples,
)


def filter_working_examples(examples: dict, results: dict) -> dict:
    """Filter examples to only include those that are working"""
    working_examples = {}
    success_list = results.get("success", [])

    for filename, diagram_info in examples.items():
        # Only include examples that are successfully rendering
        if filename in success_list:
            working_examples[filename] = diagram_info
        else:
            print(f"⚠️ Skipping {filename} - not in success list")

    return working_examples


def generate_baselines():
    """Generate baseline reference images for all working examples"""

    # Setup paths
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    baselines_dir = Path(__file__).parent / "baselines"

    # Ensure baselines directory exists
    baselines_dir.mkdir(exist_ok=True, parents=True)

    print("🎯 Generating Visual Regression Baselines")
    print("=" * 50)

    # Generate HTML files for all examples
    print("🔄 Generating HTML files for examples...")
    from diagram_renderer import DiagramRenderer

    renderer = DiagramRenderer()

    # Track which examples work
    all_results = {
        "mermaid": {"success": []},
        "plantuml": {"success": []},
        "graphviz": {"success": []},
    }

    for diagram_type, get_examples_func in [
        ("mermaid", get_mermaid_examples),
        ("plantuml", get_plantuml_examples),
        ("graphviz", get_graphviz_examples),
    ]:
        examples = get_examples_func()
        type_dir = examples_dir / diagram_type
        type_dir.mkdir(exist_ok=True, parents=True)

        for filename, diagram_info in examples.items():
            try:
                # Generate HTML
                html_content = renderer.render_diagram_auto(diagram_info["code"])
                if html_content:
                    # Save HTML file
                    html_path = examples_dir / filename
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    all_results[diagram_type]["success"].append(filename)
                    print(f"  ✅ Generated {filename}")
            except Exception as e:
                print(f"  ❌ Failed to generate {filename}: {e}")

    # Get working examples only
    examples_by_type = {
        "mermaid": filter_working_examples(get_mermaid_examples(), all_results["mermaid"]),
        "plantuml": filter_working_examples(get_plantuml_examples(), all_results["plantuml"]),
        "graphviz": filter_working_examples(get_graphviz_examples(), all_results["graphviz"]),
    }

    print("\n📊 Examples to capture:")
    for diagram_type, examples in examples_by_type.items():
        print(f"  {diagram_type}: {len(examples)} working examples")

    # Capture screenshots (use port 8003 to avoid conflicts)
    capturer = DiagramScreenshotCapture(server_port=8003)

    if not capturer.start_local_server(examples_dir):
        print("❌ Failed to start local server")
        return False

    try:
        # Capture all screenshots to baselines directory
        results = capturer.capture_all_examples(examples_by_type, baselines_dir)

        # Summary
        total_captured = sum(len(r["success"]) for r in results.values())
        total_examples = sum(len(examples) for examples in examples_by_type.items())

        print("\n🎉 Baseline Generation Complete!")
        print(f"📸 Captured: {total_captured} reference images")
        print(f"📁 Location: {baselines_dir}")

        if total_captured > 0:
            print("\n💡 Usage:")
            print(f"   - Reference images are now stored in {baselines_dir}")
            print("   - Run visual tests with: python tests/visual/visual_test_runner.py")
            print("   - Update baselines when expected: python tests/visual/baseline_generator.py")

        return total_captured > 0

    finally:
        capturer.stop_local_server()


if __name__ == "__main__":
    success = generate_baselines()
    if not success:
        print("❌ Baseline generation failed")
        sys.exit(1)
    print("✅ Baseline generation successful!")

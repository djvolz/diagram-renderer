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

    print("🎯 Generating Visual Regression Baselines")
    print("=" * 50)

    # First, regenerate all examples to ensure they're current
    print("🔄 Regenerating all examples to ensure current...")
    try:
        from examples.regenerate_all_diagrams import regenerate_all_examples

        all_results = regenerate_all_examples()
    except Exception as e:
        print(f"❌ Error regenerating examples: {e}")
        return False

    # Get working examples only
    examples_by_type = {
        "mermaid": filter_working_examples(get_mermaid_examples(), all_results["mermaid"]),
        "plantuml": filter_working_examples(get_plantuml_examples(), all_results["plantuml"]),
        "graphviz": filter_working_examples(get_graphviz_examples(), all_results["graphviz"]),
    }

    print("\n📊 Examples to capture:")
    for diagram_type, examples in examples_by_type.items():
        print(f"  {diagram_type}: {len(examples)} working examples")

    # Capture screenshots
    capturer = DiagramScreenshotCapture()

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

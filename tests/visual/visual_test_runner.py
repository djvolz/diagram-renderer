#!/usr/bin/env python3
"""
Visual regression test runner for diagram examples.
Automates the process of capturing screenshots and comparing against baselines.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Add the parent directory to the path to import diagram_generators
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from examples.diagram_generators import (
    get_graphviz_examples,
    get_mermaid_examples,
    get_plantuml_examples,
)

try:
    from .image_comparison import ImageComparator
    from .screenshot_capture import DiagramScreenshotCapture
except ImportError:
    # When running directly (not as a module)
    from image_comparison import ImageComparator
    from screenshot_capture import DiagramScreenshotCapture


class VisualRegressionTester:
    """Main visual regression testing orchestrator"""

    def __init__(self, similarity_threshold: float = 0.95, server_port: int = 8004):
        self.similarity_threshold = similarity_threshold
        self.server_port = server_port
        self.visual_dir = Path(__file__).parent
        self.baselines_dir = self.visual_dir / "baselines"
        self.artifacts_dir = self.visual_dir / "artifacts"
        self.current_dir = self.artifacts_dir / "current"
        self.diff_dir = self.artifacts_dir / "diffs"

        # Ensure directories exist
        for directory in [self.current_dir, self.diff_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        self.capturer = DiagramScreenshotCapture(server_port)
        self.comparator = ImageComparator(similarity_threshold)

    def run_visual_tests(
        self, regenerate_examples: bool = True, capture_new_screenshots: bool = True
    ) -> dict:
        """
        Run complete visual regression test suite.

        Args:
            regenerate_examples: Whether to regenerate HTML examples first
            capture_new_screenshots: Whether to capture new screenshots

        Returns:
            Comprehensive test results
        """
        print("🎯 Running Visual Regression Tests")
        print("=" * 40)

        # Step 1: Get example definitions
        examples_by_type = {
            "mermaid": get_mermaid_examples(),
            "plantuml": get_plantuml_examples(),
            "graphviz": get_graphviz_examples(),
        }

        # Step 2: Regenerate examples if requested
        example_results = None
        if regenerate_examples:
            print("🔄 Generating HTML files for diagram examples...")
            try:
                from diagram_renderer import DiagramRenderer

                renderer = DiagramRenderer()
                examples_dir = Path(__file__).parent.parent.parent / "examples"

                example_results = {
                    "mermaid": {"success": []},
                    "plantuml": {"success": []},
                    "graphviz": {"success": []},
                }

                # Generate HTML files
                for diagram_type, examples in examples_by_type.items():
                    for filename, diagram_info in examples.items():
                        try:
                            html_content = renderer.render_diagram_auto(diagram_info["code"])
                            if html_content:
                                html_path = examples_dir / filename
                                with open(html_path, "w", encoding="utf-8") as f:
                                    f.write(html_content)
                                example_results[diagram_type]["success"].append(filename)
                        except Exception:
                            pass
            except Exception as e:
                print(f"❌ Failed to generate examples: {e}")
                return {"error": "Failed to generate examples"}

        # Step 3: Capture current screenshots if requested
        if capture_new_screenshots:
            if not self._capture_current_screenshots(examples_by_type):
                return {"error": "Failed to capture screenshots"}

        # Step 4: Compare against baselines
        comparison_results = self._compare_all_against_baselines(examples_by_type)

        # Step 5: Generate test report
        report = self._generate_test_report(comparison_results, example_results)

        return report

    def _capture_current_screenshots(self, examples_by_type: dict) -> bool:
        """Capture current screenshots for comparison"""
        examples_dir = Path(__file__).parent.parent.parent / "examples"

        if not self.capturer.start_local_server(examples_dir):
            return False

        try:
            print("📸 Capturing current screenshots...")
            results = self.capturer.capture_all_examples(examples_by_type, self.current_dir)

            total_captured = sum(len(r["success"]) for r in results.values())
            print(f"✅ Captured {total_captured} screenshots")
            return total_captured > 0

        finally:
            self.capturer.stop_local_server()

    def _compare_all_against_baselines(self, examples_by_type: dict) -> dict:
        """Compare all current screenshots against baselines"""
        overall_results = {
            "passed": [],
            "failed": [],
            "missing_baseline": [],
            "comparison_details": {},
        }

        for diagram_type, examples in examples_by_type.items():
            print(f"\n🔍 Comparing {diagram_type.upper()} examples...")

            baseline_type_dir = self.baselines_dir / diagram_type
            current_type_dir = self.current_dir / diagram_type

            if not baseline_type_dir.exists():
                print(f"⚠️ No baseline directory for {diagram_type}")
                continue

            results = self.comparator.compare_diagram_examples(
                baseline_type_dir, current_type_dir, self.diff_dir, examples
            )

            # Aggregate results
            overall_results["passed"].extend(results["passed"])
            overall_results["failed"].extend(results["failed"])
            overall_results["missing_baseline"].extend(results["missing_baseline"])
            overall_results["comparison_details"].update(results["comparison_details"])

            print(
                f"📊 {diagram_type}: {len(results['passed'])} passed, {len(results['failed'])} failed"
            )

        return overall_results

    def _generate_test_report(
        self, comparison_results: dict, example_results: Optional[dict] = None
    ) -> dict:
        """Generate comprehensive test report"""
        timestamp = datetime.now().isoformat()

        # Calculate summary statistics
        total_tests = len(comparison_results["passed"]) + len(comparison_results["failed"])
        pass_rate = (
            (len(comparison_results["passed"]) / total_tests) * 100 if total_tests > 0 else 0
        )

        report = {
            "timestamp": timestamp,
            "summary": {
                "total_tests": total_tests,
                "passed": len(comparison_results["passed"]),
                "failed": len(comparison_results["failed"]),
                "missing_baseline": len(comparison_results["missing_baseline"]),
                "pass_rate": pass_rate,
                "threshold": self.similarity_threshold,
            },
            "failed_tests": comparison_results["failed"],
            "missing_baselines": comparison_results["missing_baseline"],
            "detailed_results": comparison_results["comparison_details"],
        }

        # Add example generation results if available
        if example_results:
            report["example_generation"] = example_results

        # Save report
        report_path = self.artifacts_dir / f"visual_test_report_{timestamp.replace(':', '-')}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        # Print summary
        print("\n📋 Visual Regression Test Results")
        print(f"   Tests: {total_tests}")
        print(f"   Passed: {len(comparison_results['passed'])} ({pass_rate:.1f}%)")
        print(f"   Failed: {len(comparison_results['failed'])}")

        if comparison_results["failed"]:
            print("\n❌ Failed Tests:")
            for failed_test in comparison_results["failed"]:
                details = comparison_results["comparison_details"].get(failed_test, {})
                similarity = details.get("similarity", 0)
                print(f"   - {failed_test} (similarity: {similarity:.3f})")

        if comparison_results["missing_baseline"]:
            print("\n⚠️ Missing Baselines:")
            for missing in comparison_results["missing_baseline"]:
                print(f"   - {missing}")

        print(f"\n📄 Detailed report: {report_path}")

        return report


def main():
    """Main entry point for visual regression testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Visual regression testing for diagram examples")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.95,
        help="Similarity threshold (0.0-1.0, default: 0.95)",
    )
    parser.add_argument("--skip-regen", action="store_true", help="Skip regenerating examples")
    parser.add_argument(
        "--skip-capture", action="store_true", help="Skip capturing new screenshots (use existing)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Local server port (default: 8000)")

    args = parser.parse_args()

    # Check if baselines exist
    baselines_dir = Path(__file__).parent / "baselines"
    if not any(baselines_dir.glob("*/*.png")):
        print("⚠️ No baseline images found!")
        print("   Run: python tests/visual/baseline_generator.py")
        print("   This will generate reference images for all working examples.")
        return False

    # Run visual tests
    tester = VisualRegressionTester(args.threshold, args.port)

    results = tester.run_visual_tests(
        regenerate_examples=not args.skip_regen, capture_new_screenshots=not args.skip_capture
    )

    if "error" in results:
        print(f"❌ Visual testing failed: {results['error']}")
        return False

    # Exit with error code if any tests failed
    failed_count = results["summary"]["failed"]
    if failed_count > 0:
        print(f"\n💥 {failed_count} visual regression test(s) failed!")
        return False
    else:
        print("\n✅ All visual regression tests passed!")
        return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

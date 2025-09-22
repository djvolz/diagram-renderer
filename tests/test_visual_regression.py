"""
Visual regression tests for diagram examples.
Integrates visual testing into the pytest test suite.
"""

from pathlib import Path

import pytest

from tests.visual.visual_test_runner import VisualRegressionTester


class TestVisualRegression:
    """Visual regression tests for diagram rendering"""

    @pytest.fixture(scope="class")
    def visual_tester(self):
        """Create visual regression tester instance"""
        return VisualRegressionTester(similarity_threshold=0.95)

    @pytest.fixture(scope="class")
    def baselines_exist(self):
        """Check if baseline images exist"""
        baselines_dir = Path(__file__).parent / "visual" / "baselines"
        return any(baselines_dir.glob("*/*.png"))

    @pytest.mark.visual
    def test_visual_regression_mermaid(self, visual_tester, baselines_exist):
        """Test visual regression for Mermaid diagrams"""
        if not baselines_exist:
            pytest.skip("No baseline images found. Run: python tests/visual/baseline_generator.py")

        # Run visual tests (skip regeneration since pytest handles dependencies)
        results = visual_tester.run_visual_tests(
            regenerate_examples=False, capture_new_screenshots=True
        )

        assert "error" not in results
        assert results["summary"]["failed"] == 0, (
            f"Visual regression failures: {results['failed_tests']}"
        )
        assert results["summary"]["passed"] > 0, "No visual tests passed"

    @pytest.mark.visual
    @pytest.mark.integration
    def test_visual_regression_full_suite(self, visual_tester, baselines_exist):
        """Test complete visual regression suite for all diagram types"""
        if not baselines_exist:
            pytest.skip("No baseline images found. Run: python tests/visual/baseline_generator.py")

        # Run complete visual regression test
        results = visual_tester.run_visual_tests(
            regenerate_examples=True,  # Full integration test
            capture_new_screenshots=True,
        )

        assert "error" not in results

        # Verify we have reasonable coverage
        total_tests = results["summary"]["total_tests"]
        passed_tests = results["summary"]["passed"]
        pass_rate = results["summary"]["pass_rate"]

        assert total_tests >= 20, f"Expected at least 20 visual tests, got {total_tests}"
        assert pass_rate >= 90, f"Visual regression pass rate too low: {pass_rate}%"

        # If any tests failed, provide detailed failure information
        if results["summary"]["failed"] > 0:
            failed_details = []
            for failed_test in results["failed_tests"]:
                details = results["detailed_results"].get(failed_test, {})
                similarity = details.get("similarity", 0)
                failed_details.append(f"{failed_test} (similarity: {similarity:.3f})")

            pytest.fail("Visual regression failures:\\n" + "\\n".join(failed_details))

    @pytest.mark.visual
    def test_baseline_coverage(self):
        """Test that we have baseline images for all working examples"""
        # Check that baseline directory exists and contains images
        baselines_dir = Path(__file__).parent / "visual" / "baselines"

        if not baselines_dir.exists():
            pytest.skip("No baselines directory")

        # Count baseline images
        baseline_count = len(list(baselines_dir.glob("*/*.png")))

        # We should have at least some baselines
        assert baseline_count > 20, f"Expected at least 20 baseline images, found {baseline_count}"

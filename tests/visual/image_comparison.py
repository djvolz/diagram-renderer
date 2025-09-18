#!/usr/bin/env python3
"""
Image comparison utilities for visual regression testing.
Compares current screenshots against baseline images to detect changes.
"""

import hashlib
from pathlib import Path
from typing import Optional


class ImageComparator:
    """Compares images for visual regression testing"""

    def __init__(self, similarity_threshold: float = 0.95):
        """
        Initialize image comparator.

        Args:
            similarity_threshold: Minimum similarity score to consider images matching
        """
        self.similarity_threshold = similarity_threshold

    def calculate_image_hash(self, image_path: Path) -> Optional[str]:
        """Calculate MD5 hash of image file for quick comparison"""
        try:
            with open(image_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"❌ Error calculating hash for {image_path}: {e}")
            return None

    def images_identical_by_hash(self, image1_path: Path, image2_path: Path) -> bool:
        """Quick check if images are identical using MD5 hash"""
        hash1 = self.calculate_image_hash(image1_path)
        hash2 = self.calculate_image_hash(image2_path)
        return hash1 is not None and hash1 == hash2

    def compare_images_pillow(
        self, baseline_path: Path, current_path: Path, diff_output_path: Optional[Path] = None
    ) -> dict:
        """
        Compare images using Pillow (basic comparison).
        Returns comparison results with similarity score.
        """
        try:
            import numpy as np
            from PIL import Image, ImageDraw, ImageFont

            # Load images
            baseline = Image.open(baseline_path).convert("RGB")
            current = Image.open(current_path).convert("RGB")

            # Resize to same dimensions if needed
            if baseline.size != current.size:
                current = current.resize(baseline.size, Image.Resampling.LANCZOS)

            # Convert to numpy arrays for comparison
            baseline_array = np.array(baseline)
            current_array = np.array(current)

            # Calculate pixel differences
            diff_array = np.abs(baseline_array.astype(int) - current_array.astype(int))

            # Calculate similarity metrics
            total_pixels = baseline_array.size
            different_pixels = np.count_nonzero(diff_array)
            similarity = 1.0 - (different_pixels / total_pixels)

            # Generate visual diff if requested
            if diff_output_path:
                self._generate_visual_diff(baseline, current, diff_array, diff_output_path)

            return {
                "similarity": similarity,
                "different_pixels": different_pixels,
                "total_pixels": total_pixels,
                "passed": similarity >= self.similarity_threshold,
                "baseline_size": baseline.size,
                "current_size": current.size,
            }

        except ImportError:
            print("📦 Pillow not available for image comparison")
            return {"error": "Pillow not available"}
        except Exception as e:
            print(f"❌ Image comparison failed: {e}")
            return {"error": str(e)}

    def _generate_visual_diff(self, baseline, current, diff_array, output_path: Path):
        """Generate visual diff image highlighting differences"""
        try:
            import numpy as np
            from PIL import Image

            # Create diff visualization
            diff_threshold = 30  # Minimum difference to highlight

            # Create diff image (red highlights where images differ)
            diff_highlight = np.zeros_like(diff_array)
            significant_diffs = np.any(diff_array > diff_threshold, axis=2)
            diff_highlight[significant_diffs] = [255, 0, 0]  # Red for differences

            # Blend diff highlights with current image
            current_array = np.array(current)
            alpha = 0.3
            blended = current_array * (1 - alpha) + diff_highlight * alpha

            # Save diff image
            diff_image = Image.fromarray(blended.astype(np.uint8))
            diff_image.save(output_path)

        except Exception as e:
            print(f"⚠️ Could not generate visual diff: {e}")

    def compare_diagram_examples(
        self, baseline_dir: Path, current_dir: Path, diff_dir: Path, examples: dict
    ) -> dict:
        """
        Compare all examples of a diagram type against baselines.

        Returns:
            Dict with comparison results for each example
        """
        results = {
            "passed": [],
            "failed": [],
            "missing_baseline": [],
            "missing_current": [],
            "comparison_details": {},
        }

        for filename, diagram_info in examples.items():
            screenshot_name = filename.replace(".html", ".png")
            baseline_path = baseline_dir / screenshot_name
            current_path = current_dir / screenshot_name
            diff_path = diff_dir / f"diff_{screenshot_name}"

            if not baseline_path.exists():
                results["missing_baseline"].append(filename)
                print(f"⚠️ No baseline for {screenshot_name}")
                continue

            if not current_path.exists():
                results["missing_current"].append(filename)
                print(f"⚠️ No current screenshot for {screenshot_name}")
                continue

            # Quick hash comparison first
            if self.images_identical_by_hash(baseline_path, current_path):
                results["passed"].append(filename)
                results["comparison_details"][filename] = {
                    "method": "hash",
                    "similarity": 1.0,
                    "identical": True,
                }
                print(f"✅ {screenshot_name} - Identical")
                continue

            # Detailed comparison for non-identical images
            comparison = self.compare_images_pillow(baseline_path, current_path, diff_path)
            results["comparison_details"][filename] = comparison

            if comparison.get("passed", False):
                results["passed"].append(filename)
                print(f"✅ {screenshot_name} - Similar ({comparison.get('similarity', 0):.3f})")
            else:
                results["failed"].append(filename)
                similarity = comparison.get("similarity", 0)
                print(
                    f"❌ {screenshot_name} - Failed ({similarity:.3f} < {self.similarity_threshold})"
                )

        return results


def main():
    """Standalone image comparison utility"""
    visual_dir = Path(__file__).parent
    baselines_dir = visual_dir / "baselines"
    current_dir = visual_dir / "artifacts" / "current"
    diff_dir = visual_dir / "artifacts" / "diffs"

    if not current_dir.exists():
        print("❌ No current screenshots found. Run screenshot capture first.")
        return

    comparator = ImageComparator()

    # Compare each diagram type
    for diagram_type in ["mermaid", "plantuml", "graphviz"]:
        baseline_type_dir = baselines_dir / diagram_type
        current_type_dir = current_dir / diagram_type

        if not baseline_type_dir.exists():
            print(f"⚠️ No baselines for {diagram_type}")
            continue

        if not current_type_dir.exists():
            print(f"⚠️ No current screenshots for {diagram_type}")
            continue

        print(f"\n🔍 Comparing {diagram_type.upper()} examples...")

        # Get example files
        current_screenshots = list(current_type_dir.glob("*.png"))
        example_dict = {f.stem + ".html": {} for f in current_screenshots}

        results = comparator.compare_diagram_examples(
            baseline_type_dir, current_type_dir, diff_dir, example_dict
        )

        print(
            f"📊 {diagram_type}: {len(results['passed'])} passed, {len(results['failed'])} failed"
        )


if __name__ == "__main__":
    main()

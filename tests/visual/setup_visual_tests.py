#!/usr/bin/env python3
"""
Setup script for visual regression testing.
Installs dependencies and generates initial baseline images.
"""

import subprocess
import sys
from pathlib import Path


def install_visual_dependencies():
    """Install required dependencies for visual testing"""
    print("📦 Installing visual regression testing dependencies...")

    try:
        # Install Python dependencies
        subprocess.run(
            [
                "uv",
                "add",
                "--group",
                "dev",
                "pillow>=10.0.0",
                "numpy>=1.24.0",
                "playwright>=1.40.0",
            ],
            check=True,
        )

        # Install Playwright browsers
        subprocess.run(["uv", "run", "playwright", "install", "chromium"], check=True)

        print("✅ Dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ uv not found. Please install uv first: https://docs.astral.sh/uv/")
        return False


def generate_initial_baselines():
    """Generate initial baseline images"""
    print("\n🎯 Generating initial baseline images...")

    try:
        # Import and run baseline generator
        from baseline_generator import generate_baselines

        success = generate_baselines()
        if success:
            print("✅ Baseline images generated successfully")
            return True
        else:
            print("❌ Failed to generate baseline images")
            return False

    except Exception as e:
        print(f"❌ Error generating baselines: {e}")
        return False


def run_initial_visual_test():
    """Run initial visual test to verify setup"""
    print("\n🧪 Running initial visual regression test...")

    try:
        from visual_test_runner import VisualRegressionTester

        tester = VisualRegressionTester()
        results = tester.run_visual_tests()

        if "error" not in results:
            passed = results["summary"]["passed"]
            total = results["summary"]["total_tests"]
            print(f"✅ Initial test successful: {passed}/{total} examples passed")
            return True
        else:
            print(f"❌ Initial test failed: {results['error']}")
            return False

    except Exception as e:
        print(f"❌ Error running initial test: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Visual Regression Testing")
    print("=" * 45)

    # Check if we're in the right directory
    if not Path("diagram_renderer").exists():
        print("❌ Please run this script from the project root directory")
        return False

    # Step 1: Install dependencies
    if not install_visual_dependencies():
        return False

    # Step 2: Generate baselines
    if not generate_initial_baselines():
        print("⚠️ Could not generate baseline images")
        print("   You can try manually: python tests/visual/baseline_generator.py")
        return False

    # Step 3: Run initial test
    if not run_initial_visual_test():
        print("⚠️ Initial visual test had issues")
        print("   Check the setup and try: python tests/visual/visual_test_runner.py")
        return False

    print("\n🎉 Visual Regression Testing Setup Complete!")
    print("\n💡 Usage:")
    print("   • Run visual tests: python tests/visual/visual_test_runner.py")
    print("   • Update baselines: python tests/visual/baseline_generator.py")
    print("   • Run via pytest: pytest -m visual")
    print("   • Documentation: tests/visual/README.md")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    print("✨ Setup successful!")

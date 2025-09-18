#!/usr/bin/env python3
"""
Screenshot capture utility for visual regression testing.
Uses browser automation to capture diagram screenshots consistently.
"""

import asyncio
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional


class DiagramScreenshotCapture:
    """Captures screenshots of diagram examples for visual regression testing"""

    def __init__(self, server_port: int = 8000):
        self.server_port = server_port
        self.base_url = f"http://localhost:{server_port}"
        self.server_process = None

    def start_local_server(self, examples_dir: Path):
        """Start local HTTP server for serving examples"""
        try:
            print(f"🚀 Starting local server on port {self.server_port}...")
            self.server_process = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(self.server_port)],
                cwd=examples_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Give server time to start
            time.sleep(2)
            print(f"✅ Server started at {self.base_url}")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False

    def stop_local_server(self):
        """Stop the local HTTP server"""
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("🛑 Server stopped")
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                print("🔪 Server forcefully killed")
            except Exception as e:
                print(f"⚠️ Error stopping server: {e}")

    def capture_screenshot_playwright(
        self, url: str, output_path: Path, wait_for_diagram: bool = True
    ) -> bool:
        """
        Capture screenshot using Playwright (if available).
        Falls back to other methods if Playwright not installed.
        """
        try:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()

                # Set viewport for consistent screenshots
                page.set_viewport_size({"width": 1200, "height": 800})

                # Navigate to diagram
                page.goto(url)

                if wait_for_diagram:
                    # Wait for diagram to load (look for pan/zoom controls)
                    try:
                        page.wait_for_selector(
                            '[class*="zoom-controls"], [class*="control-btn"]', timeout=10000
                        )
                        # Additional wait for diagram rendering
                        page.wait_for_timeout(2000)
                    except:
                        print(f"⚠️ Diagram controls not found for {url}")

                # Take screenshot
                page.screenshot(path=str(output_path))
                browser.close()
                return True

        except ImportError:
            print("📦 Playwright not available, falling back to browser MCP...")
            return False
        except Exception as e:
            print(f"❌ Playwright screenshot failed: {e}")
            return False

    def capture_screenshot_mcp(self, url: str, output_path: Path) -> bool:
        """
        Capture screenshot using browser MCP (if available).
        This is our fallback method.
        """
        try:
            # This would integrate with the existing browser MCP
            # For now, return False to indicate it needs implementation
            print("🔧 Browser MCP integration needed")
            return False
        except Exception as e:
            print(f"❌ MCP screenshot failed: {e}")
            return False

    def capture_diagram_screenshot(
        self, filename: str, output_path: Path, diagram_type: str = "unknown"
    ) -> bool:
        """
        Capture screenshot of a specific diagram file.
        Tries multiple capture methods until one succeeds.
        """
        url = f"{self.base_url}/{filename}"
        print(f"📸 Capturing {diagram_type}: {filename}")

        # Try Playwright first
        if self.capture_screenshot_playwright(url, output_path):
            return True

        # Fallback to MCP
        if self.capture_screenshot_mcp(url, output_path):
            return True

        print(f"❌ Failed to capture screenshot for {filename}")
        return False

    def capture_all_examples(self, examples_by_type: dict, output_dir: Path) -> dict:
        """
        Capture screenshots for all diagram examples.

        Args:
            examples_by_type: Dict with keys like "mermaid", "plantuml", "graphviz"
            output_dir: Base directory for storing screenshots

        Returns:
            Dict tracking success/failure for each diagram type
        """
        results = {}

        for diagram_type, examples in examples_by_type.items():
            print(f"\n🎯 Capturing {diagram_type.upper()} examples...")
            type_dir = output_dir / diagram_type
            type_dir.mkdir(exist_ok=True)

            type_results = {"success": [], "failed": []}

            for filename, diagram_info in examples.items():
                # Create safe filename for screenshot
                screenshot_name = filename.replace(".html", ".png")
                screenshot_path = type_dir / screenshot_name

                success = self.capture_diagram_screenshot(filename, screenshot_path, diagram_type)

                if success and screenshot_path.exists():
                    type_results["success"].append(filename)
                    print(f"  ✅ {screenshot_name}")
                else:
                    type_results["failed"].append(filename)
                    print(f"  ❌ {screenshot_name}")

            results[diagram_type] = type_results
            print(f"📊 {diagram_type}: {len(type_results['success'])}/{len(examples)} captured")

        return results


def main():
    """Main function for standalone screenshot capture"""
    from diagram_generators import (
        get_graphviz_examples,
        get_mermaid_examples,
        get_plantuml_examples,
    )

    # Get all examples
    examples_by_type = {
        "mermaid": get_mermaid_examples(),
        "plantuml": get_plantuml_examples(),
        "graphviz": get_graphviz_examples(),
    }

    # Setup paths
    examples_dir = Path(__file__).parent.parent.parent / "examples"
    output_dir = Path(__file__).parent / "artifacts" / "current"

    # Capture screenshots
    capturer = DiagramScreenshotCapture()

    if capturer.start_local_server(examples_dir):
        try:
            results = capturer.capture_all_examples(examples_by_type, output_dir)

            # Print summary
            total_success = sum(len(r["success"]) for r in results.values())
            total_examples = sum(len(examples) for examples in examples_by_type.values())

            print("\n📊 Screenshot Capture Complete:")
            print(f"✅ Success: {total_success}/{total_examples}")

            for diagram_type, type_results in results.items():
                if type_results["failed"]:
                    print(f"❌ {diagram_type} failures: {type_results['failed']}")

        finally:
            capturer.stop_local_server()
    else:
        print("❌ Could not start server for screenshot capture")


if __name__ == "__main__":
    main()

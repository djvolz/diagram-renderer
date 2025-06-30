#!/usr/bin/env python3
"""Simple script to run the Streamlit dashboard."""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    try:
        dashboard_path = Path(__file__).parent / "dashboard.py"
        subprocess.run([
            "uv", "run", "--extra", "dashboard", 
            "python", "-m", "streamlit", "run", 
            str(dashboard_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running dashboard: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
import subprocess
import sys
import click
from diagram import DiagramRenderer

@click.group()
def cli():
    """Diagram Renderer CLI - Render Mermaid, PlantUML, and Graphviz diagrams"""
    pass

@cli.command()
def dashboard():
    """Launch the Streamlit dashboard"""
    try:
        subprocess.run(["uv", "run", "streamlit", "run", "dashboard.py"], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running Streamlit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()

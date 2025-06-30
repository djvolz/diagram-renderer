#!/usr/bin/env python3
"""
Standalone CLI utility for diagram rendering.
Demonstrates how to use the diagram library without Streamlit.
"""

try:
    import click
except ImportError:
    print("Error: 'click' is required for the CLI. Install with:")
    print("  uv add diagram-renderer[cli]")
    print("  # or")
    print("  pip install diagram-renderer[cli]")
    exit(1)

import sys
import subprocess
import webbrowser
import threading
import time
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

from . import DiagramRenderer


@click.group()
@click.version_option(version="0.1.0", prog_name="diagram-renderer")
def cli():
    """
    Diagram Renderer CLI - Render Mermaid, PlantUML, and Graphviz diagrams
    
    A standalone command-line utility for converting diagram code to HTML with
    interactive zoom/pan controls and PNG export functionality.
    """
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('-o', '--output', type=click.Path(path_type=Path), 
              help='Output HTML file path (default: input_file.html)')
@click.option('--detect-only', is_flag=True, 
              help='Only detect diagram type, don\'t render')
@click.option('--verbose', '-v', is_flag=True, 
              help='Verbose output')
def render(input_file, output, detect_only, verbose):
    """
    Render diagram from a file to HTML.
    
    INPUT_FILE: Path to file containing diagram code (supports .txt, .md, .mmd, .puml, .dot files)
    
    Examples:
    \b
        diagram-renderer render flowchart.mmd
        diagram-renderer render diagram.txt -o output.html
        diagram-renderer render --detect-only input.md
    """
    try:
        # Read input file
        if verbose:
            click.echo(f"Reading input file: {input_file}")
        
        diagram_code = input_file.read_text(encoding='utf-8')
        
        # Initialize renderer
        renderer = DiagramRenderer()
        
        # Detect diagram type
        detected_type = renderer.detect_diagram_type(diagram_code)
        
        if verbose or detect_only:
            if detected_type:
                click.echo(f"Detected diagram type: {detected_type.upper()}")
            else:
                click.echo("No specific diagram type detected, will try Mermaid as fallback")
        
        if detect_only:
            return
        
        # Render diagram
        if verbose:
            click.echo("Rendering diagram...")
        
        html_content = renderer.render_diagram_auto(diagram_code)
        
        if html_content is None:
            click.echo("❌ Failed to render diagram", err=True)
            sys.exit(1)
        
        # Determine output file
        if output is None:
            output = input_file.with_suffix('.html')
        
        # Write output
        output.write_text(html_content, encoding='utf-8')
        
        click.echo(f"✅ Diagram rendered successfully: {output}")
        
        if verbose:
            click.echo(f"Output file size: {output.stat().st_size} bytes")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('diagram_code')
@click.option('-t', '--type', 'diagram_type', 
              type=click.Choice(['mermaid', 'plantuml', 'graphviz'], case_sensitive=False),
              help='Force specific diagram type')
@click.option('-o', '--output', type=click.Path(path_type=Path), 
              default='diagram.html', help='Output HTML file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def quick(diagram_code, diagram_type, output, verbose):
    """
    Quick render diagram code directly from command line.
    
    DIAGRAM_CODE: Diagram code as a string
    
    Examples:
    \b
        diagram-renderer quick "graph TD; A-->B"
        diagram-renderer quick "@startuml; A->B; @enduml" --type plantuml
        diagram-renderer quick "digraph G { A -> B; }" -o my-graph.html
    """
    try:
        renderer = DiagramRenderer()
        
        if verbose:
            if diagram_type:
                click.echo(f"Using forced diagram type: {diagram_type.upper()}")
            else:
                detected = renderer.detect_diagram_type(diagram_code)
                if detected:
                    click.echo(f"Detected diagram type: {detected.upper()}")
                else:
                    click.echo("No specific type detected, using Mermaid as fallback")
        
        if verbose:
            click.echo("Rendering diagram...")
        
        html_content = renderer.render_diagram_auto(diagram_code)
        
        if html_content is None:
            click.echo("❌ Failed to render diagram", err=True)
            sys.exit(1)
        
        # Write output
        output.write_text(html_content, encoding='utf-8')
        
        click.echo(f"✅ Diagram rendered successfully: {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
def info(input_file):
    """
    Show information about a diagram file.
    
    INPUT_FILE: Path to file containing diagram code
    """
    try:
        diagram_code = input_file.read_text(encoding='utf-8')
        renderer = DiagramRenderer()
        
        click.echo(f"File: {input_file}")
        click.echo(f"Size: {input_file.stat().st_size} bytes")
        click.echo(f"Lines: {len(diagram_code.splitlines())}")
        
        detected_type = renderer.detect_diagram_type(diagram_code)
        if detected_type:
            click.echo(f"Detected type: {detected_type.upper()}")
        else:
            click.echo("Detected type: Unknown (will fallback to Mermaid)")
        
        # Show some content preview
        lines = diagram_code.strip().splitlines()
        if lines:
            click.echo("\nContent preview:")
            for i, line in enumerate(lines[:5]):
                click.echo(f"  {i+1}: {line}")
            if len(lines) > 5:
                click.echo(f"  ... ({len(lines) - 5} more lines)")
                
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('-p', '--port', default=8000, help='Port to serve on (default: 8000)')
@click.option('--no-browser', is_flag=True, help='Don\'t automatically open browser')
@click.option('-o', '--output', type=click.Path(path_type=Path), 
              help='Output HTML file path (default: input_file.html)')
def serve(input_file, port, no_browser, output):
    """
    Render diagram and serve it via HTTP server.
    
    INPUT_FILE: Path to file containing diagram code
    
    Examples:
    \b
        diagram-renderer serve flowchart.mmd
        diagram-renderer serve diagram.txt --port 8080
        diagram-renderer serve input.md --no-browser
    """
    try:
        # First render the diagram
        click.echo(f"Reading and rendering: {input_file}")
        
        diagram_code = input_file.read_text(encoding='utf-8')
        renderer = DiagramRenderer()
        
        detected_type = renderer.detect_diagram_type(diagram_code)
        if detected_type:
            click.echo(f"Detected diagram type: {detected_type.upper()}")
        
        html_content = renderer.render_diagram_auto(diagram_code)
        
        if html_content is None:
            click.echo("❌ Failed to render diagram", err=True)
            sys.exit(1)
        
        # Determine output file
        if output is None:
            output = input_file.with_suffix('.html')
        
        # Write the HTML file
        output.write_text(html_content, encoding='utf-8')
        click.echo(f"✅ Diagram rendered: {output}")
        
        # Change to the directory containing the output file
        output_dir = output.parent
        output_name = output.name
        
        # Custom handler to serve from the specific directory
        class DiagramHandler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(output_dir), **kwargs)
        
        # Start HTTP server
        server = HTTPServer(('localhost', port), DiagramHandler)
        
        # Open browser if requested
        url = f"http://localhost:{port}/{output_name}"
        
        if not no_browser:
            # Start browser in a separate thread after a short delay
            def open_browser():
                time.sleep(1)  # Give server time to start
                webbrowser.open(url)
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
        
        click.echo(f"🌐 Serving diagram at: {url}")
        click.echo("Press Ctrl+C to stop the server")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            click.echo("\n👋 Server stopped")
            server.shutdown()
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def examples():
    """Show example diagram code for each supported type."""
    
    examples_data = {
        "Mermaid Flowchart": """graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E""",
        
        "Mermaid Sequence": """sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob!
    B-->>A: Hello Alice!""",
        
        "PlantUML Class": """@startuml
class Animal {
  +String name
  +makeSound()
}
class Dog {
  +bark()
}
Animal <|-- Dog
@enduml""",
        
        "Graphviz DOT": """digraph G {
    A -> B
    B -> C
    C -> A
    A [label="Start"]
    C [label="End"]
}"""
    }
    
    click.echo("Example diagram code for each supported type:\n")
    
    for title, code in examples_data.items():
        click.echo(f"=== {title} ===")
        click.echo(code)
        click.echo()


if __name__ == '__main__':
    cli()
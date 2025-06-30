# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-30

### Added
- Initial release of diagram-renderer
- Support for Mermaid diagrams with static assets
- Support for PlantUML diagrams via VizJS
- Support for Graphviz DOT diagrams via VizJS
- Automatic diagram type detection
- Interactive zoom/pan controls
- PNG export functionality
- Command-line interface with `diagram-renderer` command
- Streamlit dashboard integration
- Multiple theme support for Mermaid diagrams
- Markdown code block extraction
- Comprehensive test suite

### Features
- **Multi-format support**: Render Mermaid, PlantUML, and Graphviz diagrams
- **Static assets**: Version-controlled Mermaid.js and VizJS libraries
- **Auto-detection**: Automatically detect diagram type from code
- **Interactive controls**: Zoom and pan functionality in rendered diagrams
- **Export capabilities**: Download diagrams as PNG or source code
- **CLI tool**: Batch processing and automation via command line
- **Web dashboard**: Interactive Streamlit-based interface
- **Extensible**: Modular renderer architecture for easy extension
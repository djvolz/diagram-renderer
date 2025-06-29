# TODO

## Bugs

- Fix: Double check the mermaid js and viz js libraries work entirely offline and do not call out to the wider web
- Fix: Update pyproject.toml description
- Fix: Remove unused pyproject dependencies
- Fixed: Mermaid diagram button sometimes works and sometimes doesn't. Especially the first click. Download mermaid fails, switch to PlantUML and download succeeds, switch to a different mermaid and download also succeeds

## Enhancements

- Create a click based cli similar to our streamlit dashboard.py for demonstration purposes of how to use the diagram library as a standalone CLI utility
- Enh: Add the ability to preview the backing diagram code within the viewer (maybe by hovering, or maybe the download button should download the diagram code as a file)
- Enh: for command line users we should add an option to spin up a simple python http server to view the diagram
- Enh: we should make this an independent module that can be used via a "uv add" to a project

# TODO

Instructions: Tackle each todo individually. Only tackle one todo item at a time.
After each todo, generate a commit message using a special tool "explain diff".
Ask us to verify the commit message first before actually committing.

## Bugs

- Fixed: Double check the mermaid js and viz js libraries work entirely offline and do not call out to the wider web ✅ (Verified: All JS libraries are self-contained with no external network calls)
- Fixed: Update pyproject.toml description ✅
- Fixed: Remove unused pyproject dependencies ✅ (Removed fastapi, fastmcp, playwright, uvicorn - kept click, pytest, streamlit)
- Fix: Mermaid diagram button sometimes works and sometimes doesn't. Especially the first click. Download mermaid fails, switch to PlantUML and download succeeds, switch to a different mermaid and download also succeeds

## Enhancements

- Create a click based cli similar to our streamlit dashboard.py for demonstration purposes of how to use the diagram library as a standalone CLI utility
- Enh: Add the ability to preview the backing diagram code within the viewer (maybe by hovering, or maybe the download button should download the diagram code as a file)
- Enh: for command line users we should add an option to spin up a simple python http server to view the diagram
- Enh: we should make this an independent module that can be used via a "uv add" to a project

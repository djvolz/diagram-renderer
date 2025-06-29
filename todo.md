# TODO

Instructions: Tackle each todo individually. Only tackle one todo item at a time.
After each todo, generate a commit message using a special tool "explain diff".
Ask us to verify the commit message first before actually committing.

## Bugs

- Fixed: Double check the mermaid js and viz js libraries work entirely offline and do not call out to the wider web ✅ (Verified: All JS libraries are self-contained with no external network calls)
- Fixed: Update pyproject.toml description ✅
- Fixed: Remove unused pyproject dependencies ✅ (Removed fastapi, fastmcp, playwright, uvicorn - kept click, pytest, streamlit)
- Fixed: Mermaid diagram button sometimes works and sometimes doesn't. Especially the first click. Download mermaid fails, switch to PlantUML and download succeeds, switch to a different mermaid and download also succeeds ✅ (Fixed timing issue: Added diagramReady state tracking and disabled download button until rendering completes)

## Enhancements

- Fixed: Create a click based cli similar to our streamlit dashboard.py for demonstration purposes of how to use the diagram library as a standalone CLI utility ✅ (Created examples/cli.py with render, quick, info, examples, and dashboard commands. Moved dashboard.py to examples/ folder. Removed redundant main.py)
- Fixed: Add the ability to preview the backing diagram code within the viewer (maybe by hovering, or maybe the download button should download the diagram code as a file) ✅ (Added 📄 download button that downloads original source code with proper file extensions: .mmd for Mermaid, .txt for others)
- Enh: for command line users we should add an option to spin up a simple python http server to view the diagram
- Enh: we should make this an independent module that can be used via a "uv add" to a project. As part of this we should make click and streamlit optional dependencies. There is no reason to force a requirement on users that just want the html rendering. I'm not sure what the common practice is to do this.

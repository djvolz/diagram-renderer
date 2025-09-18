from ..error_pages import generate_unsupported_diagram_error_html
from .base import BaseRenderer


class PlantUMLRenderer(BaseRenderer):
    """Renderer for PlantUML diagrams using VizJS"""

    def detect_diagram_type(self, code):
        """Detect if code is PlantUML"""
        code_lower = code.strip().lower()

        # Check for strong PlantUML indicators first (before Mermaid check)
        strong_plantuml_indicators = [
            "@startuml",
            "@startmindmap",
            "@startgantt",
            "@startclass",
            "@enduml",
            "skinparam",
            "!theme",
            "!include",
        ]

        for indicator in strong_plantuml_indicators:
            if indicator in code_lower:
                return True

        # Avoid false positives when common Mermaid keywords are present
        # (but not when they're part of PlantUML directives like @startmindmap)
        mermaid_indicators = [
            "flowchart ",
            "graph ",
            "sequencediagram",
            "classdiagram",
            "statediagram",
            "erdiagram",
            "journey",
            "gantt",
            "pie ",
            "gitgraph",
            "requirement",
            "mindmap",
            "timeline",
            "block-beta",
            "c4context",
        ]
        if any(ind in code_lower for ind in mermaid_indicators):
            return False

        if "participant " in code_lower or "actor " in code_lower:
            if (
                "sequencediagram" in code_lower
                or "-->" in code_lower
                or "->>" in code_lower
                or ("participant " in code_lower and ("as " in code_lower or ":" in code_lower))
            ):
                return False
            else:
                return True

        # Weak indicators: only consider if they appear at line start to reduce
        # collisions with free-text labels in other syntaxes (e.g., Mermaid)
        plantuml_weak_indicators = (
            "boundary ",
            "control ",
            "entity ",
            "database ",
            "collections ",
            "queue ",
        )
        for line in code_lower.splitlines():
            stripped = line.lstrip()
            if any(stripped.startswith(tok) for tok in plantuml_weak_indicators):
                return True

        if "class " in code_lower and "classdiagram" not in code_lower:
            return True

        return False

    def clean_code(self, code):
        """Clean diagram code (remove markdown formatting)"""
        code = code.strip()

        if not code.startswith("@start"):
            code = "@startuml\n" + code
        if not code.endswith("@enduml"):
            code = code + "\n@enduml"

        return code

    def convert_plantuml_to_dot(self, plantuml_code):
        """Convert basic PlantUML to DOT notation for VizJS"""
        clean_code = self.clean_code(plantuml_code)
        lines = clean_code.split("\n")

        if any("participant" in line or "actor" in line or "->" in line for line in lines):
            return self._convert_sequence_to_dot(lines)
        elif any("class" in line for line in lines):
            return self._convert_class_to_dot(lines)
        else:
            # Check for known unsupported types first
            unsupported = self._detect_unsupported_plantuml_type(clean_code)
            if unsupported.startswith("UNSUPPORTED_PLANTUML_TYPE:"):
                # For specific unsupported types, return the error
                # But for truly unknown syntax, provide a fallback
                parts = unsupported.split(":", 2)
                if parts[1] != "unknown":
                    return unsupported

            # Fallback for truly unknown syntax - generate a simple DOT graph
            return self._generate_fallback_dot(clean_code)

    def _detect_unsupported_plantuml_type(self, code):
        """Detect unsupported PlantUML diagram types and return error"""
        code_lower = code.lower()

        # Detect specific unsupported diagram types
        unsupported_types = [
            ("@startmindmap", "mindmap", "Mind maps"),
            ("@startsalt", "salt", "Salt UI mockups"),
            ("@startgantt", "gantt", "Gantt charts"),
            ("@startuml\nstart\n", "activity", "Activity diagrams"),
            (":start;", "activity", "Activity diagrams with complex control flow"),
            ("object ", "object", "Object diagrams"),
            ("robust", "timing", "Timing diagrams"),
        ]

        detected_type = None
        detected_description = None

        for pattern, diagram_type, description in unsupported_types:
            if pattern in code_lower:
                detected_type = diagram_type
                detected_description = description
                break

        if detected_type:
            # Return error indicator that render_html will catch
            return f"UNSUPPORTED_PLANTUML_TYPE:{detected_type}:{detected_description}"

        # If we can't detect the specific type, return a generic unsupported message
        return "UNSUPPORTED_PLANTUML_TYPE:unknown:Advanced PlantUML features"

    def _convert_sequence_to_dot(self, lines):
        """Convert PlantUML sequence diagram to DOT"""
        participants = []
        connections = []

        for line in lines:
            line = line.strip()
            if line.startswith("participant") or line.startswith("actor"):
                name = line.split()[1].strip('"')
                if " as " in line:
                    name = line.split(" as ")[1].strip().strip('"')
                participants.append(name)
            elif "->" in line:
                parts = line.split("->")
                if len(parts) == 2:
                    from_p = parts[0].strip()
                    to_part = parts[1].strip()
                    if ":" in to_part:
                        to_p = to_part.split(":")[0].strip()
                        label = to_part.split(":", 1)[1].strip()
                    else:
                        to_p = to_part
                        label = ""
                    connections.append((from_p, to_p, label))

        dot = "digraph sequence {\n"
        dot += "  rankdir=LR;\n"
        dot += "  node [shape=box, style=filled, fillcolor=white];\n"

        for p in participants:
            dot += f'  "{p}";\n'

        for from_p, to_p, label in connections:
            if label:
                dot += f'  "{from_p}" -> "{to_p}" [label="{label}"];\n'
            else:
                dot += f'  "{from_p}" -> "{to_p}";\n'

        dot += "}"
        return dot

    def _convert_class_to_dot(self, lines):
        """Convert PlantUML class diagram to DOT"""
        classes = []
        relationships = []

        for line in lines:
            line = line.strip()
            if line.startswith("class "):
                class_name = line.split()[1].split("{")[0].strip()
                classes.append(class_name)
            elif "<|--" in line:
                parts = line.split("<|--")
                relationships.append((parts[1].strip(), parts[0].strip()))

        dot = "digraph classes {\n"
        dot += "  node [shape=record, style=filled, fillcolor=white];\n"

        for cls in classes:
            dot += f'  "{cls}" [label="{cls}"];\n'

        for parent, child in relationships:
            dot += f'  "{parent}" -> "{child}" [arrowhead=empty];\n'

        dot += "}"
        return dot

    def _generate_fallback_dot(self, plantuml_code):
        """Generate a fallback DOT graph for unknown PlantUML syntax"""
        return """digraph G {
    node [shape=box, style="filled", fillcolor="lightyellow"];
    PlantUML [label="PlantUML Diagram\\n(Local Rendering)"];
    Note [label="This PlantUML diagram type\\nis not fully supported\\nfor local rendering", shape=note, fillcolor="lightblue"];
    PlantUML -> Note [style=dashed];
}"""

    def render_html(self, code, **kwargs):
        """Generate PlantUML diagram as HTML using unified template"""
        if not self.use_local_rendering:
            raise Exception("Local rendering disabled")

        try:
            # Convert PlantUML to DOT
            dot_code = self.convert_plantuml_to_dot(code)

            # Check if conversion returned an unsupported type indicator
            if dot_code.startswith("UNSUPPORTED_PLANTUML_TYPE:"):
                parts = dot_code.split(":", 2)
                diagram_type = parts[1] if len(parts) > 1 else "unknown"
                description = parts[2] if len(parts) > 2 else "Advanced PlantUML features"

                missing_plugins = [
                    {
                        "type": f"plantuml-{diagram_type}",
                        "plugin_needed": "Full PlantUML engine support",
                        "description": f"{description} are not supported by the VizJS-based PlantUML renderer",
                    }
                ]

                return generate_unsupported_diagram_error_html(missing_plugins, code)

            return self._render_unified_html(dot_code, code, "plantuml")

        except Exception as e:
            raise Exception(f"Error rendering PlantUML diagram: {str(e)}")

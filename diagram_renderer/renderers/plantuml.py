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

        # Check for class diagram first (before sequence)
        if any("class " in line for line in lines):
            return self._convert_class_to_dot(lines)
        # Check for use case diagram
        elif any("usecase " in line or "actor " in line for line in lines):
            if any("usecase " in line for line in lines):
                # It's a use case diagram, not a sequence diagram
                return self._convert_usecase_to_dot(lines)
            elif any("participant" in line for line in lines):
                # It has actors AND participants, likely sequence
                return self._convert_sequence_to_dot(lines)
            elif any("->" in line for line in lines):
                # Has actors and arrows but no use cases, likely sequence
                return self._convert_sequence_to_dot(lines)
            else:
                # Has actors but no clear diagram type
                return self._convert_usecase_to_dot(lines)
        elif any("participant" in line or "->" in line for line in lines):
            return self._convert_sequence_to_dot(lines)
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

    def _convert_usecase_to_dot(self, lines):
        """Convert PlantUML use case diagram to DOT"""
        actors = []
        use_cases = []
        connections = []

        for line in lines:
            line = line.strip()

            # Skip PlantUML directives
            if line.startswith("@") or line == "}":
                continue

            # Handle rectangle container (just skip the declaration)
            if line.startswith("rectangle "):
                continue

            # Parse actor definition
            if line.startswith("actor "):
                parts = line.replace("actor ", "").strip()
                if " as " in parts:
                    # actor "Payment System" as PS
                    name = parts.split(" as ")[1].strip()
                    actors.append(name)
                else:
                    # actor Customer
                    name = parts.strip('"').strip()
                    actors.append(name)

            # Parse use case definition
            elif line.startswith("usecase "):
                parts = line.replace("usecase ", "").strip()
                if " as " in parts:
                    # usecase "Browse Products" as UC1
                    label = parts.split(" as ")[0].strip('"')
                    alias = parts.split(" as ")[1].strip()
                    use_cases.append((alias, label))
                else:
                    # usecase "Browse Products"
                    label = parts.strip('"')
                    use_cases.append((label, label))

            # Parse connections and inline use cases
            elif "-->" in line or ".>" in line or "->" in line or "--" in line:
                # Extract inline use cases with parentheses
                import re

                inline_use_case_pattern = r"\(([^)]+)\)"
                inline_use_cases = re.findall(inline_use_case_pattern, line)

                # Add inline use cases to the list if not already present
                for uc_name in inline_use_cases:
                    if not any(uc_name == uc[0] or uc_name == uc[1] for uc in use_cases):
                        use_cases.append((uc_name, uc_name))

                # Parse connections
                arrow_type = "normal"
                parts = []

                if "-->" in line:
                    parts = line.split("-->")
                    arrow_type = "normal"
                elif ".>" in line:
                    parts = line.split(".>")
                    arrow_type = "dashed"
                elif "->" in line:
                    parts = line.split("->")
                    arrow_type = "normal"
                elif "--" in line:
                    # Handle simple association like: Customer -- (Browse Products)
                    parts = line.split("--")
                    arrow_type = "normal"

                if len(parts) == 2:
                    from_node = parts[0].strip()
                    to_part = parts[1].strip()

                    # Handle parentheses in use case names
                    # Convert (Use Case Name) to just Use Case Name
                    if from_node.startswith("(") and from_node.endswith(")"):
                        from_node = from_node[1:-1].strip()
                    if to_part.startswith("(") and to_part.endswith(")"):
                        to_part = to_part[1:-1].strip()

                    # Check for labels like ": extends"
                    if ":" in to_part:
                        to_node = to_part.split(":")[0].strip()
                        label = to_part.split(":", 1)[1].strip()
                    else:
                        to_node = to_part
                        label = ""

                    connections.append((from_node, to_node, label, arrow_type))

        # Generate DOT
        dot = "digraph usecases {\n"
        dot += "  rankdir=LR;\n"
        dot += "  node [shape=box, style=filled, fillcolor=lightblue];\n"

        # Add actors (different shape)
        for actor in actors:
            dot += f'  "{actor}" [shape=ellipse, fillcolor=lightyellow];\n'

        # Add use cases
        for alias, label in use_cases:
            if alias != label:
                dot += f'  "{alias}" [label="{label}"];\n'
            else:
                dot += f'  "{alias}";\n'

        # Add connections
        for from_node, to_node, label, arrow_type in connections:
            style = "dashed" if arrow_type == "dashed" else "solid"
            if label:
                dot += f'  "{from_node}" -> "{to_node}" [label="{label}", style={style}];\n'
            else:
                dot += f'  "{from_node}" -> "{to_node}" [style={style}];\n'

        dot += "}"
        return dot

    def _convert_class_to_dot(self, lines):
        """Convert PlantUML class diagram to DOT"""
        classes = {}  # Map of class name to attributes/methods
        relationships = []

        current_class = None
        class_content = []
        in_class_body = False

        for line in lines:
            line_stripped = line.strip()

            # Skip PlantUML directives
            if line_stripped.startswith("@") or line_stripped.startswith("!"):
                continue

            # Start of class definition
            if line_stripped.startswith("class "):
                # Save previous class if exists
                if current_class:
                    classes[current_class] = class_content
                    class_content = []

                # Parse new class
                class_part = line_stripped.replace("class ", "")
                if "{" in class_part:
                    # Class name is before the brace
                    class_name = class_part.split("{")[0].strip()
                    in_class_body = True

                    # Check if it's a one-line class definition
                    if "}" in class_part:
                        # Extract content between braces
                        content = class_part[
                            class_part.index("{") + 1 : class_part.rindex("}")
                        ].strip()
                        if content:
                            class_content = content.split(";")
                        classes[class_name] = class_content
                        current_class = None
                        class_content = []
                        in_class_body = False
                    else:
                        current_class = class_name
                else:
                    # Class name is the whole part, body starts on next line
                    class_name = class_part.strip()
                    current_class = class_name
                    in_class_body = False

            # Opening brace on its own line
            elif line_stripped == "{" and current_class and not in_class_body:
                in_class_body = True

            # Inside class definition
            elif current_class and in_class_body and line_stripped != "}":
                if line_stripped:
                    class_content.append(line_stripped)

            # End of class definition
            elif line_stripped == "}" and current_class:
                classes[current_class] = class_content
                current_class = None
                class_content = []
                in_class_body = False

            # Parse relationships (when not inside a class body)
            elif not in_class_body and (
                "-->" in line_stripped or "<|--" in line_stripped or "||--" in line_stripped
            ):
                # Handle different PlantUML relationship notations
                if "||--o{" in line_stripped:
                    # One-to-many composition: User ||--o{ Order
                    parts = line_stripped.split("||--o{")
                    if len(parts) == 2:
                        from_class = parts[0].strip()
                        to_part = parts[1].strip()

                        # Handle label
                        if ":" in to_part:
                            to_class = to_part.split(":")[0].strip()
                            label = to_part.split(":", 1)[1].strip()
                            # Remove surrounding quotes from label if present
                            if label.startswith('"') and label.endswith('"'):
                                label = label[1:-1]
                        else:
                            to_class = to_part.strip()
                            label = ""

                        if from_class and to_class:
                            relationships.append((from_class, to_class, "association", label))

                elif "-->" in line_stripped:
                    # Association: User "1" --> "0..*" Order : places
                    parts = line_stripped.split("-->")
                    if len(parts) == 2:
                        from_part = parts[0].strip()
                        to_part = parts[1].strip()

                        # Extract class names (ignore cardinality)
                        # Handle quoted cardinality like "1" or unquoted
                        from_class = from_part.split('"')[0].strip()
                        if not from_class:  # If it starts with a quote
                            from_tokens = from_part.split()
                            from_class = from_tokens[0] if from_tokens else from_part

                        # Handle label
                        if ":" in to_part:
                            to_with_card = to_part.split(":")[0].strip()
                            label = to_part.split(":", 1)[1].strip()
                            # Remove surrounding quotes from label if present
                            if label.startswith('"') and label.endswith('"'):
                                label = label[1:-1]
                        else:
                            to_with_card = to_part
                            label = ""

                        # Extract to class (may have cardinality)
                        to_tokens = to_with_card.replace('"', " ").split()
                        to_class = to_tokens[-1] if to_tokens else to_with_card

                        if from_class and to_class:
                            relationships.append((from_class, to_class, "association", label))

                elif "<|--" in line_stripped:
                    # Inheritance
                    parts = line_stripped.split("<|--")
                    if len(parts) == 2:
                        parent = parts[0].strip()
                        child = parts[1].strip()
                        if parent and child:
                            relationships.append((child, parent, "inheritance", ""))

        # Save last class if still open (shouldn't happen with valid PlantUML)
        if current_class:
            classes[current_class] = class_content

        # Generate DOT
        dot = "digraph classes {\n"
        dot += "  rankdir=TB;\n"
        dot += "  node [shape=record, style=filled, fillcolor=lightyellow];\n"

        # Add classes with their attributes/methods
        for cls_name, attributes in classes.items():
            if attributes:
                # Format as record with attributes/methods
                # Escape special characters and join attributes
                attr_str = "\\l".join(attr.replace('"', '\\"') for attr in attributes)
                label = f"{{{cls_name}|{attr_str}\\l}}"
                dot += f'  "{cls_name}" [label="{label}"];\n'
            else:
                # Simple class with no body
                dot += f'  "{cls_name}" [label="{cls_name}"];\n'

        # Add relationships
        for from_cls, to_cls, rel_type, label in relationships:
            if rel_type == "inheritance":
                dot += f'  "{from_cls}" -> "{to_cls}" [arrowhead=empty];\n'
            elif rel_type == "association":
                if label:
                    # Escape quotes in label and ensure it's properly quoted
                    escaped_label = label.replace('"', '\\"')
                    dot += f'  "{from_cls}" -> "{to_cls}" [label="{escaped_label}"];\n'
                else:
                    dot += f'  "{from_cls}" -> "{to_cls}";\n'

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
                        "plugin_needed": "plantuml-server.jar",  # Use a proper filename for consistency
                        "description": f"{description} are not supported by the VizJS-based PlantUML renderer. Full PlantUML Java server would be required for these features",
                    }
                ]

                return generate_unsupported_diagram_error_html(missing_plugins, code)

            return self._render_unified_html(dot_code, code, "plantuml")

        except Exception as e:
            raise Exception(f"Error rendering PlantUML diagram: {str(e)}")

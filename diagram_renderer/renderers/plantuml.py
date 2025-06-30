from .base import BaseRenderer

class PlantUMLRenderer(BaseRenderer):
    """Renderer for PlantUML diagrams using VizJS"""

    def detect_diagram_type(self, code):
        """Detect if code is PlantUML"""
        code = code.strip().lower()

        strong_plantuml_indicators = [
            "@startuml", "@startmindmap", "@startgantt", "@startclass",
            "@enduml", "skinparam", "!theme", "!include"
        ]

        for indicator in strong_plantuml_indicators:
            if indicator in code:
                return True

        if "participant " in code or "actor " in code:
            if ("sequencediagram" in code or 
                "-->" in code or "->>" in code or 
                ("participant " in code and ("as " in code or ":" in code))):
                return False
            else:
                return True

        plantuml_weak_indicators = [
            "boundary ", "control ", "entity ", "database ", 
            "collections ", "queue "
        ]

        for indicator in plantuml_weak_indicators:
            if indicator in code:
                return True

        if "class " in code and "classdiagram" not in code:
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
        lines = clean_code.split('\n')

        if any('participant' in line or 'actor' in line or '->' in line for line in lines):
            return self._convert_sequence_to_dot(lines)
        elif any('class' in line for line in lines):
            return self._convert_class_to_dot(lines)
        else:
            return '''digraph G {
  node [style=filled, fillcolor=white];
  "PlantUML" -> "Local Rendering";
}'''

    def _convert_sequence_to_dot(self, lines):
        """Convert PlantUML sequence diagram to DOT"""
        participants = []
        connections = []

        for line in lines:
            line = line.strip()
            if line.startswith('participant') or line.startswith('actor'):
                name = line.split()[1].strip('"')
                if ' as ' in line:
                    name = line.split(' as ')[1].strip().strip('"')
                participants.append(name)
            elif '->' in line:
                parts = line.split('->')
                if len(parts) == 2:
                    from_p = parts[0].strip()
                    to_part = parts[1].strip()
                    if ':' in to_part:
                        to_p = to_part.split(':')[0].strip()
                        label = to_part.split(':', 1)[1].strip()
                    else:
                        to_p = to_part
                        label = ""
                    connections.append((from_p, to_p, label))

        dot = 'digraph sequence {\n'
        dot += '  rankdir=LR;\n'
        dot += '  node [shape=box, style=filled, fillcolor=white];\n'

        for p in participants:
            dot += f'  "{p}";\n'

        for from_p, to_p, label in connections:
            if label:
                dot += f'  "{from_p}" -> "{to_p}" [label="{label}"];\n'
            else:
                dot += f'  "{from_p}" -> "{to_p}";\n'

        dot += '}'
        return dot

    def _convert_class_to_dot(self, lines):
        """Convert PlantUML class diagram to DOT"""
        classes = []
        relationships = []

        for line in lines:
            line = line.strip()
            if line.startswith('class '):
                class_name = line.split()[1].split('{')[0].strip()
                classes.append(class_name)
            elif '<|--' in line:
                parts = line.split('<|--')
                relationships.append((parts[1].strip(), parts[0].strip()))

        dot = 'digraph classes {\n'
        dot += '  node [shape=record, style=filled, fillcolor=white];\n'

        for cls in classes:
            dot += f'  "{cls}" [label="{cls}"];\n'

        for parent, child in relationships:
            dot += f'  "{parent}" -> "{child}" [arrowhead=empty];\n'

        dot += '}'
        return dot

    def render_html(self, code, **kwargs):
        """Generate PlantUML-like diagram as HTML using local VizJS"""
        if not self.use_local_rendering:
            raise Exception("Local rendering disabled")

        try:
            dot_code = self.convert_plantuml_to_dot(code)
            return self._render_vizjs_html(dot_code, original_code=code)
        except Exception as e:
            raise Exception(f"Error rendering PlantUML diagram: {str(e)}")

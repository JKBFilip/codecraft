from PySide6.QtWidgets import QListWidget

class ReorderList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.InternalMove)

    def get_code_string(self):
        lines = []
        indent = ""
        for i in range(self.count()):
            line = self.item(i).text()
            lines.append(indent + line)

            # Jeśli linia kończy się ':', zwiększ wcięcie
            if line.strip().endswith(':'):
                indent += "    "
            # Jeśli to 'else:', 'elif:' itd., to zmniejsz i potem zwiększ
            elif line.strip().startswith(('else', 'elif')):
                indent = indent[:-4] + "    "

        return '\n'.join(lines)

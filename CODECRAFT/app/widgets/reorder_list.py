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
            if line.strip().endswith(':'):
                indent += "    "
            elif line.strip().startswith(('else', 'elif')):
                indent = indent[:-4] + "    "

        return '\n'.join(lines)

    def load_from_code(self, code: str):
        self.clear()
        lines = code.splitlines()
        for line in lines:
            self.addItem(line.strip())
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit


class PurePythonInput(QWidget):
    def __init__(self):
        super().__init__()
        self.user_data = ""  # This is your "Pure Python" field

        layout = QVBoxLayout()

        # Create a field, but strip the 'Word Processor' styling
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type here...")
        self.input_field.setFrame(False)  # Removes the OS border

        # Sync the 'Pure' variable every time the text changes
        self.input_field.textChanged.connect(self.sync_data)

        layout.addWidget(self.input_field)
        self.setLayout(layout)

    def sync_data(self, text):
        self.user_data = text
        print(f"Current Python String: {self.user_data}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PurePythonInput()
    window.show()
    sys.exit(app.exec())
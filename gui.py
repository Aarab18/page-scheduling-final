import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page Scheduling Simulator")
        self.setGeometry(100, 100, 600, 400)

        # Set up central widget and layout
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Input fields
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter reference string (e.g., 1 2 3 4)")
        self.frame_field = QLineEdit(self)
        self.frame_field.setPlaceholderText("Enter frame size (e.g., 3)")

        # Submit button
        self.submit_button = QPushButton("Run Simulation", self)
        self.submit_button.clicked.connect(self.run_simulation)

        # Result display
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)

        # Add widgets to layout
        layout.addWidget(self.input_field)
        layout.addWidget(self.frame_field)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_area)

        # Basic styling
        self.setStyleSheet("QLineEdit { padding: 5px; } QPushButton { padding: 10px; }")

    def validate_input(self):
        """Validate the reference string input."""
        text = self.input_field.text()
        try:
            ref_string = [int(x) for x in text.split()]
            return ref_string
        except ValueError:
            self.input_field.setText("Invalid input! Enter space-separated integers.")
            return None

    def run_simulation(self):
        """Placeholder for running the simulation."""
        ref_string = self.validate_input()
        if ref_string is None:
            return
        frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
        self.result_area.setText(f"Running simulation with {ref_string} and frame size {frame_size}\nGraph placeholder")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
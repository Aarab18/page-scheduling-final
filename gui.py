import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

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
        
        # Set background color
        widget.setStyleSheet("background-color: #dfe6e9;")
        
        # Title label
        title_label = QLabel("Page Scheduling Simulator")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px; background-color: #74b9ff; padding: 10px; border-radius: 5px;")
        layout.addWidget(title_label)
        
        # Input fields
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter reference string (e.g., 1 2 3 4)")
        self.input_field.setFont(QFont("Arial", 10))
        self.input_field.setStyleSheet("background-color: white; border: 2px solid #3498db; border-radius: 5px; padding: 8px;")
        
        self.frame_field = QLineEdit(self)
        self.frame_field.setPlaceholderText("Enter frame size (e.g., 3)")
        self.frame_field.setFont(QFont("Arial", 10))
        self.frame_field.setStyleSheet("background-color: white; border: 2px solid #3498db; border-radius: 5px; padding: 8px;")
        
        # Submit button
        self.submit_button = QPushButton("Run Simulation", self)
        self.submit_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.submit_button.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        self.submit_button.clicked.connect(self.run_simulation)
        
        # Result display
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        self.result_area.setFont(QFont("Arial", 10))
        self.result_area.setStyleSheet("background-color: #ecf0f1; border: 2px solid #bdc3c7; border-radius: 5px; padding: 8px;")
        
        # Add widgets to layout
        layout.addWidget(self.input_field)
        layout.addWidget(self.frame_field)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_area)
        
        # Basic styling
        self.setStyleSheet("QLineEdit { padding: 8px; } QPushButton:hover { background-color: #2980b9; }")
    
    def validate_input(self):
        """Validate the reference string input."""
        text = self.input_field.text()
        try:
            ref_string = [int(x) for x in text.split()]
            return ref_string
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter space-separated integers only.")
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
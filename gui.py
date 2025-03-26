import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtWidgets import QTextEdit
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page Scheduling Simulator")
        self.setGeometry(100, 100, 600, 400)
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.input_field = QLineEdit(self)
        self.submit_button = QPushButton("Run Simulation", self)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_button)
        self.frame_field = QLineEdit(self)
		layout.addWidget(self.frame_field)
		self.submit_button.clicked.connect(self.run_simulation)
		self.result_area = QTextEdit(self)
		layout.addWidget(self.result_area)
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
    ref_string = self.validate_input()
    frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
    print(f"Reference String: {ref_string}, Frame Size: {frame_size}")
    
def run_simulation(self):
    ref_string = self.validate_input()
    frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
    self.result_area.setText(f"Running simulation with {ref_string} and frame size {frame_size}")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
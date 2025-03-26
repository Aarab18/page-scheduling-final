import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton
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
        
def validate_input(self):
        """Validate the reference string input."""
        text = self.input_field.text()
        try:
            ref_string = [int(x) for x in text.split()]
            return ref_string
        except ValueError:
            self.input_field.setText("Invalid input! Enter space-separated integers.")
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
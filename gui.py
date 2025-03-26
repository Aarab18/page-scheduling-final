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
        
        # Colorful background
        widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                stop:0 #a29bfe, stop:1 #74b9ff);
            border-radius: 10px;
        """)
        
        # Vibrant title label
        title_label = QLabel("Page Scheduling Simulator")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #ffffff;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #ff7675, stop:1 #fdcb6e);
            padding: 15px;
            border-radius: 8px;
            margin: 10px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        """)
        layout.addWidget(title_label)
        
        # Colorful input fields
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter reference string (e.g., 1 2 3 4)")
        self.input_field.setFont(QFont("Segoe UI", 11))
        self.input_field.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #fab1a0;
            border-radius: 6px;
            padding: 10px;
            margin: 5px 10px;
            color: #2d3436;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #ffffff, stop:1 #ffeaa7);
        """)
        self.input_field.setFocus()
        
        self.frame_field = QLineEdit(self)
        self.frame_field.setPlaceholderText("Enter frame size (e.g., 3)")
        self.frame_field.setFont(QFont("Segoe UI", 11))
        self.frame_field.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #55efc4;
            border-radius: 6px;
            padding: 10px;
            margin: 5px 10px;
            color: #2d3436;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #ffffff, stop:1 #b2ff59);
        """)
        
        # Bright button with effects
        self.submit_button = QPushButton("Run Simulation", self)
        self.submit_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #e84393;
                color: white;
                padding: 12px;
                border-radius: 6px;
                margin: 10px;
                border: none;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            QPushButton:hover {
                background-color: #fd79a8;
            }
            QPushButton:pressed {
                background-color: #d63031;
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }
        """)
        self.submit_button.clicked.connect(self.run_simulation)
        
        # Colorful result area
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        self.result_area.setFont(QFont("Segoe UI", 10))
        self.result_area.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #6c5ce7;
            border-radius: 6px;
            padding: 10px;
            margin: 5px 10px;
            color: #2d3436;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                stop:0 #ffffff, stop:1 #dfe6e9);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        """)
        
        # Add widgets to layout with spacing
        layout.addWidget(self.input_field)
        layout.addWidget(self.frame_field)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_area)
        layout.setSpacing(15)
        
        # Window styling with focus effects
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLineEdit:focus {
                border: 2px solid #00cec9;
                box-shadow: 0 0 8px rgba(0, 206, 201, 0.5);
            }
        """)

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
    # Set application-wide palette with colorful base
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#a29bfe"))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PageReplacementSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Page Scheduling Simulator")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f5f6fa;")
        
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # Title
        title_label = QLabel("Page Scheduling Simulator", self)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #273c75; padding: 10px; background-color: #74b9ff; border-radius: 8px;")
        layout.addWidget(title_label)
        
        # Input Fields
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter reference string (e.g., 1 2 3 4)")
        self.input_field.setFont(QFont("Arial", 10))
        self.input_field.setStyleSheet("background: white; border: 2px solid #0984e3; border-radius: 5px; padding: 8px;")
        layout.addWidget(self.input_field)
        
        self.frame_field = QLineEdit(self)
        self.frame_field.setPlaceholderText("Enter frame size (e.g., 3)")
        self.frame_field.setFont(QFont("Arial", 10))
        self.frame_field.setStyleSheet("background: white; border: 2px solid #0984e3; border-radius: 5px; padding: 8px;")
        layout.addWidget(self.frame_field)
        
        # Submit Button
        self.submit_button = QPushButton("Run Simulation", self)
        self.submit_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.submit_button.setStyleSheet("background-color: #00cec9; color: white; padding: 10px; border-radius: 5px;")
        self.submit_button.clicked.connect(self.run_simulation)
        layout.addWidget(self.submit_button)
        
        # Graph Area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
    def validate_input(self):
        text = self.input_field.text()
        try:
            ref_string = [int(x) for x in text.split()]
            return ref_string
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter space-separated integers only.")
            return None
    
    def run_simulation(self):
        ref_string = self.validate_input()
        if ref_string is None:
            return
        
        frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
        result_text = f"Running simulation with {ref_string} and frame size {frame_size}...\n"
        
        self.show_result_alert(result_text)
        self.plot_graph(ref_string, frame_size)
        
    def show_result_alert(self, result_text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Simulation Result")
        msg.setText(result_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def plot_graph(self, ref_string, frame_size):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        time_axis = np.arange(len(ref_string))
        frames = np.random.randint(0, frame_size, len(ref_string))  # Simulated data for now
        
        ax.plot(time_axis, frames, marker='o', linestyle='-', color='b', label="Frame Usage")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Frame Number")
        ax.set_title("Page Replacement Process Visualization")
        ax.legend()
        
        self.canvas.draw()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PageReplacementSimulator()
    window.show()
    sys.exit(app.exec_())
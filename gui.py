import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                            QMessageBox, QTextEdit, QStatusBar, QGraphicsDropShadowEffect,
                            QCheckBox, QProgressBar)
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PageReplacementSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """Initialize the main user interface"""
        self.setWindowTitle("Page Scheduling Simulator")
        self.setGeometry(100, 100, 1150, 800)
        self.dark_mode = False
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(25)
        self.central_widget.setLayout(self.main_layout)
        
        # Header
        self.create_header()
        
        # Input container
        self.create_input_container()
        
        # Progress bar
        self.create_progress_bar()
        
        # Results area
        self.create_result_area()
        
        # Graph
        self.create_graph()
        
        # Status bar
        self.create_status_bar()
        
        # Connect submit button
        self.submit_button.clicked.connect(self.run_simulation)
        
        # Apply initial theme
        self.set_light_theme()
        self.update_styles()
        
    def create_header(self):
        """Create the header section of the GUI"""
        self.header_widget = QWidget()
        self.header_widget.setFixedHeight(100)
        header_layout = QHBoxLayout(self.header_widget)
        
        self.title = QLabel("Page Scheduling Simulator")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header_layout.addWidget(self.title)
        
        # Dark mode toggle
        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.setFont(QFont("Segoe UI", 10))
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_toggle)
        self.main_layout.addWidget(self.header_widget)
        
    def create_input_container(self):
        """Create input fields and submit button"""
        self.input_container = QWidget()
        input_layout = QHBoxLayout(self.input_container)
        input_layout.setSpacing(20)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Reference String (e.g., 1 2 3 4)")
        self.input_field.setFont(QFont("Segoe UI", 12))
        self.input_field.textChanged.connect(self.validate_input_live)
        self.input_field.setMinimumWidth(400)
        input_layout.addWidget(self.input_field)
        
        self.frame_field = QLineEdit()
        self.frame_field.setPlaceholderText("Frame Size (default: 3)")
        self.frame_field.setFont(QFont("Segoe UI", 12))
        self.frame_field.textChanged.connect(self.validate_frame_live)
        self.frame_field.setMaximumWidth(200)
        input_layout.addWidget(self.frame_field)
        
        self.submit_button = QPushButton("Run Simulation")
        self.submit_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.submit_button.setCursor(Qt.PointingHandCursor)
        input_layout.addWidget(self.submit_button)
        
        self.main_layout.addWidget(self.input_container)
        
    def create_progress_bar(self):
        """Create progress bar for simulation"""
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.hide()
        self.main_layout.addWidget(self.progress_bar)
        
    def create_result_area(self):
        """Create area to display simulation results"""
        self.result_area = QTextEdit()
        self.result_area.setFont(QFont("Segoe UI", 12))
        self.result_area.setReadOnly(True)
        self.main_layout.addWidget(self.result_area)
        
    def create_graph(self):
        """Create matplotlib graph canvas"""
        self.figure = Figure(figsize=(10, 4.5), facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        self.main_layout.addWidget(self.canvas)
        
    def create_status_bar(self):
        """Create status bar"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def set_light_theme(self):
        """Set light theme styles"""
        # Color palette for light theme
        self.bg_color = '#ffffff'  # White background
        self.bg_secondary = '#f0f4f8'  # Light gray background
        self.text_primary = '#2c3e50'  # Dark blue-gray text
        self.text_secondary = '#34495e'  # Slightly lighter blue-gray
        self.accent_color = '#6b48ff'  # Purple accent
        self.border_color = '#e0e4e8'  # Light gray border
        self.shadow_color = QColor(0, 0, 0, 30)  # Subtle shadow
        
        # Update dark mode flag
        self.dark_mode = False
        self.theme_toggle.setChecked(False)

    def set_dark_theme(self):
        """Set dark theme styles"""
        # Color palette for dark theme
        self.bg_color = '#2d3436'  # Dark background
        self.bg_secondary = '#353b48'  # Slightly lighter dark background
        self.text_primary = '#dcdde1'  # Light gray text
        self.text_secondary = '#b2bec3'  # Lighter gray text
        self.accent_color = '#00ddeb'  # Cyan accent
        self.border_color = '#576574'  # Dark gray border
        self.shadow_color = QColor(255, 255, 255, 30)  # Subtle light shadow
        
        # Update dark mode flag
        self.dark_mode = True
        self.theme_toggle.setChecked(True)

    def update_styles(self):
        """Update widget styles and shadows"""
        # Styling for root/central widget
        self.central_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {self.bg_color};
                color: {self.text_primary};
            }}
        """)
        
        # Header title styling
        self.title.setStyleSheet(f"""
            QLabel {{
                color: {self.text_primary};
                background-color: transparent;
            }}
        """)
        
        # Theme toggle styling
        self.theme_toggle.setStyleSheet(f"""
            QCheckBox {{
                color: {self.text_primary};
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid {self.accent_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.accent_color};
            }}
        """)
        
        # Input fields styling
        input_styles = f"""
            QLineEdit {{
                background-color: {self.bg_secondary};
                color: {self.text_primary};
                border: none;
                border-bottom: 2px solid {self.border_color};
                padding: 8px;
                font-size: 12pt;
            }}
            QLineEdit:focus {{
                border-bottom-color: {self.accent_color};
            }}
        """
        self.input_field.setStyleSheet(input_styles)
        self.frame_field.setStyleSheet(input_styles)
        
        # Submit button styling
        self.submit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.accent_color};
                color: {self.bg_color};
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """)
        
        # Result area styling
        self.result_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.bg_secondary};
                color: {self.text_primary};
                border: none;
                padding: 10px;
            }}
        """)
        
        # Progress bar styling
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {self.bg_secondary};
                border: none;
                height: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {self.accent_color};
            }}
        """)
        
        # Add drop shadow effects
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(self.shadow_color)
        shadow_effect.setOffset(0, 2)
        
        # Apply shadow to specific widgets
        self.input_container.setGraphicsEffect(shadow_effect)
        self.result_area.setGraphicsEffect(shadow_effect)
        
        # Status bar styling
        self.statusBar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {self.bg_secondary};
                color: {self.text_secondary};
            }}
        """)

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
        self.update_styles()
        
    def validate_input_live(self):
        """Live validation of input field"""
        text = self.input_field.text().strip()
        style = self.input_field.styleSheet()
        if text:
            try:
                [int(x) for x in text.split()]
                self.input_field.setStyleSheet(style + f"border-bottom: 2px solid {self.accent_color};")
            except ValueError:
                self.input_field.setStyleSheet(style + "border-bottom: 2px solid #ff6b6b;")
        else:
            self.input_field.setStyleSheet(style + f"border-bottom: 2px solid {self.border_color};")
        
    def validate_frame_live(self):
        """Live validation of frame size field"""
        text = self.frame_field.text().strip()
        style = self.frame_field.styleSheet()
        if text:
            try:
                if int(text) > 0:
                    self.frame_field.setStyleSheet(style + f"border-bottom: 2px solid {self.accent_color};")
                else:
                    self.frame_field.setStyleSheet(style + "border-bottom: 2px solid #ff6b6b;")
            except ValueError:
                self.frame_field.setStyleSheet(style + "border-bottom: 2px solid #ff6b6b;")
        else:
            self.frame_field.setStyleSheet(style + f"border-bottom: 2px solid {self.border_color};")
        
    def validate_input(self):
        """Validate reference string input"""
        text = self.input_field.text().strip()
        if not text:
            self.show_error("Please enter a reference string")
            return None
        try:
            ref_string = [int(x) for x in text.split()]
            if not ref_string:
                raise ValueError
            return ref_string
        except ValueError:
            self.show_error("Enter space-separated integers only")
            return None
        
    def show_error(self, message):
        """Display error message"""
        msg = QMessageBox(self)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background: {self.bg_color};
                border-radius: 10px;
            }}
            QLabel {{
                color: {self.text_primary};
            }}
            QPushButton {{
                background: #ff6b6b;
                color: white;
                padding: 8px 20px;
                border-radius: 15px;
            }}
        """)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()
        
    def run_simulation(self):
        """Run page replacement simulation"""
        ref_string = self.validate_input()
        if ref_string is None:
            return
            
        frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
        if frame_size <= 0:
            self.show_error("Frame size must be positive")
            return
            
        self.statusBar.showMessage("Processing...")
        self.progress_bar.show()
        
        # Simulate processing with progress
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)
        
        # Placeholder for actual algorithm implementation
        results = {
            'FIFO': 10,
            'LRU': 8,
            'Optimal': 7
        }
        analysis = "LRU algorithm performed best"
        
        result_text = "<h3>Simulation Results</h3>"
        for algo, faults in results.items():
            result_text += f"<p><b>{algo}:</b> {faults} page faults</p>"
        result_text += f"<p style='color: {self.accent_color};'><b>{analysis}</b></p>"
        
        self.result_area.setHtml(result_text)
        self.plot_graph(results)
        
    def update_progress(self):
        """Update progress bar during simulation"""
        self.progress_value += 10
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.progress_bar.hide()
            self.statusBar.showMessage("Simulation completed successfully")
        
    def plot_graph(self, results):
        """Plot bar graph of simulation results"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        algorithms = list(results.keys())
        faults = list(results.values())
        colors = [
            self.accent_color, 
            '#00ddeb', 
            '#ff6b6b', 
            '#4ecdc4', 
            '#45b7d1'
        ]
        
        bars = ax.bar(algorithms, faults, color=colors, width=0.65, alpha=0.9)
        
        ax.set_title("Algorithm Performance", fontsize=16, pad=20, fontweight='bold')
        ax.set_xlabel("Algorithms", fontsize=12)
        ax.set_ylabel("Page Faults", fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
        ax.set_facecolor(self.bg_color)
        self.figure.set_facecolor('none')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', 
                   fontsize=10, fontweight='bold', 
                   color=self.text_primary)
        
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = PageReplacementSimulator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QLabel,
                            QMessageBox, QTextEdit, QStatusBar, QGraphicsDropShadowEffect,
                            QCheckBox, QProgressBar, QComboBox, QGridLayout, QScrollArea)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PageReplacementSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.results = {}
        self.current_step = 0
        
    def initUI(self):
        self.setWindowTitle("Page Replacement Simulator")
        self.setGeometry(100, 100, 2000, 1400)  # Further expanded window size
        
        # Central widget with scroll area
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Scroll area for the entire page
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_container = QWidget()
        self.main_layout = QVBoxLayout(self.scroll_container)
        self.main_layout.setSpacing(30)
        self.scroll_area.setWidget(self.scroll_container)
        
        # Add scroll area to central widget
        central_layout = QVBoxLayout(self.central_widget)
        central_layout.addWidget(self.scroll_area)
        
        # Create UI components
        self.create_header()
        self.create_input_container()
        self.create_progress_bar()
        self.create_visualization_area()
        self.create_control_buttons()
        self.create_result_area()
        self.create_graph()
        self.create_status_bar()
        
        # Apply initial theme
        self.set_light_theme()
        self.update_styles()
        
    def create_header(self):
        self.header_widget = QWidget()
        self.header_widget.setFixedHeight(100)
        header_layout = QHBoxLayout(self.header_widget)
        
        self.title = QLabel("Page Replacement Simulator")
        self.title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header_layout.addWidget(self.title)
        
        self.theme_toggle = QCheckBox("Dark Mode")
        self.theme_toggle.setFont(QFont("Segoe UI", 10))
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_toggle)
        self.main_layout.addWidget(self.header_widget)
    
    def create_input_container(self):
        self.input_container = QWidget()
        input_layout = QHBoxLayout(self.input_container)
        input_layout.setSpacing(20)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Reference String (e.g., 1 2 3 4)")
        self.input_field.setFont(QFont("Segoe UI", 12))
        self.input_field.textChanged.connect(self.validate_input_live)
        self.input_field.setMinimumWidth(500)  # Larger input field
        input_layout.addWidget(self.input_field)
        
        self.frame_field = QLineEdit()
        self.frame_field.setPlaceholderText("Frame Size (default: 3)")
        self.frame_field.setFont(QFont("Segoe UI", 12))
        self.frame_field.textChanged.connect(self.validate_frame_live)
        self.frame_field.setMaximumWidth(200)
        input_layout.addWidget(self.frame_field)
        
        self.algo_dropdown = QComboBox()
        self.algo_dropdown.addItems([
            "All Algorithms", "FIFO", "LRU", "Optimal", "Second Chance", "Clock"
        ])
        self.algo_dropdown.setFont(QFont("Segoe UI", 12))
        input_layout.addWidget(self.algo_dropdown)
        
        self.submit_button = QPushButton("Run Simulation")
        self.submit_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.clicked.connect(self.run_simulation)
        input_layout.addWidget(self.submit_button)
        
        self.main_layout.addWidget(self.input_container)
    
    def create_progress_bar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.hide()
        self.main_layout.addWidget(self.progress_bar)
    
    def create_visualization_area(self):
        self.vis_widget = QWidget()
        self.vis_layout = QVBoxLayout(self.vis_widget)
        
        self.step_label = QLabel("Step 0: Initial State")
        self.step_label.setFont(QFont("Segoe UI", 16))
        self.vis_layout.addWidget(self.step_label)
        
        # Scroll area for side-by-side grids
        self.vis_scroll = QScrollArea()
        self.vis_scroll.setWidgetResizable(True)
        self.vis_scroll.setMinimumHeight(400)  # Larger visualization area
        self.vis_container = QWidget()
        self.vis_grid_layout = QHBoxLayout(self.vis_container)
        self.vis_grid_layout.setSpacing(30)
        self.vis_scroll.setWidget(self.vis_container)
        self.vis_layout.addWidget(self.vis_scroll)
        
        self.algo_grids = {}
        self.main_layout.addWidget(self.vis_widget)
    
    def create_control_buttons(self):
        self.control_widget = QWidget()
        control_layout = QHBoxLayout(self.control_widget)
        
        self.prev_button = QPushButton("Previous Step")
        self.prev_button.setFont(QFont("Segoe UI", 12))
        self.prev_button.setCursor(Qt.PointingHandCursor)
        self.prev_button.clicked.connect(self.prev_step)
        control_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next Step")
        self.next_button.setFont(QFont("Segoe UI", 12))
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.clicked.connect(self.next_step)
        control_layout.addWidget(self.next_button)
        
        self.auto_play = QCheckBox("Auto Play")
        self.auto_play.setFont(QFont("Segoe UI", 12))
        self.auto_play.stateChanged.connect(self.toggle_auto_play)
        control_layout.addWidget(self.auto_play)
        
        self.main_layout.addWidget(self.control_widget)
    
    def create_result_area(self):
        self.result_area = QTextEdit()
        self.result_area.setFont(QFont("Segoe UI", 12))
        self.result_area.setReadOnly(True)
        self.result_area.setMinimumHeight(600)  # Much larger result area
        self.main_layout.addWidget(self.result_area)
    
    def create_graph(self):
        self.figure = Figure(figsize=(15, 6), facecolor='none')  # Larger graph
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(400)  # Ensure graph is tall enough
        self.main_layout.addWidget(self.canvas)
    
    def create_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
    
    def set_light_theme(self):
        self.bg_color = '#ffffff'
        self.bg_secondary = '#f0f4f8'
        self.text_primary = '#2c3e50'
        self.text_secondary = '#34495e'
        self.accent_color = '#6b48ff'
        self.border_color = '#e0e4e8'
        self.shadow_color = QColor(0, 0, 0, 30)
        self.dark_mode = False
        self.theme_toggle.setChecked(False)
    
    def set_dark_theme(self):
        self.bg_color = '#2d3436'
        self.bg_secondary = '#353b48'
        self.text_primary = '#dcdde1'
        self.text_secondary = '#b2bec3'
        self.accent_color = '#00ddeb'
        self.border_color = '#576574'
        self.shadow_color = QColor(255, 255, 255, 30)
        self.dark_mode = True
        self.theme_toggle.setChecked(True)
    
    def update_styles(self):
        self.central_widget.setStyleSheet(f"background-color: {self.bg_color}; color: {self.text_primary};")
        self.scroll_container.setStyleSheet(f"background-color: {self.bg_color};")
        self.title.setStyleSheet(f"color: {self.text_primary}; background-color: transparent;")
        
        self.theme_toggle.setStyleSheet(f"""
            QCheckBox {{ color: {self.text_primary}; spacing: 5px; }}
            QCheckBox::indicator {{ width: 20px; height: 20px; border-radius: 10px; border: 2px solid {self.accent_color}; }}
            QCheckBox::indicator:checked {{ background-color: {self.accent_color}; }}
        """)
        
        input_styles = f"""
            QLineEdit {{ background-color: {self.bg_secondary}; color: {self.text_primary}; border: none;
                        border-bottom: 2px solid {self.border_color}; padding: 8px; font-size: 12pt; }}
            QLineEdit:focus {{ border-bottom-color: {self.accent_color}; }}
        """
        self.input_field.setStyleSheet(input_styles)
        self.frame_field.setStyleSheet(input_styles)
        
        self.algo_dropdown.setStyleSheet(f"""
            QComboBox {{ background-color: {self.bg_secondary}; color: {self.text_primary}; 
                        padding: 8px; border-radius: 5px; border: 1px solid {self.border_color}; }}
            QComboBox::drop-down {{ border: none; width: 30px; }}
            QComboBox QAbstractItemView {{ background-color: {self.bg_secondary}; color: {self.text_primary};
                                         border: 1px solid {self.border_color}; }}
        """)
        
        button_style = f"""
            QPushButton {{ background-color: {self.accent_color}; color: {self.bg_color}; border: none;
                          padding: 10px 20px; font-weight: bold; border-radius: 5px; }}
            QPushButton:hover {{ opacity: 0.9; }}
            QPushButton:pressed {{ opacity: 0.8; }}
        """
        self.submit_button.setStyleSheet(button_style)
        self.prev_button.setStyleSheet(button_style)
        self.next_button.setStyleSheet(button_style)
        
        self.auto_play.setStyleSheet(f"""
            QCheckBox {{ color: {self.text_primary}; spacing: 5px; }}
            QCheckBox::indicator {{ width: 20px; height: 20px; border-radius: 10px; border: 2px solid {self.accent_color}; }}
            QCheckBox::indicator:checked {{ background-color: {self.accent_color}; }}
        """)
        
        self.result_area.setStyleSheet(f"background-color: {self.bg_secondary}; color: {self.text_primary}; border: none; padding: 10px;")
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{ background-color: {self.bg_secondary}; border: none; height: 5px; }}
            QProgressBar::chunk {{ background-color: {self.accent_color}; }}
        """)
        
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(self.shadow_color)
        shadow_effect.setOffset(0, 2)
        self.input_container.setGraphicsEffect(shadow_effect)
        self.result_area.setGraphicsEffect(shadow_effect)
        self.vis_widget.setGraphicsEffect(shadow_effect)
        
        self.statusBar.setStyleSheet(f"background-color: {self.bg_secondary}; color: {self.text_secondary};")
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
        self.update_styles()
        self.update_visualization()
    
    def validate_input_live(self):
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
        msg = QMessageBox(self)
        msg.setStyleSheet(f"""
            QMessageBox {{ background: {self.bg_color}; border-radius: 10px; }}
            QLabel {{ color: {self.text_primary}; }}
            QPushButton {{ background: #ff6b6b; color: white; padding: 8px 20px; border-radius: 15px; }}
        """)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()
    
    def run_simulation(self):
        ref_string = self.validate_input()
        if ref_string is None:
            return
            
        frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
        if frame_size <= 0:
            self.show_error("Frame size must be positive")
            return
        
        from algorithms import fifo, lru, optimal, second_chance, clock
        
        algo_functions = {
            'FIFO': fifo,
            'LRU': lru,
            'Optimal': optimal,
            'Second Chance': second_chance,
            'Clock': clock
        }
        
        self.results = {}
        selected_algo = self.algo_dropdown.currentText()
        if selected_algo == "All Algorithms":
            for algo_name, algo_func in algo_functions.items():
                self.results[algo_name] = algo_func(ref_string, frame_size)
        else:
            self.results[selected_algo] = algo_functions[selected_algo](ref_string, frame_size)
        
        self.current_step = 0
        
        self.statusBar.showMessage("Processing...")
        self.progress_bar.show()
        
        self.progress_value = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)
        
        result_text = f"<h3>Page Replacement Simulation Results</h3>"
        result_text += f"<p><b>Reference String:</b> {' '.join(map(str, ref_string))}</p>"
        result_text += f"<p><b>Frame Size:</b> {frame_size}</p>"
        result_text += "<h4>Detailed Steps:</h4>"
        
        for algo, result in self.results.items():
            result_text += f"<h4>{algo} (Total Faults: {result['faults']})</h4>"
            result_text += "<table border='1' cellpadding='5' style='border-collapse: collapse; width: 100%;'>"
            result_text += "<tr style='background-color: #f2f2f2;'><th>Step</th><th>Page</th><th>Frames Before</th><th>Frames After</th><th>Page Fault</th></tr>"
            
            for i, step in enumerate(result["steps"]):
                frames_before = " ".join(map(str, step["frames_before"])) or "-"
                frames_after = " ".join(map(str, step["frames_after"])) or "-"
                fault = "Yes" if step["page_fault"] else "No"
                result_text += f"<tr><td>{i+1}</td><td>{step['page']}</td><td>{frames_before}</td><td>{frames_after}</td><td>{fault}</td></tr>"
            
            result_text += "</table><br>"
        
        most_efficient = min(self.results, key=lambda x: self.results[x]["faults"])
        result_text += f"<p style='color: {self.accent_color};'><b>Most Efficient:</b> {most_efficient} ({self.results[most_efficient]['faults']} faults)</p>"
        
        self.result_area.setHtml(result_text)
        self.plot_graph({algo: result["faults"] for algo, result in self.results.items()})
        self.setup_visualization(frame_size)
        self.update_visualization()
    
    def setup_visualization(self, frame_size):
        for algo in self.algo_grids:
            for label in self.algo_grids[algo]["labels"]:
                self.algo_grids[algo]["grid"].removeWidget(label)
                label.deleteLater()
        self.algo_grids.clear()
        
        for algo in self.results:
            algo_widget = QWidget()
            algo_layout = QVBoxLayout(algo_widget)
            algo_label = QLabel(algo)
            algo_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            algo_label.setAlignment(Qt.AlignCenter)
            algo_layout.addWidget(algo_label)
            
            grid = QGridLayout()
            labels = []
            for i in range(frame_size):
                label = QLabel("-")
                label.setFont(QFont("Segoe UI", 16))
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(80, 80)  # Larger frame boxes
                label.setStyleSheet(f"background-color: {self.bg_secondary}; border: 2px solid {self.border_color}; border-radius: 5px;")
                grid.addWidget(label, i, 0)
                labels.append(label)
            
            algo_layout.addLayout(grid)
            self.vis_grid_layout.addWidget(algo_widget)
            self.algo_grids[algo] = {"grid": grid, "labels": labels}
    
    def update_visualization(self):
        if not self.results:
            return
        
        if self.current_step >= len(next(iter(self.results.values()))["steps"]):
            self.current_step = len(next(iter(self.results.values()))["steps"]) - 1
        elif self.current_step < 0:
            self.current_step = 0
        
        step_info = f"Step {self.current_step + 1}: Page {next(iter(self.results.values()))['steps'][self.current_step]['page']}"
        self.step_label.setText(step_info)
        
        for algo, result in self.results.items():
            step = result["steps"][self.current_step]
            frames_after = step["frames_after"]
            for i, label in enumerate(self.algo_grids[algo]["labels"]):
                if i < len(frames_after):
                    label.setText(str(frames_after[i]))
                    label.setStyleSheet(f"background-color: {'#ff6b6b' if step['page_fault'] and i == len(frames_after) - 1 else self.bg_secondary}; border: 2px solid {self.border_color}; border-radius: 5px; color: {self.text_primary};")
                else:
                    label.setText("-")
                    label.setStyleSheet(f"background-color: {self.bg_secondary}; border: 2px solid {self.border_color}; border-radius: 5px; color: {self.text_primary};")
    
    def next_step(self):
        if self.results and self.current_step < len(next(iter(self.results.values()))["steps"]) - 1:
            self.current_step += 1
            self.update_visualization()
    
    def prev_step(self):
        if self.results and self.current_step > 0:
            self.current_step -= 1
            self.update_visualization()
    
    def toggle_auto_play(self):
        if self.auto_play.isChecked():
            self.timer = QTimer()
            self.timer.timeout.connect(self.next_step)
            self.timer.start(1000)
        else:
            if hasattr(self, 'timer'):
                self.timer.stop()
    
    def update_progress(self):
        self.progress_value += 10
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.progress_bar.hide()
            self.statusBar.showMessage("Simulation completed successfully")
    
    def plot_graph(self, results):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        algorithms = list(results.keys())
        faults = list(results.values())
        colors = [self.accent_color, '#00ddeb', '#ff6b6b', '#4ecdc4', '#45b7d1'][:len(algorithms)]
        
        bars = ax.bar(algorithms, faults, color=colors, width=0.65, alpha=0.9)
        
        ax.set_title("Page Replacement Algorithm Performance", fontsize=16, pad=20, fontweight='bold')
        ax.set_xlabel("Algorithms", fontsize=12)
        ax.set_ylabel("Page Faults", fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
        ax.set_facecolor(self.bg_color)
        self.figure.set_facecolor('none')
        
        min_faults = min(faults)
        for bar in bars:
            height = bar.get_height()
            if height == min_faults:
                bar.set_edgecolor('green')
                bar.set_linewidth(3)
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom',
                   fontsize=10, fontweight='bold', color=self.text_primary)
        
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    window = PageReplacementSimulator()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
# main.py
import sys
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt

# Placeholder imports (to be replaced with actual imports after merging)
from algorithms import fifo, lru, optimal, second_chance, clock
from gui import MainWindow

def run_algorithms(ref_string, frame_size):
    """Run all page replacement algorithms and return results."""
    results = {
        "FIFO": fifo(ref_string, frame_size),
        "LRU": lru(ref_string, frame_size),
        "Optimal": optimal(ref_string, frame_size),
        "Second Chance": second_chance(ref_string, frame_size),
        "Clock": clock(ref_string, frame_size)
    }
    return results

def analyze_results(results):
    """Analyze results to find the most efficient algorithm."""
    best_algo = min(results, key=results.get)
    return f"Most efficient: {best_algo} with {results[best_algo]} page faults"

def plot_results(results):
    """Generate a bar chart comparing page faults."""
    plt.bar(results.keys(), results.values())
    plt.title("Page Faults by Algorithm")
    plt.xlabel("Algorithm")
    plt.ylabel("Page Faults")
    plt.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # Override run_simulation to use integration logic
    def run_simulation():
        ref_string = window.validate_input()
        if ref_string is None:
            return
        frame_size = int(window.frame_field.text()) if window.frame_field.text().isdigit() else 3
        results = run_algorithms(ref_string, frame_size)
        analysis = analyze_results(results)
        window.result_area.setText(str(results) + "\n" + analysis)
        plot_results(results)
    window.submit_button.clicked.disconnect()
    window.submit_button.clicked.connect(run_simulation)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
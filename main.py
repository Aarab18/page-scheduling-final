def main():
    pass

if __name__ == "__main__":
    main()

from algorithms import fifo, lru, optimal, second_chance, clock
from gui import MainWindow
def run_algorithms(ref_string, frame_size):
    results = {
        "FIFO": fifo(ref_string, frame_size),
        "LRU": lru(ref_string, frame_size),
        "Optimal": optimal(ref_string, frame_size),
        "Second Chance": second_chance(ref_string, frame_size),
        "Clock": clock(ref_string, frame_size)
    }
    return results
def analyze_results(results):
    best_algo = min(results, key=results.get)
    return f"Most efficient: {best_algo} with {results[best_algo]} page faults"
import matplotlib.pyplot as plt

def plot_results(results):
    plt.bar(results.keys(), results.values())
    plt.title("Page Faults by Algorithm")
    plt.xlabel("Algorithm")
    plt.ylabel("Page Faults")
    plt.show()
    
def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# In gui.py, update run_simulation
def run_simulation(self):
    ref_string = self.validate_input()
    frame_size = int(self.frame_field.text()) if self.frame_field.text().isdigit() else 3
    results = run_algorithms(ref_string, frame_size)
    analysis = analyze_results(results)
    self.result_area.setText(str(results) + "\n" + analysis)
    plot_results(results)
    
	
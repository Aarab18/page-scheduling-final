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
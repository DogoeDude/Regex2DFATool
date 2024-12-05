import tkinter as tk
from tkinter import ttk, scrolledtext
from regex_parser import RegexParser
from regex_to_nfa import RegexToNFA
from scanner_generator import ScannerGenerator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import product

class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer Generator")
        self.root.geometry("1600x900")  # Increased window size
        self.scanner = None
        self.setup_gui()

    def setup_gui(self):
        # Create main frames
        control_frame = ttk.Frame(self.root, padding="10")
        visualization_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        visualization_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Split control frame into upper and lower sections
        upper_frame = ttk.Frame(control_frame)
        lower_frame = ttk.Frame(control_frame)
        upper_frame.pack(fill=tk.BOTH, expand=True)
        lower_frame.pack(fill=tk.BOTH, expand=True)

        # Regex Input Section (Upper Frame)
        input_frame = ttk.LabelFrame(upper_frame, text="Regular Expression Input", padding="5")
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="Enter Regular Expression:").pack(anchor=tk.W)
        self.regex_entry = ttk.Entry(input_frame, width=50)
        self.regex_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Generate Button
        ttk.Button(input_frame, text="Generate DFA", command=self.generate_dfa).pack(pady=5)

        # Test Input Section
        test_frame = ttk.LabelFrame(upper_frame, text="Test Input", padding="5")
        test_frame.pack(fill=tk.X, pady=5)

        ttk.Label(test_frame, text="Enter string to test:").pack(anchor=tk.W)
        self.test_entry = ttk.Entry(test_frame, width=50)
        self.test_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Test Button
        ttk.Button(test_frame, text="Test Input", command=self.test_input).pack(pady=5)

        # Results Section
        results_frame = ttk.LabelFrame(upper_frame, text="Test Results", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=6, width=50)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Accepted Strings Section (Lower Frame)
        accepted_frame = ttk.LabelFrame(lower_frame, text="Accepted Strings", padding="5")
        accepted_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Add length control
        length_frame = ttk.Frame(accepted_frame)
        length_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(length_frame, text="Max string length:").pack(side=tk.LEFT)
        self.length_var = tk.StringVar(value="3")
        self.length_entry = ttk.Entry(length_frame, textvariable=self.length_var, width=5)
        self.length_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(length_frame, text="Generate Strings", command=self.generate_accepted_strings).pack(side=tk.LEFT, padx=5)

        # Accepted strings text area
        self.accepted_text = scrolledtext.ScrolledText(accepted_frame, height=10, width=50)
        self.accepted_text.pack(fill=tk.BOTH, expand=True)

        # DFA Visualization Section
        viz_frame = ttk.LabelFrame(visualization_frame, text="DFA Visualization", padding="5")
        viz_frame.pack(fill=tk.BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_accepted_strings(self):
        if not self.scanner or not self.scanner.dfa:
            self.log_result("Please generate a DFA first.")
            return

        try:
            max_length = int(self.length_var.get())
            if max_length > 10:  # Limit maximum length to prevent hanging
                self.log_result("Maximum length limited to 10 to prevent excessive computation.")
                max_length = 10
        except ValueError:
            self.log_result("Please enter a valid number for maximum length.")
            return

        alphabet = sorted(list(self.scanner.dfa[0].transitions.keys()))
        accepted_strings = []

        # Generate strings of different lengths
        for length in range(max_length + 1):
            for combination in product(alphabet, repeat=length):
                test_string = ''.join(combination)
                if self.scanner.test_input(test_string):
                    accepted_strings.append(test_string)

        # Clear and update the accepted strings text area
        self.accepted_text.delete('1.0', tk.END)
        if accepted_strings:
            for i, string in enumerate(accepted_strings, 1):
                if string == '':
                    self.accepted_text.insert(tk.END, f"{i}. ε (empty string)\n")
                else:
                    self.accepted_text.insert(tk.END, f"{i}. {string}\n")
        else:
            self.accepted_text.insert(tk.END, "No strings accepted up to the specified length.")

    def generate_dfa(self):
        regex = self.regex_entry.get()
        if not regex:
            self.log_result("Please enter a regular expression.")
            return

        try:
            # Parse regex
            parser = RegexParser()
            parsed_regex = parser.parse(regex)

            # Convert to NFA
            converter = RegexToNFA()
            nfa = converter.convert(parsed_regex)

            # Convert to DFA and create scanner
            self.scanner = ScannerGenerator()
            self.scanner.nfa_to_dfa(nfa)

            # Clear previous visualization
            self.ax.clear()
            
            # Draw new DFA
            self.scanner.visualize_dfa(ax=self.ax)
            self.canvas.draw()

            self.log_result(f"DFA generated successfully for regex: {regex}")
            
            # Generate accepted strings automatically
            self.generate_accepted_strings()

        except Exception as e:
            self.log_result(f"Error generating DFA: {str(e)}")

    def test_input(self):
        if not self.scanner:
            self.log_result("Please generate a DFA first.")
            return

        test_string = self.test_entry.get()
        if not test_string:
            self.log_result("Please enter a test string.")
            return

        try:
            is_accepted = self.scanner.test_input(test_string)
            result = "accepted" if is_accepted else "rejected"
            self.log_result(f"Input '{test_string}' is {result} by the DFA")
        except Exception as e:
            self.log_result(f"Error testing input: {str(e)}")

    def log_result(self, message):
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)

def main():
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
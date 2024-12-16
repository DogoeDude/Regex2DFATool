import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import random
import subprocess #open our default file viewer
import os #for handling os systems
import itertools #used for generating possible combinations from a string

from FAdo.reex import str2regexp
from FAdo.fa import *

from NFA_DFA import nfa_to_dfa
from RGX_NFA import regex_to_nfa 
from DFA_MIN import minimize_dfa
def regex_to_nfa(regex):
    try:
        # Parse the regex into a FAdo regex object
        parsed_regex = str2regexp(regex)
        
        # Convert regex to NFA
        nfa = parsed_regex.toNFA()
        
        # Rename states for readability
        nfa.renameStates()
        
        return nfa
    except Exception as e:
        print(f"Error processing the regex: {e}")
        return None


def nfa_to_dfa(nfa):
    try:
        # Convert the NFA to DFA (no minimization)
        dfa = nfa.toDFA()
        
        return dfa
    except Exception as e:
        print(f"Error during NFA to DFA conversion: {e}")
        return None


def minimize_dfa(dfa):
    try:
        # Minimize the DFA
        minimized_dfa = dfa.minimal()
        return minimized_dfa
    except Exception as e:
        print(f"Error during DFA minimization: {e}")
        return None


class DFAScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("DFA Regex Scanner")
        master.geometry("800x700")

        # Regex Input Frame
        self.regex_frame = tk.Frame(master)
        self.regex_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(self.regex_frame, text="Regular Expression:").pack(side="left")
        self.regex_entry = tk.Entry(self.regex_frame, width=50)
        self.regex_entry.pack(side="left", expand=True, fill="x", padx=10)

        # Buttons Frame
        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=10, padx=10, fill="x")

        # Convert to Min DFA Button
        self.convert_btn = tk.Button(
            self.buttons_frame, text="Convert to Min DFA", command=self.convert_to_min_dfa
        )
        self.convert_btn.pack(side="left", padx=5)

        # Show Graph Button
        self.show_graph_btn = tk.Button(
            self.buttons_frame,
            text="Show DFA Graph",
            command=self.show_dfa_graph,
            state=tk.DISABLED,
        )
        self.show_graph_btn.pack(side="left", padx=5)

        # Test Code Button
        self.test_code_btn = tk.Button(
            self.buttons_frame,
            text="Test Code",
            command=self.test_code,
            state=tk.DISABLED,
        )
        self.test_code_btn.pack(side="left", padx=5)

        # Generate Random/Enumerated Code Button
        self.generate_code_btn = tk.Button(
            self.buttons_frame,
            text="Generate Codes",
            command=self.ask_code_length,
            state=tk.DISABLED,
        )
        self.generate_code_btn.pack(side="left", padx=5)

        # DFA Information Frame
        self.info_frame = tk.Frame(master)
        self.info_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=15, wrap=tk.WORD)
        self.info_text.pack(fill="both", expand=True)

        # Results Frame
        self.results_frame = tk.Frame(master)
        self.results_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.results_text = scrolledtext.ScrolledText(
            self.results_frame, height=10, wrap=tk.WORD
        )
        self.results_text.pack(fill="both", expand=True)

        # Class variables
        self.minimized_dfa = None
        self.alphabet = set()

    def convert_to_min_dfa(self):
        # Clear previous results
        self.info_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)

        # Reset button states
        self.show_graph_btn.config(state=tk.DISABLED)
        self.test_code_btn.config(state=tk.DISABLED)
        self.generate_code_btn.config(state=tk.DISABLED)

        # Get regex from entry
        regex = self.regex_entry.get()

        try:
            # Generate NFA from regex using the custom function
            nfa = regex_to_nfa(regex)

            if nfa:
                # Convert NFA to DFA using the custom function
                dfa = nfa_to_dfa(nfa)

                if dfa:
                    # Minimize the DFA using the custom function
                    minimized_dfa = minimize_dfa(dfa)
                    self.minimized_dfa = minimized_dfa

                    # Determine alphabet
                    self.alphabet = set(
                        symbol
                        for state in minimized_dfa.delta
                        for symbol in minimized_dfa.delta[state].keys()
                    )

                    # Display DFA Information
                    self.info_text.insert(tk.END, f"Minimized DFA for Regex: {regex}\n\n")
                    self.info_text.insert(tk.END, f"States: {minimized_dfa.States}\n")
                    self.info_text.insert(tk.END, f"Initial State: {minimized_dfa.Initial}\n")
                    self.info_text.insert(tk.END, f"Final States: {minimized_dfa.Final}\n\n")

                    self.info_text.insert(tk.END, "Transitions:\n")
                    for state in minimized_dfa.delta:
                        for symbol, next_state in minimized_dfa.delta[state].items():
                            self.info_text.insert(
                                tk.END, f"{state} --{symbol}--> {next_state}\n"
                            )

                    # Enable buttons
                    self.show_graph_btn.config(state=tk.NORMAL)
                    self.test_code_btn.config(state=tk.NORMAL)
                    self.generate_code_btn.config(state=tk.NORMAL)

                else:
                    messagebox.showerror("Error", "Failed to convert NFA to DFA")
            else:
                messagebox.showerror("Error", "Failed to generate NFA from regex")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_dfa_graph(self):
        if not self.minimized_dfa:
            messagebox.showwarning("Warning", "Please convert to Min DFA first")
            return

        try:
            # Create a temporary file to save the graph
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file.close()  # Close the file so it can be opened by other applications

            # Use display method to generate graph
            self.minimized_dfa.display(temp_file.name)

            # Open the generated PDF
            if os.name == 'nt':  # Windows
                os.startfile(temp_file.name)  # This should open the file with the default PDF viewer
            elif os.name == 'posix':  # macOS and Linux
                subprocess.call(('open', temp_file.name))
            else:
                messagebox.showinfo("Info", f"Graph saved to {temp_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not display graph: {str(e)}")


    def test_code(self):
        if not self.minimized_dfa:
            messagebox.showwarning("Warning", "Please convert to Min DFA first")
            return

        # Prompt for test code
        test_string = simpledialog.askstring("Test Code", "Enter the code to test:")
        
        if not test_string:
            return
        
        # Test string acceptance
        current_state = self.minimized_dfa.Initial
        accepted = True

        for char in test_string:
            if char not in self.alphabet:
                accepted = False
                break
            
            if current_state not in self.minimized_dfa.delta or \
               char not in self.minimized_dfa.delta[current_state]:
                accepted = False
                break
            
            current_state = self.minimized_dfa.delta[current_state][char]

        # Check if final state is reached
        accepted = accepted and current_state in self.minimized_dfa.Final

        # Show result
        result_msg = f"Code: {test_string}\n"
        result_msg += f"Accepted: {'Yes' if accepted else 'No'}"
        
        if accepted:
            messagebox.showinfo("Code Test", result_msg)
        else:
            messagebox.showwarning("Code Test", result_msg)

    def ask_code_length(self):
        # Ask the user for the length of the code
        length_str = simpledialog.askstring("Code Length", "Enter the length of codes to generate:")
        
        if not length_str or not length_str.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid numeric length.")
            return
        
        length = int(length_str)
        self.generate_codes(length)

    def generate_codes(self, length):
        if not self.minimized_dfa:
            messagebox.showwarning("Warning", "Please convert to Min DFA first")
            return

        # Clear previous results
        self.results_text.delete(1.0, tk.END)

        # Generate random accepted codes
        self.results_text.insert(tk.END, f"Random Accepted Codes (Length {length}):\n")
        for _ in range(5):
            random_code = self.generate_random_accepted_string(length)
            if random_code:
                self.results_text.insert(tk.END, random_code + "\n")
            else:
                self.results_text.insert(tk.END, "No random codes generated.\n")

        # Enumerate all accepted codes
        self.results_text.insert(tk.END, f"\nEnumerated Accepted Codes (Length {length}):\n")
        enumerated_codes = self.generate_enumerated_codes(length)
        if enumerated_codes:
            for code in enumerated_codes:
                self.results_text.insert(tk.END, code + "\n")
        else:
            self.results_text.insert(tk.END, "No enumerated codes found.\n")


    def generate_random_accepted_string(self, length):
        if not self.minimized_dfa or length <= 0:
            return None

        for _ in range(100):  # Attempt up to 100 times to find a valid string
            current_state = self.minimized_dfa.Initial
            generated_string = ""

            for _ in range(length):
                # Check if there are valid transitions from the current state
                if current_state not in self.minimized_dfa.delta or not self.minimized_dfa.delta[current_state]:
                    break  # No valid transitions, abandon this attempt

                # Choose a random valid transition
                valid_transitions = list(self.minimized_dfa.delta[current_state].items())
                symbol, next_state = random.choice(valid_transitions)
                generated_string += symbol
                current_state = next_state

            # Verify the string ends in a final state
            if current_state in self.minimized_dfa.Final:
                return generated_string

        # If no valid string is found after 100 attempts, return None
        return None



    def generate_enumerated_codes(self, length):
        if not self.minimized_dfa or not self.alphabet:
            return []

        codes = []
        for code in itertools.product(self.alphabet, repeat=length):
            code_str = ''.join(code)
            if self.test_string_acceptance(code_str):
                codes.append(code_str)
        return codes


    def test_string_acceptance(self, test_string):
        if not self.minimized_dfa:
            return False

        current_state = self.minimized_dfa.Initial

        for char in test_string:
            # Check if the character is in the alphabet
            if char not in self.alphabet:
                return False

            # Follow the transition
            if current_state not in self.minimized_dfa.delta or \
            char not in self.minimized_dfa.delta[current_state]:
                return False

            current_state = self.minimized_dfa.delta[current_state][char]

        # Check if the current state is a final state
        return current_state in self.minimized_dfa.Final


if __name__ == "__main__":
    root = tk.Tk()
    app = DFAScannerApp(root)
    root.mainloop()

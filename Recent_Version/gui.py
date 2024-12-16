import tkinter as tk
from tkinter import ttk, scrolledtext
from regex_parser import RegexParser
from regex_to_nfa import RegexToNFA
from scanner_generator import ScannerGenerator
from PIL import Image, ImageTk
import io
from itertools import product
from collections import deque

class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer Generator")
        self.root.geometry("1200x800")
        
        self.scanner = None
        self.current_graph = "DFA"
        self.nfa = None
        self.original_image = None
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

        # Regex Input Section
        input_frame = ttk.LabelFrame(upper_frame, text="Regular Expression Input", padding="5")
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="Enter Regular Expression:").pack(anchor=tk.W)
        self.regex_entry = ttk.Entry(input_frame, width=50)
        self.regex_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(input_frame, text="Generate DFA", command=self.generate_dfa).pack(pady=5)

        # Test Input Section
        test_frame = ttk.LabelFrame(upper_frame, text="Test Input", padding="5")
        test_frame.pack(fill=tk.X, pady=5)

        ttk.Label(test_frame, text="Enter string to test:").pack(anchor=tk.W)
        self.test_entry = ttk.Entry(test_frame, width=50)
        self.test_entry.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(test_frame, text="Test Input", command=self.test_input).pack(pady=5)

        # Add animation controls to test frame
        self.animate_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(test_frame, text="Animate", variable=self.animate_var).pack(side=tk.LEFT, padx=5)
        self.animation_speed = tk.Scale(test_frame, from_=0.5, to=2.0, resolution=0.1, 
                                      orient=tk.HORIZONTAL, label="Animation Speed")
        self.animation_speed.set(1.0)
        self.animation_speed.pack(side=tk.LEFT, padx=5)

        # Results Section
        results_frame = ttk.LabelFrame(upper_frame, text="Test Results", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.results_text = scrolledtext.ScrolledText(results_frame, height=6, width=50)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Accepted Strings Section
        accepted_frame = ttk.LabelFrame(lower_frame, text="Accepted Strings", padding="5")
        accepted_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        length_frame = ttk.Frame(accepted_frame)
        length_frame.pack(fill=tk.X, pady=5)
        ttk.Label(length_frame, text="Max string length:").pack(side=tk.LEFT)
        self.length_var = tk.StringVar(value="3")
        self.length_entry = ttk.Entry(length_frame, textvariable=self.length_var, width=5)
        self.length_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(length_frame, text="Generate Strings", 
                  command=self.generate_accepted_strings).pack(side=tk.LEFT, padx=5)

        self.accepted_text = scrolledtext.ScrolledText(accepted_frame, height=10, width=50)
        self.accepted_text.pack(fill=tk.BOTH, expand=True)

        # DFA Visualization Section
        viz_frame = ttk.LabelFrame(visualization_frame, text="DFA Visualization", padding="5")
        viz_frame.pack(fill=tk.BOTH, expand=True)

        # Add zoom controls
        zoom_frame = ttk.Frame(viz_frame)
        zoom_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(zoom_frame, text="Zoom In (+)", command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="Zoom Out (-)", command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="Reset Zoom", command=self.reset_zoom).pack(side=tk.LEFT, padx=5)

        # Create canvas with scrollbars
        canvas_frame = ttk.Frame(viz_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(canvas_frame, bg='white',
                              xscrollcommand=h_scrollbar.set,
                              yscrollcommand=v_scrollbar.set)
        
        # Configure scrollbars
        h_scrollbar.config(command=self.canvas.xview)
        v_scrollbar.config(command=self.canvas.yview)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize zoom level
        self.zoom_level = 1.0
        self.original_image = None

    def update_visualization(self, dot):
        # Render the graph
        png_data = dot.pipe(format='png')
        
        # Convert to PIL Image and store as original
        self.original_image = Image.open(io.BytesIO(png_data))
        
        # Calculate initial scaling to fit the canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.original_image.size
        
        # Calculate scale factor
        scale = min(canvas_width/img_width, canvas_height/img_height)
        self.zoom_level = scale
        
        # Resize image
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_image = self.original_image.resize(
            (new_width, new_height), 
            Image.Resampling.LANCZOS
        )
        
        # Convert to PhotoImage and store reference
        self.photo = ImageTk.PhotoImage(resized_image)
        
        # Update canvas
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width//2, canvas_height//2,
            image=self.photo,
            anchor=tk.CENTER
        )
        
        # Update canvas scrollregion
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

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

            # Generate and display visualization
            dot = self.scanner.visualize_dfa()
            self.update_visualization(dot)

            # Log information about states
            total_states = len(self.scanner.dfa)
            dead_states = sum(1 for state in self.scanner.dfa if self.scanner.is_dead_state(state))
            self.log_result(f"DFA generated successfully for regex: {regex}")
            self.log_result(f"Total states: {total_states} (including {dead_states} dead state{'s' if dead_states != 1 else ''})")
            
            # Generate accepted strings automatically
            self.generate_accepted_strings()

        except Exception as e:
            self.log_result(f"Error generating DFA: {str(e)}")

    def generate_accepted_strings(self):
        if not self.scanner or not self.scanner.dfa:
            self.log_result("Please generate a DFA first.")
            return

        try:
            max_length = int(self.length_var.get())
            if max_length > 10:
                self.log_result("Maximum length limited to 10 to prevent excessive computation.")
                max_length = 10
        except ValueError:
            self.log_result("Please enter a valid number for maximum length.")
            return

        # Get alphabet from all DFA states
        alphabet = set()
        for state in self.scanner.dfa:
            alphabet.update(state.transitions.keys())
        alphabet = sorted(list(alphabet))

        if not alphabet:
            self.log_result("No transitions found in DFA.")
            return

        accepted_strings = []
        
        # Check for empty string acceptance (if initial state is final)
        if self.scanner.dfa[0].is_final:
            accepted_strings.append('')

        # Generate strings using BFS to avoid generating unnecessary strings
        queue = deque([('', self.scanner.dfa[0])])
        seen_states = set()

        while queue:
            current_string, current_state = queue.popleft()
            
            # Skip if string length exceeds maximum
            if len(current_string) > max_length:
                continue

            # Add string to accepted list if in final state
            if current_state.is_final and current_string:
                accepted_strings.append(current_string)

            # Only continue if we can add more characters
            if len(current_string) < max_length:
                # Try each symbol in the alphabet
                for symbol in alphabet:
                    if symbol in current_state.transitions:
                        next_state = current_state.transitions[symbol]
                        new_string = current_string + symbol
                        state_string_pair = (new_string, next_state)
                        
                        # Only add if we haven't seen this exact state with this exact string before
                        if state_string_pair not in seen_states:
                            seen_states.add(state_string_pair)
                            queue.append(state_string_pair)

        # Sort strings by length and then alphabetically
        accepted_strings.sort(key=lambda x: (len(x), x))

        # Clear and update the accepted strings text area
        self.accepted_text.delete('1.0', tk.END)
        
        if accepted_strings:
            for i, string in enumerate(accepted_strings, 1):
                if string == '':
                    self.accepted_text.insert(tk.END, f"{i}. ε (empty string)\n")
                else:
                    self.accepted_text.insert(tk.END, f"{i}. {string}\n")
            self.log_result(f"Generated {len(accepted_strings)} accepted strings")
        else:
            self.accepted_text.insert(tk.END, "No strings accepted up to the specified length.")
            self.log_result("No accepted strings found")

    def test_input(self):
        if not self.scanner:
            self.log_result("Please generate a DFA first.")
            return

        test_string = self.test_entry.get()
        if not test_string:
            self.log_result("Please enter a test string.")
            return

        try:
            if self.animate_var.get():
                self.animate_string_processing(test_string)
            else:
                is_accepted = self.scanner.test_input(test_string)
                result = "accepted" if is_accepted else "rejected"
                self.log_result(f"Input '{test_string}' is {result} by the DFA")
        except Exception as e:
            self.log_result(f"Error testing input: {str(e)}")

    def animate_string_processing(self, input_string):
        steps = self.scanner.process_string_step_by_step(input_string)
        
        def animate_step(step_index):
            if step_index >= len(steps):
                # Animation finished - show final result with special highlighting
                current_state = steps[-1][0]
                if current_state is not None:
                    is_accepted = self.scanner.state_map[current_state].is_final
                    result = "accepted" if is_accepted else "rejected"
                    
                    # Show final message with color
                    result_color = "green" if is_accepted else "red"
                    self.results_text.tag_config("result", foreground=result_color)
                    self.log_result(f"Input '{input_string}' is {result} by the DFA", "result")
                    
                    # Show final state with special highlighting
                    dot = self.scanner.visualize_dfa(
                        highlight_state=current_state,
                        highlight_transition=None
                    )
                    self.update_visualization(dot)
                return

            current_state, transition = steps[step_index]
            
            if current_state is None:
                self.log_result("Input rejected - no valid transition", "error")
                return
            
            # Update visualization with smooth transition
            dot = self.scanner.visualize_dfa(
                highlight_state=current_state,
                highlight_transition=transition
            )
            self.update_visualization(dot)
            
            # Add position indicator in results with improved formatting
            if transition:
                char = transition[0]
                pos = step_index
                input_display = input_string
                indicator = ' ' * pos + '^'
                self.log_result(f"Processing: {input_display}\n{indicator}")
            
            # Calculate delay based on animation speed with smoother timing
            base_delay = 800  # Slightly faster base delay
            delay = int(base_delay / self.animation_speed.get())
            
            # Schedule next step with smooth transition
            self.root.after(delay, lambda: animate_step(step_index + 1))

        # Clear previous results and set up text tags
        self.results_text.delete('1.0', tk.END)
        self.results_text.tag_config("error", foreground="red")
        self.results_text.tag_config("processing", foreground="blue")
        self.log_result(f"Testing string: {input_string}", "processing")
        
        # Start animation
        animate_step(0)

    def log_result(self, message, tag=None):
        self.results_text.insert(tk.END, message + "\n", tag)
        self.results_text.see(tk.END)

    def zoom_in(self):
        self.zoom_level *= 1.2
        self.update_zoom()

    def zoom_out(self):
        self.zoom_level /= 1.2
        self.update_zoom()

    def reset_zoom(self):
        self.zoom_level = 1.0
        self.update_zoom()

    def update_zoom(self):
        if self.original_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Get original image dimensions
        img_width, img_height = self.original_image.size
        
        # Calculate new dimensions
        new_width = int(img_width * self.zoom_level)
        new_height = int(img_height * self.zoom_level)
        
        # Resize image
        resized_image = self.original_image.resize(
            (new_width, new_height), 
            Image.Resampling.LANCZOS
        )
        
        # Update PhotoImage
        self.photo = ImageTk.PhotoImage(resized_image)
        
        # Update canvas
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width//2, canvas_height//2,
            image=self.photo,
            anchor=tk.CENTER
        )
        
        # Update canvas scrollregion
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

def main():
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
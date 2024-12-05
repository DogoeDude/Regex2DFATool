from typing import Dict, Set
from regex_parser import RegexParser
from regex_to_nfa import NFA, State
from graphviz import Digraph
from PIL import Image
from collections import deque
import io

class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states)
        self.transitions = {}
        self.is_final = any(state.is_final for state in nfa_states)
        self.state_id = None

class ScannerGenerator:
    def __init__(self):
        self.dfa = None
        self.state_map = {}
        
    def add_token(self, token_name: str, regex: str) -> None:
        self.token_definitions[token_name] = regex
        
    def generate_scanner(self, output_file: str) -> None:
        # Generate the scanner code
        code = self._generate_scanner_code()
        
        with open(output_file, 'w') as f:
            f.write(code)
            
    def _generate_scanner_code(self) -> str:
        # Template for the generated scanner
        return '''
class Scanner:
    def __init__(self, input_text: str):
        self.text = input_text
        self.position = 0
        
    def next_token(self):
        while self.position < len(self.text):
            # Skip whitespace
            while self.position < len(self.text) and self.text[self.position].isspace():
                self.position += 1
                
            if self.position >= len(self.text):
                return None
                
            # Try to match each token definition
            current_char = self.text[self.position]
            
            # Add generated matching logic here
            
        return None
''' 

    def epsilon_closure(self, nfa_states):
        closure = set(nfa_states)
        stack = list(nfa_states)
        
        while stack:
            state = stack.pop()
            for eps_state in state.epsilon_transitions:
                if eps_state not in closure:
                    closure.add(eps_state)
                    stack.append(eps_state)
        
        return closure

    def nfa_to_dfa(self, nfa):
        dfa_states = []
        unmarked_states = deque()
        
        # Create initial state
        start_closure = self.epsilon_closure({nfa.start_state})
        start_state = DFAState(start_closure)
        dfa_states.append(start_state)
        unmarked_states.append(start_state)
        
        while unmarked_states:
            current_state = unmarked_states.popleft()
            
            for symbol in nfa.alphabet:
                next_states = set()
                for nfa_state in current_state.nfa_states:
                    if symbol in nfa_state.transitions:
                        next_states.update(nfa_state.transitions[symbol])
                
                if next_states:
                    next_states = self.epsilon_closure(next_states)
                    new_state = DFAState(next_states)
                    
                    # Check if this state already exists
                    exists = False
                    for existing_state in dfa_states:
                        if existing_state.nfa_states == new_state.nfa_states:
                            new_state = existing_state
                            exists = True
                            break
                    
                    if not exists:
                        dfa_states.append(new_state)
                        unmarked_states.append(new_state)
                    
                    current_state.transitions[symbol] = new_state
        
        # Assign state IDs
        for i, state in enumerate(dfa_states):
            state.state_id = i
            self.state_map[state.state_id] = state
        
        self.dfa = dfa_states
        return dfa_states

    def visualize_dfa(self):
        if not self.dfa:
            return None

        # Create a new directed graph
        dot = Digraph(comment='DFA Visualization')
        dot.attr(rankdir='LR')  # Left to right layout
        
        # Add nodes (states)
        for state in self.dfa:
            # Node attributes
            attrs = {
                'shape': 'doublecircle' if state.is_final else 'circle',
                'style': 'filled',
                'fillcolor': 'lightgreen' if state.is_final else 'lightblue',
                'fontname': 'Arial'
            }
            
            # Add state node
            dot.node(f'q{state.state_id}', f'q{state.state_id}', **attrs)
            
            # Add transitions
            for symbol, next_state in state.transitions.items():
                dot.edge(f'q{state.state_id}', 
                        f'q{next_state.state_id}',
                        label=symbol,
                        fontname='Arial')

        # Add initial state marker
        dot.node('start', '', shape='none')
        dot.edge('start', 'q0', '')

        # Set graph attributes
        dot.attr(bgcolor='white')
        dot.attr(pad='0.5')

        return dot

    def test_input(self, input_string):
        if not self.dfa:
            raise Exception("DFA not generated yet")
        
        current_state = self.state_map[0]  # Start state
        
        for char in input_string:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char]
        
        return current_state.is_final
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
        
        # Get complete alphabet from NFA
        alphabet = set()
        for state in nfa.states:
            alphabet.update(state.transitions.keys())
        
        # Assign state IDs
        for i, state in enumerate(dfa_states):
            state.state_id = i
            self.state_map[state.state_id] = state
        
        self.dfa = dfa_states

        # After converting NFA to DFA, add dead state
        self.add_dead_state()

    def add_dead_state(self):
        # Get all symbols from existing transitions
        alphabet = set()
        for state in self.dfa:
            alphabet.update(state.transitions.keys())
        
        # Create dead state
        dead_state = DFAState(set())  # Empty set of NFA states
        dead_state.state_id = len(self.dfa)
        dead_state.is_final = False
        
        # Add self-loops for all symbols to dead state
        for symbol in alphabet:
            dead_state.transitions[symbol] = dead_state
        
        # Add transitions to dead state from other states
        dead_state_needed = False
        for state in self.dfa:
            for symbol in alphabet:
                if symbol not in state.transitions:
                    state.transitions[symbol] = dead_state
                    dead_state_needed = True
        
        # Only add dead state if it's needed
        if dead_state_needed:
            self.dfa.append(dead_state)
            self.state_map[dead_state.state_id] = dead_state

    def visualize_dfa(self, highlight_state=None, highlight_transition=None):
        dot = Digraph()
        dot.attr(rankdir='LR')
        
        # Add nodes
        for state in self.dfa:
            node_name = str(state.state_id)
            shape = 'doublecircle' if state.is_final else 'circle'
            color = 'red' if state.state_id == highlight_state else 'black'
            
            # Add label "DEAD" for dead state
            label = f"q{state.state_id}"
            if self.is_dead_state(state):
                label += "\n(DEAD)"
                
            dot.node(node_name, label, shape=shape, color=color)
        
        # Get all symbols from the DFA
        alphabet = set()
        for state in self.dfa:
            alphabet.update(state.transitions.keys())
        
        # Add edges with combined transitions to dead states
        for state in self.dfa:
            # Group transitions by destination state
            transitions_by_dest = {}
            for symbol, next_state in state.transitions.items():
                if next_state not in transitions_by_dest:
                    transitions_by_dest[next_state] = []
                transitions_by_dest[next_state].append(symbol)
            
            # Add edges for each destination
            for next_state, symbols in transitions_by_dest.items():
                # Skip self-loops in dead state
                if self.is_dead_state(state) and state == next_state:
                    continue
                    
                # Determine if this transition should be highlighted
                is_highlighted = (highlight_state == state.state_id and 
                                highlight_transition is not None and 
                                highlight_transition[0] in symbols and 
                                highlight_transition[1] == next_state.state_id)
                
                # Format the label - always show grouped symbols
                if len(symbols) > 1:
                    # Sort symbols for consistent display
                    symbols.sort()
                    label = ','.join(symbols)  # Use commas to separate symbols
                else:
                    label = symbols[0]
                
                # Add the edge
                dot.edge(str(state.state_id), str(next_state.state_id), 
                        label=label, 
                        color='red' if is_highlighted else 'black')
        
        return dot

    def is_dead_state(self, state):
        # A state is a dead state if:
        # 1. It's not final
        # 2. All transitions lead back to itself
        if state.is_final:
            return False
        
        return all(next_state == state for next_state in state.transitions.values())

    def test_input(self, input_string):
        if not self.dfa:
            raise Exception("DFA not generated yet")
        
        current_state = self.state_map[0]  # Start state
        
        for char in input_string:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char]
        
        return current_state.is_final

    def process_string_step_by_step(self, input_string):
        if not self.dfa:
            raise Exception("DFA not generated yet")
        
        steps = []
        current_state = self.state_map[0]  # Start state
        steps.append((current_state.state_id, None))  # Initial state
        
        for i, char in enumerate(input_string):
            if char not in current_state.transitions:
                return steps + [(None, None)]  # Indicate rejection
            next_state = current_state.transitions[char]
            steps.append((current_state.state_id, (char, next_state.state_id)))
            current_state = next_state
        
        steps.append((current_state.state_id, None))  # Final state
        return steps

    def visualize_nfa(self, nfa, highlight_states=None, highlight_transition=None):
        if not nfa:
            return None

        dot = Digraph(comment='NFA Visualization')
        dot.attr(rankdir='LR')
        
        visited_states = set()
        shown_transitions = set()  # Keep track of transitions we've already shown
        
        def add_state_to_graph(state):
            if state in visited_states:
                return
            visited_states.add(state)
            
            # Node attributes
            attrs = {
                'shape': 'doublecircle' if state.is_final else 'circle',
                'style': 'filled',
                'fontname': 'Arial'
            }
            
            if highlight_states and state in highlight_states:
                attrs['fillcolor'] = 'yellow'
                attrs['penwidth'] = '3'
            else:
                attrs['fillcolor'] = 'lightgreen' if state.is_final else 'lightblue'
            
            state_name = f'q{state.state_id}'
            dot.node(state_name, state_name, **attrs)
            
            # Add normal transitions
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    transition_key = (state.state_id, symbol, next_state.state_id)
                    if transition_key not in shown_transitions:
                        shown_transitions.add(transition_key)
                        edge_attrs = {
                            'fontname': 'Arial',
                            'label': symbol
                        }
                        
                        if (highlight_transition and 
                            state in highlight_states and 
                            next_state in highlight_transition[1] and 
                            symbol == highlight_transition[0]):
                            edge_attrs['color'] = 'red'
                            edge_attrs['penwidth'] = '2'
                        
                        dot.edge(f'q{state.state_id}', 
                                f'q{next_state.state_id}',
                                **edge_attrs)
                        
                        add_state_to_graph(next_state)
            
            # Add direct epsilon transitions only
            for eps_state in state.epsilon_transitions:
                transition_key = (state.state_id, 'ε', eps_state.state_id)
                if transition_key not in shown_transitions:
                    shown_transitions.add(transition_key)
                    edge_attrs = {
                        'fontname': 'Arial',
                        'label': 'ε',
                        'style': 'dashed'
                    }
                    
                    if (highlight_transition and 
                        state in highlight_states and 
                        eps_state in highlight_transition[1] and 
                        highlight_transition[0] is None):
                        edge_attrs['color'] = 'red'
                        edge_attrs['penwidth'] = '2'
                    
                    dot.edge(f'q{state.state_id}', 
                            f'q{eps_state.state_id}',
                            **edge_attrs)
                    
                    add_state_to_graph(eps_state)

        add_state_to_graph(nfa.start_state)
        
        dot.node('start', '', shape='none')
        dot.edge('start', f'q{nfa.start_state.state_id}', '')
        
        dot.attr(bgcolor='white')
        dot.attr(pad='0.5')
        
        return dot

    def process_nfa_string_step_by_step(self, nfa, input_string):
        if not nfa:
            raise Exception("NFA not provided")
        
        steps = []
        current_states = self.epsilon_closure({nfa.start_state})
        steps.append((list(current_states), None))  # Initial state(s)
        
        for char in input_string:
            next_states = set()
            for state in current_states:
                if char in state.transitions:
                    next_states.update(state.transitions[char])
            
            if not next_states:
                return steps + [([], None)]  # Indicate rejection
            
            # Add epsilon closure of next states
            next_states = self.epsilon_closure(next_states)
            steps.append((list(current_states), (char, list(next_states))))
            current_states = next_states
        
        steps.append((list(current_states), None))  # Final state(s)
        return steps
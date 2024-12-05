from typing import Dict, Set
from regex_parser import RegexParser
from regex_to_nfa import NFA, State
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

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

    def visualize_dfa(self, ax=None):
        G = nx.DiGraph()
        
        # Add nodes
        for state in self.dfa:
            G.add_node(state.state_id, 
                      final=state.is_final,
                      initial=state.state_id == 0)
        
        # Add edges
        for state in self.dfa:
            for symbol, next_state in state.transitions.items():
                G.add_edge(state.state_id, next_state.state_id, label=symbol)
        
        # Use provided axes or create new figure
        if ax is None:
            plt.figure(figsize=(12, 8))
            ax = plt.gca()
        
        pos = nx.spring_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, 
                             node_color=['lightblue' if not G.nodes[n]['final'] else 'lightgreen' for n in G.nodes()],
                             node_size=2000,
                             ax=ax)
        
        # Draw initial state marker
        initial_state = [n for n, attr in G.nodes(data=True) if attr['initial']][0]
        ax.plot([pos[initial_state][0] - 0.15], [pos[initial_state][1]], 
                marker='>', color='black', markersize=20)
        
        # Draw edges and labels
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        ax.set_title("DFA Visualization")
        ax.axis('off')
        
        if ax is None:
            plt.show()

    def test_input(self, input_string):
        if not self.dfa:
            raise Exception("DFA not generated yet")
        
        current_state = self.state_map[0]  # Start state
        
        for char in input_string:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char]
        
        return current_state.is_final
from FAdo.fa import *  # Import FAdo automata library
from NFA_DFA import nfa_to_dfa  # Import the function for NFA to DFA conversion
from RGX_NFA import regex_to_nfa  # Import the function for regex to NFA conversion
#test
def minimize_dfa(dfa):
    """
    Minimize a given DFA.

    Args:
        dfa (DFA): The DFA to be minimized.

    Returns:
        DFA: The minimized DFA.
    """
    try:
        # Minimize the DFA
        minimized_dfa = dfa.minimal()
        return minimized_dfa
    except Exception as e:
        print(f"Error during DFA minimization: {e}")
        return None

if __name__ == "__main__":
    # Example regex
    regex = "(a|b)*a"
    
    # Generate NFA from regex
    nfa = regex_to_nfa(regex)
    
    if nfa:
        # Convert NFA to DFA
        dfa = nfa_to_dfa(nfa)
        
        if dfa:
            # Minimize the DFA
            minimized_dfa = minimize_dfa(dfa)
            
            if minimized_dfa:
                minimized_dfa.display()

                # Display Minimized DFA details
                print("Minimized DFA States:", minimized_dfa.States)
                print("Minimized DFA Initial State:", minimized_dfa.Initial)
                print("Minimized DFA Final States:", minimized_dfa.Final)
                print("Minimized DFA Transitions:")
                for state in minimized_dfa.delta:
                    for symbol, next_state in minimized_dfa.delta[state].items():
                        print(f"{state} --{symbol}--> {next_state}")

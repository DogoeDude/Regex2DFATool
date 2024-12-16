from FAdo.reex import str2regexp
from FAdo.fa import *
#test
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

if __name__ == "__main__":
    # Example regex
    regex = "a(bc)*"
    
    # Generate NFA from regex
    nfa = regex_to_nfa(regex)
    
    if nfa:
        print("NFA Generated from Regex:")
        nfa.display()  # Display NFA details

        # Additional NFA details
        print("\nNFA States:", nfa.States)  # Change states to States
        print("NFA Initial State:", nfa.Initial)
        print("NFA Final States:", nfa.Final)
        print("NFA Transitions:")
        for state in nfa.delta:
            for symbol, next_states in nfa.delta[state].items():
                for next_state in next_states:
                    print(f"{state} --{symbol}--> {next_state}")
    else:
        print("Failed to generate NFA from the given regex.")

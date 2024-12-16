from regex_parser import RegexParser
from regex_to_nfa import RegexToNFA
from scanner_generator import ScannerGenerator

def main():
    # Get regex from user
    regex = input("Enter your regular expression: ")
    
    # Parse regex
    parser = RegexParser()
    try:
        parsed_regex = parser.parse(regex)
    except SyntaxError as e:
        print(f"Error parsing regex: {e}")
        return

    # Convert to NFA
    converter = RegexToNFA()
    nfa = converter.convert(parsed_regex)

    # Convert to DFA and create scanner
    scanner = ScannerGenerator()
    scanner.nfa_to_dfa(nfa)

    # Visualize the DFA
    scanner.visualize_dfa()

    # Test inputs
    while True:
        test_input = input("Enter a string to test (or 'quit' to exit): ")
        if test_input.lower() == 'quit':
            break
        
        is_accepted = scanner.test_input(test_input)
        print(f"Input '{test_input}' is {'accepted' if is_accepted else 'rejected'} by the DFA")

if __name__ == "__main__":
    main() 
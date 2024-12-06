# Regex2DFATool

The regex_parser.py is a recursive file to which it is a descent parser that breaks down a regex
into a syntax tree.

The parser follows this grammar rules :
    expression → term ('|' term)*      # Handles union operations (a|b)
    term → factor*                     # Handles concatenation (ab)
    factor → symbol ['*' | '+']        # Handles basic symbols and operators
    symbol → character | '(' expression ')'  # Handles basic chars and groups

    Example: For input "a|b":
        Creates:
        {
            'type': 'union',
            'terms': [
                {'type': 'symbol', 'value': 'a'},
                {'type': 'symbol', 'value': 'b'}
            ]
        }
    Example: For input "ab":
        Creates:
        {
        'type': 'concat',
        'factors': [
            {'type': 'symbol', 'value': 'a'},
            {'type': 'symbol', 'value': 'b'}
        ]
    }
The parser works by:
    1. Reading characters one by one
    2. Building a tree structure based on regex operators
    3. Handling precedence through recursive calls
    4. Creating appropriate node types for each operation
    5. This syntax tree is then used by regex_to_nfa.py to construct the NFA using Thompson's Construction Algorithm.
    6. The supported operations are:
        Concatenation (ab)
        Union (a|b)
        Kleene star (a)
        Plus (a+)
        Grouping with parentheses ((a|b))

The regex_to_nfa.py works by converting a Regular Expression to our desired DFA. Here exists the utilization of the Thompsons construction algorithm.
    1. The creation of invidual states with their defined transitions, etc.
    2. NFA construction class
    3. RegexToNFA:
        a. From the class itself, it  should have a self loop in case for preceeding repetitions.
        b. From the generated parsed regex from Regex_parser.py, we then determine the type of symbol.
        c. After identifying the symbols, we then create their specified NFA conversion.
        d. Each symbol has their own function in the creation of their states and transitions using Thompsons construction algorithm.

The scanner_generator.py works by utilizing Subset Construction algorithm.
    1. First are the class definitions for each DFA state and then the ScannerGenerator
    2. For the nfa_to_dfa function, we are utilizing now the Subset Construction Algorithm to which an array of dfa_states can be appended once each state has been determined.
        How subset construction works(in my understanding):
            a. Creation of intial DFA states from e-closure
            b. Processing of all states
                i.For each determined input symbol, we get all possible transitions from it.
                ii. Take E-closures and check if state already exists.
                iii. If the state is unique, then  we append it to the dfa_states array.
                iv. Add the transition and assign state ID's.
    3. E-closure computation: the set of all states reachable for their next transition through epsilon transitions.
    4. Visualize the DFA using Graphviz library in python.
    5. String testing.
    6. For the transition animation:
        a. Check if there are valid transitions from the current state being checked.
        b. If not, we then add a rejection step and stops.

Animation Processing:
    1. Collect all steps before starting the animation. Each step is its own current state, next state or none.
    2. Animation control, we process the steps one step at a time, to which we highlight the current state and transition..
    3. Visual updates, current state would be highlighted as yellow and transition anim is red.
    4. Time control: add delays to prevent overlaps. Add a speed slider.

    Animation step:
        steps = [
            (0, None),              # Initial state
            (0, ('a', 1)),         # Processing 'a'
            (1, ('b', 2)),         # Processing 'b'
            (2, None)              # Final state
        ]

Lastly, the gui.py
    Import the needed functions from the other files for the merging of Thompsons and Subset Construction(Our main Algorithsm for conversion) and the other algorithms such as:
    

    1. First and foremost, we initialize and class for the whole codebase to which it will have our scanner in.
    2. Layout the structure of the GUI using tkinter.
    3. Create input sections for the test and regex input.
    4. Add the animation controls of the file.
    5. DFA Generation and Visualization, Parse the Regex then the Parsed Regex will be processed to be converted to NFA through Thompsons construction Algorithm, once the generated NFA has been finished we use the NFA to be then passed through the next function to which it utilizes Subset Construction to which the NFA will be now converted to DFA.
    To visualize it, we use the the scanner to which will have their own states considered in the code as DOTS.
    6.String test and Animating, use the visualization functions from each file.
    7. Animation: Show Final result and update each run through of the visualization with Highlights to which every after highlight, the next step is already scheduled.
    8. Generated accepted strings are now then tested, if the entered string alphabet is positive then we go through its transitions and highlight their transition. We will also be sorting the transitions to prevent confusion.

Libraries: 
    1. Tkinter for GUI(TTK for modern widgets)
    2. Image and ImageTK for PIL(DFA visualization and Displays iamges in the GUI)
    3. Graphviz from Digraph(Handles DFA Visualization and drawing of states and transitions)
    4. Standard Library Utilities:
        i. Deque: for BFS string generation and NFA to DFA conversion.
        ii. Product: Generation of combinations or input sequences.
        iii. IO: For data conversion and image data processing streams.
        iv. Typing: Code readability
    5. Custom Module Imports:
        i. regex_parser:
            Parsing Regular Expressions.
            Creation of Syntax Trees.
        ii. regex_converter:
            Converts the parsed regex to NFA using Thompsons construction
            Manages the states and transitions.
        iii. scanner_generator:
            Converts NFA to DFA using subset construction and handles the visualization and test Input strings.

resources: 
    Subset Construction Algorithm:https://medium.com/@mmksajeeb/the-subset-construction-algorithm-nfa-%CE%B5-nfa-to-dfa-adf46dba31e3
    Thompsons Construction Algorithm: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b

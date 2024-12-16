# Regex2DFATool

This is for my Final Project in Automata Theory and Formal Languages

"Develop a tool that generates lexical analyzers (scanners) based on regular expressions. 
This project can involve translating regular expressions into finite automata and then generating 
code for a scanner based on the resulting automaton."

![Screenshot 2024-12-06 093957](https://github.com/user-attachments/assets/1ca2e28b-793d-41db-b9e3-e9afcd1eba18)

Steps in achieving the goal:
  1. Create a GUI using Tkinter for User interaction.
  2. The inputted REGEX will be parsed into singular variables to which will be specified.
  3. Using Thompsons Construction Algorithm, the parsed REGEX will be then converted to NFA.
  4. The converted NFA will be then converted again to DFA using Subset Construction Theorem.
  5. We then graph the generated DFA.
  6. The Graph is considered as our Scanner based off the regular expression.
  7. We then use Itertools library for the enumeration of the accepted strings to be tested for acceptance for the DFA.

The application supports REGEX's (), +, * and |. The graph gives out an animation for the inputted string.

Here is another example for the application:

![image](https://github.com/user-attachments/assets/371ada51-28d1-4b52-b2c5-320fac15194a)

For more Documentation, please do review the Document.txt.

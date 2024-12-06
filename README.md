# Regex2DFATool

This is for my Final Project in Automata Theory and Formal Languages.
This application is created using Python

The concept here is :
  "Develop a tool that generates lexical analyzers (scanners) based on regular expressions. 
  This project can involve translating regular expressions into finite automata and then generating 
  code for a scanner based on the resulting automaton."

  What I have come up with is: 
  
  ![Framework](https://github.com/user-attachments/assets/08cfd240-09de-4ff3-b3b2-d01fd096d03d)

  
Summarize steps in the development of this application:
  1. Create a GUI for the usability.
  2. Any inputed Regex will be parsed to which each character is individually identified.
  3. Once the Regex is parsed, then it goes through the Thompson's Subset Construction Algorithm to which it will generate an NFA.
  4. The generated NFA will be then converted using Subset Construction Algorithm.
  5. Enumerated strings are created as well using a built in Python Library named product from Itertools.

Here is the GUI: 
  ![image](https://github.com/user-attachments/assets/92b827f8-11c4-4b5d-ae17-74fd5b096729)
  
The supported symbols would be (), +, |, and *.

For more documentation, please do review the readme file.

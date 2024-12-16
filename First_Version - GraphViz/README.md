# Lexical-_Analyzer_Gen_Tool
This is for my Final Project in Automata Theory and Formal Languages
Context(Goal): Develop a tool that generates lexical analyzers (scanners) based on regular expressions. This project can involve translating regular expressions into finite automata and then generating code for a scanner based on the resulting automaton.
  -Create an app that has the ability to convert regular expressions down to minimized DFA
  -The minimized DFA can be considered as the scanner
  -Generate random codes that are acceptable for the scanner
  -Enumerate the codes acceptable for the scanner

I have Utilized the FAdo library that was built for Regular Expressions: https://pypi.org/project/FAdo/ or https://fado.dcc.fc.up.pt/
For graphing, I have used the GraphViz library that is directly built in VScode and has its very own software: https://graphviz.org/
For the GUI, I have utilized the Tkinter library for simplicity and efficiency.

![Screenshot 2024-11-27 004606](https://github.com/user-attachments/assets/0cda0958-89ea-4191-afaa-e5b9bd498413)
![Screenshot 2024-11-27 002302](https://github.com/user-attachments/assets/67e81454-7016-4a9b-879f-cddc5afb8254)

We can consider the Graph or the Minimized DFA as the Scanner
whereas for our generated codes or enumerated strings, those are the acceptable codes
for the scanner to base off.

Redefined the UI and Fixed some bugs:


![Screenshot 2024-11-27 161729](https://github.com/user-attachments/assets/df17a782-0cde-4589-8d51-c65c220263b3)
![Screenshot 2024-11-27 161720](https://github.com/user-attachments/assets/3a2f8b9a-ba2a-43d8-8476-1e416b01541d)
![Screenshot 2024-11-27 161705](https://github.com/user-attachments/assets/4d21395c-e36a-4df2-a35a-3d071030c5e4)
![Screenshot 2024-11-27 161651](https://github.com/user-attachments/assets/b9a487b4-c9fe-4671-9b89-e1daf514c129)
![Screenshot 2024-11-27 161552](https://github.com/user-attachments/assets/385d5908-2eb0-4bb2-a8f8-2a72bc6ba65f)

<<<<<<< HEAD
Currently fixing the random string generator
Update: None
=======
Have Fixed the Random Generation bug:

![image](https://github.com/user-attachments/assets/2eec69c6-196a-4169-876e-95d517fd0463)

But to get random code generated, the string maximum length should be less than or equal to 6 only.
>>>>>>> ac068d363a24c6e25e4985381f854eac073fbe3f

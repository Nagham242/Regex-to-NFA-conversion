# Regex to NFA Visualizer

This project is a **Regex to NFA Visualizer**, which converts regular expressions (regex) into non-deterministic finite automata (NFA) and visualizes the NFA states, transitions, and various components. The project is built using Python, and it provides a graphical user interface (GUI) for users to input regular expressions and view the conversion to NFA.

## Features

1. **Starting Window with Description and Welcome Message**
   - Displays a user-friendly starting window with a welcoming message.
   - Provides a brief description of supported regex operators.
   - 
2. **Regex Input Description**
   - Accepts a user-provided regex pattern and provides a detailed breakdown.
   - Shows the states, start state, and accept states of the converted NFA.
   - 
3. **Full NFA Visualization**
   - Visually represents the entire NFA (Non-deterministic Finite Automaton) for the provided regex.
   - Displays states, transitions, start state, and accept states clearly on the GUI.
   - 
4. **Support for Various Regex Operators**
   - **Union (`|`)**: Denotes the union (OR) of two regex patterns.
   - **Concatenation (`.`)**: Represents implicit concatenation between patterns.
   - **Kleene Star (`*`)**: Matches zero or more repetitions of the preceding expression.
   - **Kleene Plus (`+`)**: Matches one or more repetitions of the preceding expression.
   - **Grouping (`()`)**: Used to group expressions and control precedence.
   - **Optional (`?`)**: Matches zero or one occurrence of the preceding expression.
   - **Character Class (`[]`)**: Denotes a set of characters that can match.
   - 
5. **Option to Save the NFA as a PNG**
   - Allows the user to save the generated NFA visualization as a PNG image for further use or sharing.
   - 
6. **Clear Display of Start and Accept States**
   - Clearly highlights the **start state** and **accept states** in the NFA diagram for easier understanding of the regex's behavior.
   - 
7. **User-Friendly GUI**
   - Easy-to-use graphical user interface with intuitive controls.
   - 
8. **Error Handling and Feedback**
    - Provides clear error messages if the input regex is invalid, helping users understand and correct their inputs.

## Project Structure
### Key Files:
- **`startwindow.py`**: This file handles the starting window that displays a welcoming message, logo, and description of supported operators. It serves as the initial screen when the user runs the program.
  
- **`nfa_gui.py`**: This file contains the logic for converting the input regex into an NFA and visualizing the NFA states and transitions graphically.

- **`regex_to_nfa.py`**: This is the core logic for converting a regular expression into a non-deterministic finite automaton (NFA). It parses the regex and constructs the corresponding NFA.

- **`regex.png`**: The logo image that is displayed in the start window.

### Dependencies

The following Python packages are required to run the project:

- `tkinter` - for building the GUI.
- `PIL` (Python Imaging Library) - for image handling and display.
- `subprocess` - to invoke external processes when needed.
- `os` - for handling filesystem paths.

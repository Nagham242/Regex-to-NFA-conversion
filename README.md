# Regex to NFA Converter
This is a Python-based tool that converts regular expressions (regex) into Non-deterministic Finite Automata (NFA). The tool processes the regex, constructs an NFA, and displays its transitions in a human-readable format. It supports common regex operators such as union (`|`), concatenation (`.`), Kleene star (`*`), Kleene plus (`+`), and optional (`?`) operators.

## Features:
- Convert regex patterns into NFAs.
- Handle standard regex operators:
  - `|` : Union (OR)
  - `.` : Concatenation (implicit, but added automatically)
  - `*` : Kleene Star (0 or more repetitions)
  - `+` : Kleene Plus (1 or more repetitions)
  - `?` : Optional (0 or 1 repetition)
  - `[]` : Character classes (e.g., `[a-z],[0-9]`)
  - `()` : Grouping
- Allows continuous input of regex patterns to convert to NFA without restarting the program.

## Requirements

- Python 3.x
- The `re` module (standard library in Python, no installation required)
## Example
Enter a regular expression: (a|b)*

✅ The NFA Transitions for this regex: (a|b)*
_________________________________________________
S0 --ε--> S1
S1 --ε--> S2
S2 --a--> S3
S3 --ε--> S4
S4 --ε--> S1
S4 --ε--> S5
S1 --ε--> S6
S6 --b--> S7
S7 --ε--> S4
S0 --ε--> S5
S0 --ε--> S1
S1 --ε--> S2
S2 --a--> S3
S3 --ε--> S4
S4 --ε--> S1
S4 --ε--> S5
S1 --ε--> S6
S6 --b--> S7
S7 --ε--> S4
S0 --ε--> S5
## Setup

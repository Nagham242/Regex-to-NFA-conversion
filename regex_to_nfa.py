import re
class State:
    def __init__(self):
        self.transitions = {}  # dict: symbol -> list of State
        self.epsilon = []      # list of epsilon-transition states

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept
#adds concatenation operator '.' to the regex
def regex_to_nfa(regex):
    def expand_character_classes(regex):
        def expand_class(match):
            content = match.group(1)
            expanded = []
            i = 0
            while i < len(content):
                if i + 2 < len(content) and content[i+1] == '-':
                    start = content[i]
                    end = content[i+2]
                    expanded.extend(chr(c) for c in range(ord(start), ord(end)+1))
                    i += 3
                else:
                    expanded.append(content[i])
                    i += 1
            return '(' + '|'.join(expanded) + ')'
        # Find [ ... ] and replace with (x|y|z)
        return re.sub(r'\[([^\]]+)\]', expand_class, regex)
    def add_concat(regex):
        result = ""
        for i in range(len(regex) - 1):
            c1 = regex[i]
            c2 = regex[i + 1]
            result += c1
            if (c1.isalnum() or c1 in ")*+?") and (c2.isalnum() or c2 == '('):
                result += '.'
        result += regex[-1]
        return result
# adds precedence to the operators *,+ are the highest precedence > . > |
    def precedence(op):
        return {'*': 3,'+':3,'?': 3, '.': 2, '|': 1}.get(op, 0)
    
    def to_postfix(regex):
        output = ""
        stack = []
        i = 0
        while i < len(regex):
            char = regex[i]
            if char.isalnum():  # For literals
                output += char
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output += stack.pop()
                stack.pop()  # remove '(' from stack
            else:  # operators (*, +, ., |, ?)
                while stack and precedence(char) <= precedence(stack[-1]):
                    output += stack.pop()
                stack.append(char)
            i += 1
        while stack:
            output += stack.pop()
        return output

    def build_nfa(postfix):
        stack = []
        i = 0
        while i < len(postfix):
            char = postfix[i]
            if char.isalnum():  # For literals (a-z, A-Z, 0-9)
                start = State()
                accept = State()
                start.transitions[char] = [accept]
                stack.append(NFA(start, accept))
            elif char == '.':  # Concatenation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa1.accept.epsilon.append(nfa2.start)
                stack.append(NFA(nfa1.start, nfa2.accept))
            elif char == '|':  # Alternation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = State()
                accept = State()
                start.epsilon.extend([nfa1.start, nfa2.start])
                nfa1.accept.epsilon.append(accept)
                nfa2.accept.epsilon.append(accept)
                stack.append(NFA(start, accept))
            elif char == '*':  # Kleene Star
                nfa = stack.pop()
                start = State()
                accept = State()
                start.epsilon.extend([nfa.start, accept])
                nfa.accept.epsilon.extend([nfa.start, accept])
                stack.append(NFA(start, accept))
            
            elif char == '+':
                nfa = stack.pop()
                start = State()
                accept = State()
                start.epsilon.append(nfa.start)                 # must go through the NFA at least once
                nfa.accept.epsilon.extend([nfa.start, accept])  # repeat or move to accept
                stack.append(NFA(start, accept))
            elif char == '?':  # Optional: zero or one occurrence
                nfa = stack.pop()
                start = State()
                accept = State()
                start.epsilon.extend([nfa.start, accept])
                nfa.accept.epsilon.append(accept)
                stack.append(NFA(start, accept))
            i += 1
        if len(stack) != 1:
            raise ValueError("Invalid regex: stack should have exactly one NFA at the end")
        return stack.pop()

    # Main function logic
    regex = expand_character_classes(regex)
    regex = add_concat(regex)
    postfix = to_postfix(regex)
    return build_nfa(postfix)

def print_nfa(nfa, visited=None, state_ids=None, counter=None):
    if visited is None:
        visited = set()
    if state_ids is None:
        state_ids = {}
    if counter is None:
        counter = [0]
    def get_id(state):
        if state not in state_ids:
            state_ids[state] = f"S{counter[0]}"
            counter[0] += 1
        return state_ids[state]

    start = nfa.start
    sid = get_id(start)
    if start in visited:
        return
    visited.add(start)

    for symbol, targets in start.transitions.items():
        for target in targets:
            tid = get_id(target)
            print(f"{sid} --{symbol}--> {tid}")
            print_nfa(NFA(target, nfa.accept), visited, state_ids, counter)

    for target in start.epsilon:
        tid = get_id(target)
        print(f"{sid} --ε--> {tid}")
        print_nfa(NFA(target, nfa.accept), visited, state_ids, counter)
# ========== TEST CASE ==========

def main():
    print("\nWelcome to the Regex to NFA Converter!")
    print("Supported operators:")
    print("  |  : Union (OR)")
    print("  .  : Concatenation (Added automatically)")
    print("  *  : Kleene Star (0 or more repetitions)")
    print("  +  : Kleene Plus (1 or more repetitions)")
    print("  ?  : Optional (0 or 1 repetition)")
    print("  [] : Character class (e.g., [a-z])")
    print("  () : Grouping")
    print("Example: (a|b)*ab+\n")
    while True:
        counter = [0]
        regex = input("Enter a regular expression: ")
        try:
            nfa = regex_to_nfa(regex)
            print("\n✅ The NFA Transitions for this regex:", regex)
            print("_________________________________________________")
            print_nfa(nfa)
            print_nfa(nfa, counter=counter)
        except Exception as e:
            print("\n❌ Error:", e)
        continue_input = input("Do you want to enter another regex? (y/n): ").lower()
        if continue_input != 'y':
            print("Exiting the program.")
            break
if __name__ == "__main__":
    main()
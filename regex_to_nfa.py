import re

class State:
    def __init__(self):
        self.transitions = {}  # dict: symbol -> list of State
        self.epsilon = []      # list of epsilon-transition states

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

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

    def precedence(op):
        return {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}.get(op, 0)

    def to_postfix(regex):
        output = ""
        stack = []
        i = 0
        while i < len(regex):
            char = regex[i]
            if char.isalnum():
                output += char
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output += stack.pop()
                stack.pop()
            else:
                while stack and precedence(char) <= precedence(stack[-1]):
                    output += stack.pop()
                stack.append(char)
            i += 1
        while stack:
            output += stack.pop()
        return output

    def build_nfa(postfix):
        stack = []
        for char in postfix:
            if char.isalnum():
                start = State()
                accept = State()
                start.transitions[char] = [accept]
                stack.append(NFA(start, accept))
            elif char == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                nfa1.accept.epsilon.append(nfa2.start)
                stack.append(NFA(nfa1.start, nfa2.accept))
            elif char == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                start = State()
                accept = State()
                start.epsilon.extend([nfa1.start, nfa2.start])
                nfa1.accept.epsilon.append(accept)
                nfa2.accept.epsilon.append(accept)
                stack.append(NFA(start, accept))
            elif char == '*':
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
                start.epsilon.append(nfa.start)
                nfa.accept.epsilon.extend([nfa.start, accept])
                stack.append(NFA(start, accept))
            elif char == '?':
                nfa = stack.pop()
                start = State()
                accept = State()
                start.epsilon.extend([nfa.start, accept])
                nfa.accept.epsilon.append(accept)
                stack.append(NFA(start, accept))
        if len(stack) != 1:
            raise ValueError("Invalid regex")
        return stack[0]

    regex = expand_character_classes(regex)
    regex = add_concat(regex)
    postfix = to_postfix(regex)
    return build_nfa(postfix)
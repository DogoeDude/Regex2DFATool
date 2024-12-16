from typing import List
from regex_to_nfa import NFA

class RegexParser:
    def __init__(self):
        self.pos = 0
        self.regex = ""

    def parse(self, regex_str):
        self.regex = regex_str
        self.pos = 0
        return self.parse_expression()

    def parse_expression(self):
        terms = [self.parse_term()]
        
        while self.pos < len(self.regex) and self.regex[self.pos] == '|':
            self.pos += 1
            terms.append(self.parse_term())
        
        return {'type': 'union', 'terms': terms} if len(terms) > 1 else terms[0]

    def parse_term(self):
        factors = []
        while self.pos < len(self.regex) and self.regex[self.pos] not in ')|':
            factors.append(self.parse_factor())
        
        return {'type': 'concat', 'factors': factors} if len(factors) > 1 else factors[0]

    def parse_factor(self):
        if self.pos >= len(self.regex):
            raise SyntaxError("Unexpected end of regex")

        char = self.regex[self.pos]
        
        if char == '(':
            self.pos += 1
            subexpr = self.parse_expression()
            if self.pos >= len(self.regex) or self.regex[self.pos] != ')':
                raise SyntaxError("Missing closing parenthesis")
            self.pos += 1
            result = subexpr
        else:
            self.pos += 1
            result = {'type': 'symbol', 'value': char}

        # Handle closure operators (* and +)
        if self.pos < len(self.regex):
            if self.regex[self.pos] == '*':
                self.pos += 1
                result = {'type': 'kleene_star', 'expr': result}
            elif self.regex[self.pos] == '+':
                self.pos += 1
                result = {'type': 'plus', 'expr': result}

        return result
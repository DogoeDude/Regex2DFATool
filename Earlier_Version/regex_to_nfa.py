class State:
    def __init__(self, is_final=False):
        self.transitions = {}  # dict of symbol -> list of states
        self.epsilon_transitions = set()
        self.is_final = is_final
        self.state_id = None  # Will be set when building the NFA

class NFA:
    def __init__(self):
        self.states = []
        self.start_state = None
        self.final_states = set()
        self.alphabet = set()

    def add_state(self, state):
        state.state_id = len(self.states)
        self.states.append(state)
        return state

class RegexToNFA:
    def __init__(self):
        self.counter = 0

    def convert(self, parsed_regex):
        if parsed_regex['type'] == 'symbol':
            return self.create_basic_nfa(parsed_regex['value'])
        elif parsed_regex['type'] == 'union':
            return self.create_union_nfa(parsed_regex['terms'])
        elif parsed_regex['type'] == 'concat':
            return self.create_concat_nfa(parsed_regex['factors'])
        elif parsed_regex['type'] == 'kleene_star':
            return self.create_kleene_star_nfa(parsed_regex['expr'])
        elif parsed_regex['type'] == 'plus':
            return self.create_plus_nfa(parsed_regex['expr'])

    def create_basic_nfa(self, symbol):
        nfa = NFA()
        start = State()
        end = State(is_final=True)
        
        start.transitions[symbol] = [end]
        nfa.alphabet.add(symbol)
        
        nfa.add_state(start)
        nfa.add_state(end)
        nfa.start_state = start
        nfa.final_states.add(end)
        
        return nfa

    def create_union_nfa(self, terms):
        nfa = NFA()
        start = State()
        end = State(is_final=True)
        
        nfa.add_state(start)
        nfa.add_state(end)
        
        for term in terms:
            sub_nfa = self.convert(term)
            start.epsilon_transitions.add(sub_nfa.start_state)
            for final in sub_nfa.final_states:
                final.epsilon_transitions.add(end)
                final.is_final = False
            
            nfa.states.extend(sub_nfa.states)
            nfa.alphabet.update(sub_nfa.alphabet)
        
        nfa.start_state = start
        nfa.final_states = {end}
        return nfa

    def create_concat_nfa(self, factors):
        if not factors:
            return None
        
        result = self.convert(factors[0])
        
        for factor in factors[1:]:
            second = self.convert(factor)
            for final in result.final_states:
                final.epsilon_transitions.add(second.start_state)
                final.is_final = False
            
            result.states.extend(second.states)
            result.final_states = second.final_states
            result.alphabet.update(second.alphabet)
        
        return result

    def create_kleene_star_nfa(self, expr):
        nfa = NFA()
        start = State()
        end = State(is_final=True)
        
        sub_nfa = self.convert(expr)
        
        nfa.add_state(start)
        nfa.add_state(end)
        
        start.epsilon_transitions.add(end)
        start.epsilon_transitions.add(sub_nfa.start_state)
        
        for final in sub_nfa.final_states:
            final.epsilon_transitions.add(end)
            final.epsilon_transitions.add(sub_nfa.start_state)
            final.is_final = False
        
        nfa.states.extend(sub_nfa.states)
        nfa.start_state = start
        nfa.final_states = {end}
        nfa.alphabet = sub_nfa.alphabet
        
        return nfa

    def create_plus_nfa(self, expr):
        nfa = NFA()
        start = State()
        end = State(is_final=True)
        
        sub_nfa = self.convert(expr)
        
        nfa.add_state(start)
        nfa.add_state(end)
        
        start.epsilon_transitions.add(sub_nfa.start_state)
        
        for final in sub_nfa.final_states:
            final.epsilon_transitions.add(end)
            final.epsilon_transitions.add(sub_nfa.start_state)
            final.is_final = False
        
        nfa.states.extend(sub_nfa.states)
        nfa.start_state = start
        nfa.final_states = {end}
        nfa.alphabet = sub_nfa.alphabet
        
        return nfa 
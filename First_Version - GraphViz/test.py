import random

def regex_based_string_generator(regex, num_strings=10):
    """
    Generate random strings that match a given regex.

    Parameters:
        regex (str): A simplified regex (e.g., "(a|b)*cd*").
        num_strings (int): Number of matching strings to generate.

    Returns:
        list: A list of strings matching the regex.
    """
    def generate_segment(segment):
        """
        Generate a string segment based on a simplified regex component.
        """
        if segment.startswith('(') and '|' in segment:  # Alternation group, e.g., (a|b)
            options = segment.strip('()').split('|')
            return random.choice(options)
        elif segment.endswith('*'):  # Repetition, e.g., a*
            char = segment[0]
            return char * random.randint(0, 10)  # Repeat 0-10 times
        elif segment.endswith('+'):  # At least one repetition, e.g., a+
            char = segment[0]
            return char * random.randint(1, 10)  # Repeat 1-10 times
        else:
            return segment  # Literal characters like "cd"

    # Split the regex into segments
    # Assumes a regex with simple constructs: (a|b)*, cd*, etc.
    # For complex regex, more parsing would be required.
    segments = []
    i = 0
    while i < len(regex):
        if regex[i] == '(':
            j = regex.find(')', i)  # Find the end of the group
            segments.append(regex[i:j + 1])
            i = j + 1
        elif regex[i].isalpha():
            if i + 1 < len(regex) and regex[i + 1] in '*+':
                segments.append(regex[i:i + 2])
                i += 2
            else:
                segments.append(regex[i])
                i += 1
        else:
            i += 1

    # Generate random strings by combining generated segments
    result = []
    for _ in range(num_strings):
        random_string = ''.join(generate_segment(segment) for segment in segments)
        result.append(random_string)

    return result

# Example usage
regex = "(a|b)*cd*"
random_strings = regex_based_string_generator(regex, num_strings=10)
print("Random strings matching the regex:")
print(random_strings)

'''
=== Plugboard class for Enigma Machine ===
                [VERIFIED]
'''

import helpers

class Plugboard:
    def __init__(self, pairs: list[str] = [], alphabet: str = helpers.ALPHABET):
        self.alphabet = [helpers.letter_to_index(letter) for letter in alphabet]

        swapped: list[str] = [] # list of swapped letters
        for pair in pairs:     # for each pair
            if len(pair) != 2: # check valid length
                raise ValueError(f"Error in Plugboard Initialization: Expected string of length 2, found length {len(pair)} ({pair!r})")
            elif pair[0] == pair[1]: # check distincness
                raise ValueError(f"Error in Plugboard Initialization: Can not swap identical values ({pair!r})")
            elif pair[0] in swapped or pair[1] in swapped:
                raise ValueError(f"Error in Plugboard Initialization: Can not swap positions more than once ({pair!r})")

            else:
                a = helpers.letter_to_index(pair[0])
                b = helpers.letter_to_index(pair[1])

                # swap letters
                self.alphabet = self.alphabet[:a] + [b] + self.alphabet[a+1:]
                self.alphabet = self.alphabet[:b] + [a] + self.alphabet[b+1:]

                # appened to swapped
                swapped.append(pair[0])
                swapped.append(pair[1])

    def forward(self, signal: int) -> int:
        return self.alphabet[signal]

    def backward(self, signal: int) -> int:
        return self.alphabet.index(signal)
    
if __name__ == "__main__":
    pass
'''
=== Plugboard class for Enigma Machine ===
                [VERIFIED]
'''

import helpers as hp

class Plugboard:
    def __init__(self, pairs: list[str] = [], alphabet: str = hp.ALPHABET):
        '''
        self.wiring = a map of which letters (A-Z) map to which
        eg. self.wiring[0] ('A') = 0 ('A'), self.wiring[5] = 5 ('F')
        '''
        self.wiring = [hp.letter_to_index(letter) for letter in alphabet]

        # === swap pairs ===

        # validate no duplicate letters
        assert len(pairs) == len(set(pairs))

        for pair in pairs:     # for each pair
            if len(pair) != 2: # check valid length
                raise ValueError(f"Error in Plugboard Initialization: Expected string of length 2, found length {len(pair)} ({pair!r})")
            elif pair[0] == pair[1]: # check distincness
                raise ValueError(f"Error in Plugboard Initialization: Can not swap identical values ({pair!r})")
            
            else:
                a = hp.letter_to_index(pair[0])
                b = hp.letter_to_index(pair[1])

                # swap letters
                self.wiring = self.wiring[:a] + [b] + self.wiring[a+1:]
                self.wiring = self.wiring[:b] + [a] + self.wiring[b+1:]

    def forward(self, signal: int) -> int:
        return self.wiring[signal]

    def backward(self, signal: int) -> int:
        return self.wiring.index(signal)


# test usage
if __name__ == "__main__":
    # Test Plugboard
    pb = Plugboard(["AB", "CD", "EF"])
    assert pb.forward(0) == 1
    assert pb.forward(1) == 0
    assert pb.forward(2) == 3
    assert pb.forward(3) == 2
    assert pb.forward(4) == 5
    assert pb.forward(5) == 4
    print("Plugboard test passed.")
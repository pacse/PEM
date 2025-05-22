'''
=== Plugboard class for Enigma Machine ===
                [VERIFIED]
'''

import helpers as hp

class Plugboard:
    def __init__(self, pairs: list[str] = []):
        '''
        self.wiring = a map of which letters (A-Z) map to which
        eg. self.wiring[0] ('A') = 0 ('A'), self.wiring[5] = 5 ('F')
        '''
        self.wiring = [hp.letter_to_index(letter) for letter in hp.ALPHABET]
        # Left: indexes
        # Right: values

        # === swap pairs ===

        # validate no duplicate letters
        assert len(pairs) == len(set(pairs))

        for pair in pairs:     # for each pair
            if len(pair) != 2: # check valid length
                raise ValueError(f"Error in Plugboard Initialization: Expected string of length 2, found length {len(pair)} ({pair!r})")
            elif pair[0] == pair[1]: # check distincness
                raise ValueError(f"Error in Plugboard Initialization: Can not swap identical values ({pair!r})")

            else:
                # get indexes
                a = hp.letter_to_index(pair[0])
                b = hp.letter_to_index(pair[1])

                # swap letters
                self.wiring[a] = b
                self.wiring[b] = a

    def forward(self, signal: int) -> int:
        return self.wiring[signal]

    def backward(self, signal: int) -> int:
        return self.wiring.index(signal)


# test usage
if __name__ == "__main__":

    # test swapped Plugboard
    swapped_pb = Plugboard(["AB", "CD", "EF"])
    assert swapped_pb.forward(0) == 1, f"Plugboard test failed at index 0 ({swapped_pb.forward(0)})"
    assert swapped_pb.forward(1) == 0, f"Plugboard test failed at index 1 ({swapped_pb.forward(1)})"
    assert swapped_pb.forward(2) == 3, f"Plugboard test failed at index 2 ({swapped_pb.forward(2)})"
    assert swapped_pb.forward(3) == 2, f"Plugboard test failed at index 3 ({swapped_pb.forward(3)})"
    assert swapped_pb.forward(4) == 5, f"Plugboard test failed at index 4 ({swapped_pb.forward(4)})"
    assert swapped_pb.forward(5) == 4, f"Plugboard test failed at index 5 ({swapped_pb.forward(5)})"
    for i in range(6, 26):
        assert swapped_pb.forward(i) == i, f"Plugboard test failed at index {i} ({swapped_pb.forward(i)})"
    # test unswapped Plugboard
    unswapped_pb = Plugboard()
    for i in range(26):
        assert unswapped_pb.forward(i) == i, f"Plugboard test failed at index {i} ({unswapped_pb.forward(i)})"
    print("Plugboard test passed.")
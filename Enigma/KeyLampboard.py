'''
=== Keyboard and Lampboard classes for Enigma Machine ===
                        [VERIFIED]
'''

import helpers as hp

class Keyboard:
    def __init__(self):
        '''
        initialize a keyboard
        self.wiring = a map of which letters (A-Z) map to which
        eg. self.wiring[0] ('A') = 0 ('A'), self.wiring[5] = 5 ('F')
        '''
        self.wiring = hp.ALPHABET

    def forward(self, letter: str) -> int:
        '''
        converts a letter to its signal
        '''
        return self.wiring.index(letter)

class Lampboard:
    def __init__(self):
        '''
        initialize a lampboard
        self.wiring = a map of which letters (A-Z) map to which
        eg. self.wiring[0] ('A') = 0 ('A'), self.wiring[5] = 5 ('F')
        '''
        self.wiring = hp.ALPHABET
        
    def forward(self, signal: int) -> str:
        '''
        converts a signal to its letter
        '''
        return self.wiring[signal]

# test usage
if __name__ == "__main__":
    # init Keyboard and Lampboard
    KB = Keyboard()
    LB = Lampboard()
    
    # Test Keyboard
    for i, char in enumerate(hp.ALPHABET):
        assert KB.forward(char) == i, f"Keyboard test failed at index {i} ({char})"
    print("Keyboard test passed.")
    
    # Test Lampboard
    for i, char in enumerate(hp.ALPHABET):
        assert LB.forward(i) == char, f"Lampboard test failed at index {i} ({char})"
    print("Lampboard test passed.")
    print(f"Keyboard wiring: {KB.wiring}")
    print(f"Lampboard wiring: {LB.wiring}")
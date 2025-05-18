'''
=== Keyboard class for Enigma Machine ===
               [VERIFIED]
'''
import helpers as hp

class Keyboard:
    def __init__(self, alphabet: str = hp.ALPHABET):
        '''
        self.wiring = a map of which letters (A-Z) map to which
        eg. self.wiring[0] ('A') = 'A'
        '''
        self.wiring = alphabet

    def keyboard(self, letter: str) -> int:
        return self.wiring.index(letter)

    def lampboard(self, signal: int) -> str:
        return self.wiring[signal]


# test usage
if __name__ == "__main__":
    KB = Keyboard()
    # Test Keyboard
    for i, char in enumerate(KB.wiring):
        assert KB.keyboard(char) == i, f"Keyboard test failed at index {i} ({char})"
    print("Keyboard test passed.")
    # Test Lampboard
    for i, char in enumerate(KB.wiring):
        assert KB.lampboard(i) == char, f"Lampboard test failed at index {i} ({char})"
    print("Lampboard test passed.")
    print(KB.wiring)
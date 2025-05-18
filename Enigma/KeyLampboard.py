'''
=== Keyboard class for Enigma Machine ===
               [VERIFIED]
'''
import helpers

class Keyboard:
    def __init__(self, alphabet: str=helpers.ALPHABET):
        self.alphabet = alphabet

    def keyboard(self, letter: str) -> int:
        return self.alphabet.index(letter)

    def lampboard(self, signal: int) -> str:
        return self.alphabet[signal]

'''
KB = Keyboard()
print(KB)
print(KB.keyboard("A"))
print(KB.lampboard(4))
'''
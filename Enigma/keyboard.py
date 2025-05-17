'''
=== Keyboard class for Enigma Machine ===
               [VERIFIED]
'''
import helpers

class Keyboard:
    def __init__(self, alphabet=helpers.ALPHABET):
        self.alphabet = alphabet

    def keyboard(self, letter):
        return self.alphabet.index(letter)

    def lampboard(self, signal):
        return self.alphabet[signal]

'''
KB = Keyboard()
print(KB)
print(KB.keyboard("A"))
print(KB.lampboard(4))
'''
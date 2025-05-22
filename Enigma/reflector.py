'''
=== Reflector class for Enigma Machine ===
                [VERIFIED]                
'''

import helpers as hp

class Reflector:
    def __init__(self, wiring: str) -> None:
        '''
        Initialize a reflector
        Parameters:
        wiring - The wiring for the reflector
        '''
        self.wiring = [hp.letter_to_index(letter) for letter in wiring]

    def reflect(self, signal: int) -> int:
        '''
        Passes the provided signal through the reflector.
        '''
        return self.wiring[signal]

# historical reflectors
A = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
C = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")

if __name__ == "__main__":
    pass
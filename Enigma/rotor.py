'''
=== Rotor class for Enigma Machine ===
              [VERIFIED]              
'''

import helpers as hp

class Rotor:
    def __init__(self, wiring: str, notches: list[str]) -> None:
        '''
        Initialize a rotor
        Parameters:
        wiring - The wiring for the rotor
        notch - The notch position for the rotor
        '''
        self.wiring = [hp.letter_to_index(letter) for letter in wiring] # rotor wiring
        self.position = 0 # rotor position (for rotation)
        self.notch = [hp.letter_to_index(notch) for notch in notches] # rotor notch(es)

    def forward(self, signal: int) -> int:
        '''
        Passes the provided signal forward through the rotor
        '''
        signal = (signal + self.position) % 26
        return (self.wiring[signal] - self.position) % 26

    def backward(self, signal: int) -> int:
        '''
        Passes the provided signal backward through the rotor
        '''
        signal = (signal + self.position) % 26
        return (self.wiring.index(signal) - self.position) % 26

    def rotate(self, n: int = 1) -> None:
        '''
        Steps the rotor n times
        '''
        self.position = (self.position + n) % 26

    def rotate_to_letter(self, letter: str) -> None:
        '''
        Sets the rotor position to the provided letter
        '''
        self.position = hp.letter_to_index(letter)

    def show(self) -> None:
        '''
        Prints the rotor wiring and position
        '''
        print(f"Position: {self.position} ({hp.index_to_letter(self.position)})")
        print("Wiring:", ''.join(hp.index_to_letter(index) for index in self.wiring))
        print()

# historical rotors
I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"])
II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"])
III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"])
IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"])
V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"])

# test usage
if __name__ == "__main__":

    I.show()
    print(hp.index_to_letter(I.forward(0)))
    I.rotate()
    I.show()
    print(hp.index_to_letter(I.forward(0)))
import helpers

class Reflector:
    def __init__(self, alphabet):
        self.alphabet = [helpers.letter_to_index(letter) for letter in alphabet]

    def reflect(self, signal):
        return self.alphabet[signal]

RF = Reflector("")
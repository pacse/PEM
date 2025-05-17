import helpers

class Reflector:
    def __init__(self, alphabet):
        self.alphabet = [helpers.letter_to_index(letter) for letter in alphabet]

    def forward(self, signal):
        return self.alphabet[signal]

    def backward(self, signal):
        pass

if __name__ == "__main__":
    pass
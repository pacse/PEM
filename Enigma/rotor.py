import helpers

class Reflector:
    def __init__(self, alphabet: str) -> None:
        self.alphabet = [helpers.letter_to_index(letter) for letter in alphabet]

    def forward(self, signal: int) -> int:
        return self.alphabet[signal]

    def backward(self, signal: int) -> int:
        return self.alphabet.index(signal)

if __name__ == "__main__":
    pass
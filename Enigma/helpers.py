ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LTR_0 = ord(ALPHABET[0])

def index_to_letter(index):
    return chr(index + LTR_0)

def letter_to_index(letter):
    return ord(letter) - LTR_0

if __name__ == "__main__":
    pass
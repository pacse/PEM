from string import ascii_uppercase

''' === Alphabetical stuff === '''
ALPHABET = ascii_uppercase # A-Z
A = ord(ALPHABET[0]) # A for easier reference

def index_to_letter(index: int) -> str:
    '''
    Converts alphabetical index to alphabetical letter
    '''
    return chr(index + A)

def letter_to_index(letter: str) -> int:
    '''
    Converts alphabetical letter to  alphabetical index
    '''
    return ord(letter) - A

''' === Asciibetical stuff === '''
ASCIIBET = ''.join(chr(i) for i in range(32, 127)) # Ascii printable characters
LTR_0 = ord(ASCIIBET[0]) # letter 0 for easier reference

def index_to_ascii(index: int) -> str:
    '''
    Converts ascii index to ascii character
    '''
    return chr(index + LTR_0)

def ascii_to_index(ascii: str) -> int:
    '''
    Converts ascii character to ascii index
    '''
    return ord(ascii) - LTR_0


# test stuff
if __name__ == "__main__":
    print(ALPHABET)
    print(A)
    print(ASCIIBET)
    print(LTR_0)
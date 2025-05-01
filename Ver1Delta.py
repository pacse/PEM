# PEM Version Delta – WIP
import secrets
from dataclasses import dataclass
from typing import Tuple, List, TypeAlias

ModResults: TypeAlias = List[List[int]]

@dataclass
class EncryptedMessage:
  message: str
  mod_results: ModResults

#message: str = "Hello. I like rice."
#ciphertext: str = ""
#decrypted_text: str = ""

ASCII_MIN = 32  # first unicode ascii character
ASCII_MAX = 126 # last unicode ascii character
ASCII_RANGE = ASCII_MAX - ASCII_MIN + 1 # total unicode ascii characters

def check_type(variable, check_type: list[str]) -> bool:
  '''
  Checks if a variable is equal to a type with a list of types
  eg. to check for list[list[int]] check_type = [list, list, int]
  '''
  # type 0 is correct, and isn't a list
  if isinstance(variable, check_type[0]) and check_type[0] != "list":
    return True

  # type 0 is correct, and is a list
  elif isinstance(variable, check_type[0]) and check_type[0] == "list":

    # type 1 is correct, and isn't a list
    if all(isinstance(var, check_type[1]) for var in variable) and check_type[1] != "list":
      return True

    # type 1 is correct, and is a list
    elif all(isinstance(var, check_type[1]) for var in variable) and check_type[1] == "list":
      if all(all(isinstance(v, check_type[2]) for v in var) for var in variable) and check_type[3] != "list":
        return True

      else:
        raise Exception(f"type too complex")

  # We didn't find the type
  return False

def char_to_ascii(char: str) -> int:
  '''
  converts a character to it's ASCII value
  '''
  try:
    return ord(char) - ASCII_MIN
  except Exception as e:
    print(f"Error: {e}")

def ascii_to_char(char: int) -> str:
  '''
  converts an ASCII value to it's character
  '''
  return chr(char + ASCII_MIN)

def srandascii(mas_de_0 = True) -> int:
  '''
  Securely generates a random ascii character
  if mas_de_0, the number must be greater than 0
  '''
  if not mas_de_0:
    return chr(secrets.randbelow(ASCII_RANGE) + ASCII_MIN)
  else:
    char = 32
    while char == 32:
      char = secrets.randbelow(ASCII_RANGE) + ASCII_MIN
    return chr(char)

def srandstr(length: int, allow_whitespace = False) -> str:
  '''
  Securely generates a random string of length {length}
  If allow_whitespace, the strings can contain ' '
  '''
  string = ""
  for _ in range(length):
    char = srandascii(False) if allow_whitespace else srandascii()
    string += char

  return string

def srandrotorwiring() -> list[int]:
  '''
  Securely generate random rotor wiring
  returning a shuffled ascii list
  '''
  choices = [i for i in range(ASCII_RANGE)]
  wiring: list[int] = []

  while len(choices) > 0:
    index = secrets.randbelow(len(choices))
    wiring.append(choices[index])
    choices.pop(index)

  return wiring

# class for Ascii Enigma Cipher
class Enigma:
  class Keyboard:

    def forward(self, letter: str) -> int: # pass from input
      return char_to_ascii(letter) # signal

    def backward(self, signal: int) -> str: # pass to output
      return chr(signal + ASCII_MIN) # letter

  class Plugboard:

    def __init__(self, plugs: list[str]) -> None:
      # list for wiring
      self.wiring: list[int] = [i for i in range(ASCII_RANGE)]

      # swap wires
      for plug in plugs:
        # get indexes to swap
        a = char_to_ascii(plug[0])
        b = char_to_ascii(plug[1])

        # update wiring
        self.wiring[a], self.wiring[b] = self.wiring[b], self.wiring[a]

    # mutate character based on plugboard
    def forward_and_backward(self, signal: int) -> int:
      return self.wiring[signal]

  class Rotor:

    def __init__(self, wiring: list[int] or str, notch: int = 0) -> None:
      # list for wiring
      if check_type(wiring, [list, int]):
        self.wiring: list[int] = wiring

      elif check_type(wiring, [str]):
        self.wiring: list[int] = [char_to_ascii(wire) for wire in wiring]
      
      else:
        raise Exception(f"Could not initialise wiring with {wiring}")

    def forward_and_backward(self, signal: int) -> int:
      return self.wiring[signal]

  class Reflector:
    def __init__(self, wiring: list[int]) -> None:
        # list for wiring
      if check_type(wiring, [list, int]):
        self.wiring: list[int] = wiring

      elif check_type(wiring, [str]):
        self.wiring: list[int] = [char_to_ascii(wire) for wire in wiring]

    def reflect(self, signal: int) -> int:
      return self.wiring[signal]

  hist_rotors: dict[str, Rotor] = { # historical settings from wikipedia

    # Commercial Enigma A, B
    "IC": Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV"),
    "IIC": Rotor("HQZGPJTMOBLNCIFDYAWVEUSRKX"),
    "IIIC": Rotor("UQNTLSZFMREHDPXKIBVYGJCWOA"),

    # Swiss K
    "I-K": Rotor("PEZUOHXSCVFMTBGLRINQJWAYDK"),
    "II-K": Rotor("ZOUESYDKFWPCIQXHMVBLGNJRAT"),
    "III-K": Rotor("EHRVXGAOBQUSIMZFLYNWKTPDJC"),
    "UKW-K": Rotor("IMETCGFRAYSQBZXWLHKDVUPOJN"),
    "ETW-K": Rotor("QWERTZUIOASDFGHJKPYXCVBNML"),

    # Enigma I
    "I": Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ"),
    "II": Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE"),
    "III": Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO"),

    # M3 Army
    "IV": Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB"),
    "V": Rotor("VZBRGITYUPSDNHLXAWMJQOFECK"),

    # M3 & M4 Naval
    "VI": Rotor("JPGVOUMFYQBENHZRDKASXLICTW"),
    "VII": Rotor("NZJHGRCXMYSWBOUFAIVLPEKQDT"),
    "VIII": Rotor("FKQHTLXOCBJSPDZRAMEWNIUYGV"),
  }

  hist_reflectors: dict[str, Reflector] = { # historical settings from wikipedia

    # Model Name & Number unknown
    "A": Reflector("EJMZALYXVBWFCRQUONTSPIKHGD"),
    "B": Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT"),
    "C": Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL"),

    # M4 R2
    "Beta": Reflector("LEYJVCNIXWPBQMDRTAKZGFUHOS"),
    "Gamma": Reflector("FSOKANUERHMBTIYCWLQPZXVGJD"),

    # M4 R1 (M3 + Thin)
    "B Thin": Reflector("ENKQAUYWJICOPBLMDXZVFTHRGS"),
    "C Thin": Reflector("RDOBJNTKVEHMLFCWZAXGYIPSUQ"),

    # Enigma I
    "ETW": Reflector("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
  }

  def __init__(self,
               use_hist_rotors: bool,
               rotors: list[str] or list[list[int]],
               use_hist_reflectors: bool,
               reflector: list[int] or str,
               plugboard: list[str] or None) -> None:

    # === initialize rotors ===

    # historical settings using key: value pairs
    if use_hist_rotors and check_type(rotors, [list, str]):
      self.rotors: list[Enigma.Rotor] = []
      for rotor in rotors:
        self.rotors.append(Enigma.hist_rotors[rotor])

    # custom settings as a list list of ints for signals
    elif check_type(rotors, [list, list, int]):
      self.rotors: list[Enigma.Rotor] = []
      for rotor in rotors:
        self.rotors.append(Enigma.Rotor(rotor))

    # Rotor also accepts a list of strs for signals
    elif check_type(rotors, [list, str]):
      self.rotors: list[Enigma.Rotor] = []
      for rotor in rotors:
        self.rotors.append(Enigma.Rotor(rotor))

    # invalid
    else:
      raise Exception(f"Invalid rotor assignment: {rotors}\nExpected type list[list[int]] or list[str], got {type(rotors)}")

    # === initialise reflector ===
    
    # historical settings
    if use_hist_reflectors and check_type(reflector, [str]):
      self.reflector: Enigma.Reflector = Enigma.hist_reflectors[reflector]

    # custom settings
    elif not use_hist_reflectors and (check_type(reflector, [str]) or check_type(reflector, [list, int])):
      self.reflector: Enigma.Reflector = Enigma.Reflector(reflector)

    else:
      raise Exception(f"Invalid reflector assignment: {rotors}\nExpected type str or list[int], got {type(rotors)}")

    # === initialise plugboard ===
    if check_type(plugboard, [list, str]) or plugboard == None:
      self.plugboard: Enigma.Plugboard = Enigma.Plugboard(plugboard)
        
    else:
      raise Exception(f"Invalid plugboard assignment: {plugboard}\nExcepted type list[str] or None, got {type(plugboard)}")

    # === initialize keyboard ===
    self.keyboard = Enigma.Keyboard()

  def pass_message(self, message: str):
    '''
    passes a provided message through the enigma
    '''
    result: str = ""
    
    for char in plaintext:
      signal = self.keyboard.forward(char)                 # keyboard first
      signal = self.plugboard.forward_and_backward(signal) # then plugboard
      for rotor in self.rotors:                           
        signal = rotor.forward_and_backward(signal)        # then rotors
      signal = self.reflector.reflect(signal)              # reflector
      for rotor in self.rotors[::-1]:                           
        signal = rotor.forward_and_backward(signal)        # rotors again (reverse order)
      signal = self.plugboard.forward_and_backward(signal) # plugboard again
      result += self.keyboard.backward(signal)             # finally append to result

def gen_random_strs(amount: int, length: int) -> list[str]:
  '''
  Generates {amount} random strings of length {length}
  '''
  random_strs: list[str] = []
  for _ in range(amount): # generate {amount} strings
    random_strs.append(srandstr(length))

  return random_strs

def populate_mod_list(length: int) -> ModResults:
  return [[0, 0] for i in range(length)]

def get_key_letters(keys: list[str], index: int) -> list[int]:
  '''
  Returns each letter in keys at the specified index
  '''

  return [char_to_ascii(keys[i][index]) for i in range(len(keys))]

def do_math(keys: list[str], message: str, mod_results: ModResults) -> EncryptedMessage:
  result = ""

  # for each character
  for i in range(len(message)):
    char = char_to_ascii(message[i])

    # a is key letters we're focusing on
    a = get_key_letters(keys, i)

    # math time!
    char = char + a[0] % ASCII_RANGE
    char = char + a[1] % ASCII_RANGE

    # append
    result += ascii_to_char(char)

  return EncryptedMessage(result, mod_results[::-1])

def undo_math(keys: list[str], message: str, mod_results: ModResults) -> str:
  result = ""

  # for each char
  for i in range(len(message)):

    # get char undoing mod
    char = char_to_ascii(message[i]) + (mod_results[i][0] * ASCII_RANGE)

    # a is key letters we're focusing on
    a = get_key_letters(keys, i)

    # math time!
    char = char - a[1] % ASCII_RANGE
    char = char - a[0] % ASCII_RANGE

    # append char
    result += ascii_to_char(char)

  return result

def encrypt_message(plaintext: str, keys: list[str]) -> EncryptedMessage:

  # list of lists for each time mod is used
  mod_results: ModResults = populate_mod_list(len(plaintext))

  # strings to store encrypted message through stages
  encrypted_message: EncryptedMessage

  # First pass
  encrypted_message = do_math(keys, plaintext, mod_results)

  # Pass through 16 rotor 3 reflector enigma

  # return
  return encrypted_message

def decrypt_message(encrypted_message: EncryptedMessage, keys: list[str]) -> str:
  decrypted_message = ""

  # get mod_results
  mod_results: ModResults = encrypted_message.mod_results[::-1] # reverse list

  # undo first pass
  decrypted_message = undo_math(keys, encrypted_message.message, mod_results)

  # return
  return decrypted_message

def main() -> None:
  # plaintext
  plaintext: str = "Hello. I like rice."

  # plaintext length
  length = len(plaintext)

  # get encryption strings
  encryption_strings = gen_random_strs(4, length)

  # encrypt
  ciphertext = encrypt_message(plaintext, encryption_strings)

  # decrypt
  decrypted_text = decrypt_message(ciphertext, encryption_strings)

  print(f"Message: {plaintext}")
  print(f"Cipher text: {ciphertext.message}")
  print(f"Keys: {encryption_strings}")
  print(f"Decrypted text: {decrypted_text}")
  '''
  if plaintext != decrypted_text:
    raise Exception(f"Plaintext is not equal to decrypted_text: {plaintext} - {decrypted_text}")
  '''
if __name__ == "__main__":
  #main()
  rotors = ["I", "II", "III", "IV", "V"]
  reflector = "A"
  plugboard = ["AF", "CR", "EQ"]
  machine = Enigma(True, rotors, True, reflector, plugboard)
  plaintext = "Hello. I like rice."
  encrypted_text = machine.pass_message(plaintext)
  decrypted_text = machine.pass_message(plaintext)

  print(f"Plain Text: {plaintext}")
  print(f"Encrypted Text: {encrypted_text}")
  print(f"Decrypted Text: {decrypted_text}")

# Citations:
# Enigma Historical Settings: https://en.m.wikipedia.org/wiki/Enigma_rotor_details
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

# class for Ascii Enigma Cipher
class Enigma:
  class Keyboard:

    def forward(self, letter: str) -> int: # pass from input
      return ord(letter) - ASCII_MIN # signal

    def backward(self, signal: int) -> str: # pass to output
      return chr(signal + ASCII_MIN) # letter

  class Plugboard:

    def __init__(self, plugs: list[str]) -> None:
      # list for wiring
      self.wiring: list[int] = [i for i in range(ASCII_RANGE)]

      # swap wires
      for plug in plugs:
        # get indexes to swap
        a = ord(plug[0]) - ASCII_MIN
        b = ord(plug[1]) - ASCII_MIN

        # update wiring
        self.wiring[a], self.wiring[b] = self.wiring[b], self.wiring[a]

    # mutate character based on plugboard
    def forward_and_backward(self, signal: int) -> int:
      return self.wiring[signal]

  class Rotor:

    def __init__(self, wiring: list[int] or str, notch: int = 0) -> None:
      # list for wiring
      if type(wiring) == list[int]:
        self.wiring: list[int] = wiring

      elif type(wiring) == str:
        self.wiring: list[int] = [char_to_ascii(wire) for wire in wiring]

    def forward_and_backward(self, signal: int) -> int:
      return self.wiring[signal]

  class Reflector:
    def __init__(self, wiring: list[int]) -> None:
        # list for wiring
      if type(wiring) == list[int]:
        self.wiring: list[int] = wiring

      elif type(wiring) == list[str]:
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
               rotors: list[int] or list[list[int]] or list[list[str]],
               use_hist_reflectors: bool,
               reflector: list[int] or list[str] or int,
               plugboard: list[str] or None) -> None:

    # === initialize rotors ===
    if isinstance(rotors, list):

      # historical settings using key: value pairs
      if use_hist_rotors and all(isinstance(rotor, int) for rotor in rotors):
        self.rotors: list[Enigma.Rotor] = []
        for rotor in rotors:
          self.rotors.append(Enigma.hist_rotors[rotor])

      # custom settings as a list list of ints for signals
      elif all(
          isinstance(rotor, list) 
          and all(isinstance(wire, int) 
          for wire in rotor)
          for rotor in rotors
      ):
        self.rotors: list[list[int]] = []
        for rotor in rotors:
          self.rotors.append(Enigma.Rotor(rotor))

      # Rotor also accepts a list of strs for signals
      elif all(isinstance(rotor, str)
      for rotor in rotors):
        self.rotors: list[list[str]] = []
        for rotor in rotors:
          self.rotors.append(Enigma.Rotor(rotor))

      else:
        raise Exception(f"Invalid rotor assignent: {rotors}\nEXpected type list[list[int]] or list[str], got {type(rotors)}")

    # invalid
    else:
      raise Exception(f"Invalid rotor assignment: {rotors}\nExpected type list[int] or list[list[int]] or list[str], got {type(rotors)}")

    # === initialise reflectors ===
    if isinstance(reflector, list):

      # historical settings
      if use_hist_reflectors and all(
        isinstance(wire, str) for wire in reflector
      ):
        self.reflector = Enigma.hist_reflectors[reflector]

      # custom settings
      elif not use_hist_reflectors:
        self.reflector = Enigma.Reflector(reflector)

    else:
      raise Exception(f"Invalid reflector assignment: {rotors}\nExpected type int or list[int] or list[str], got {type(rotors)}")

    # === initialise plugboard ===
    if isinstance(plugboard, list[str]) or isinstance(plugboard, None):
      self.plugboard = Enigma.Plugboard(plugboard)

    else:
      raise Exception(f"Invalid plugboard assignment: {plugboard}\nExcepted type list[str] or None, got {type(plugboard)}")

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


'''
Citations:
Enigma Historical Settings: https://en.m.wikipedia.org/wiki/Enigma_rotor_details
'''
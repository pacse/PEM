# PEM Version Delta – Works
import copy
import secrets
from dataclasses import dataclass
from typing import Tuple, List, TypeAlias

ModResults: TypeAlias = List[List[int]]

@dataclass
class EncryptedMessage:
  message: str
  mod_results: ModResults

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A = ord("A")

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

# class for Enigma Cipher
def check_type(variable, check_types: list[type]) -> bool:
  '''
  Checks if a variable is equal to a type with a list of types
  eg. to check for list[list[int]] check_type = [list, list, int]
  '''
  # no types specified
  if not check_types:
    return True

  # just check the first type
  check = check_types[0]
  if not isinstance(variable, check):
    return False
  # variable is equal to check type

  if check != list: # no more checking needed
    return True

  if len(check_types) > 1:
    # recursively check variable for lists of lists ect
    return all(check_type(item, check_types[1:]) for item in variable)

  # final fallback
  return True # hasn't triggered anything else, could just be check_type == list

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

def alpha_to_index(char: str) -> int:
  '''
  converts a capital character to it's alphabetical index
  '''
  if len(char) != 1:
    raise Exception(f"Char: {char!r} is longer than 1")

  return ord(char.upper()) - A + 1

def ascii_to_index(char: int) -> str:
  '''
  converts an alphabetical index to it's capital character
  '''
  if char > 26:
    raise Exception(f"Char: {char!r} is greater than 25 (Z)")

  return chr(char + A - 1)

def srandrotorwiring() -> list[int]:
  '''
  Securely generate random rotor wiring
  returning a shuffled ascii list

  choices = [i for i in range(ASCII_RANGE)]
  wiring: list[int] = []
  '''
  choices = [i for i in range(len(ALPHABET))]
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
      return ord(letter) - ord("A") # signal

    def backward(self, signal: int) -> str: # pass to output
      return chr(signal + ord("A")) # letter

  class Plugboard:

    def __init__(self, plugs: list[str]) -> None:
      plugs = plugs if plugs != None else []
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

    def __init__(self,
                 wiring: list[int] or str,
                 notch: list[int] or str or None = None) -> None:

      # current position in "window"
      self.position = 0

      # list for wiring
      if check_type(wiring, [list, int]):
        self.wiring: list[int] = wiring

      elif check_type(wiring, [str]):
        self.wiring: list[int] = [ord(wire) - A for wire in wiring]

      else:
        raise Exception(f"Could not initialise wiring with {wiring!r}")

      self.reverse_wiring = [0] * len(self.wiring)
      for index, value in enumerate(self.wiring):
        self.reverse_wiring[value] = index

      # === Inititalize self.notch ===
      if notch is None:
        self.notch = None

      elif check_type(notch, [str]):
        self.notch = [alpha_to_index(letter) - 1 for letter in notch]

      elif check_type(notch, [list, int]):
        self.notch = notch

      else:
        raise Exception(f"Notch type invalid with {notch!r}")

    def forward(self, signal: int) -> int:
      return self.wiring[signal]

    def backward(self, signal: int) -> int:
      return self.reverse_wiring[signal]

    def rotate(self, n = 1, is_forward = True) -> None:
      # rotate wiring
      for _ in range(n):
        if is_forward:
          self.wiring = self.wiring[1:] + [self.wiring[0]]
          self.position = (self.position + 1) % 26
        else:
          self.wiring = [self.wiring[-1]] + self.wiring[:-1]
          self.position = (self.position - 1) % 26

      # update reverse wiring
      self.reverse_wiring = [0] * len(self.wiring)
      for index, value in enumerate(self.wiring):
        self.reverse_wiring[value] = index

    def set_ring(self, position: int) -> None:
      self.rotate(position-1, is_forward=False)

      # find where the notch is
      if self.notch is not None:
        new_notch_positions = []
        for notch in self.notch:
          new_notch_positions.append(self.wiring.index(notch))
        self.notch = new_notch_positions

    def rotate_to_letter(self, letter):
      index = ord(letter.upper()) - A
      rotations = (index - self.position) % 26
      self.rotate(rotations)

  class Reflector:
    def __init__(self, wiring: list[int] or str) -> None:
        # list for wiring
      if check_type(wiring, [list, int]):
        self.wiring: list[int] = wiring

      elif check_type(wiring, [str]):
        self.wiring: list[int] = [ord(wire) - A for wire in wiring]

    def reflect(self, signal: int) -> int:
      return self.wiring[signal]

  hist_rotors: dict[str, Rotor] = { # historical settings from wikipedia

    # Commercial Enigma A, B (stepped together, no notches)
    "IC": Rotor("DMTWSILRUYQNKFEJCAZBPGXOHV"),
    "IIC": Rotor("HQZGPJTMOBLNCIFDYAWVEUSRKX"),
    "IIIC": Rotor("UQNTLSZFMREHDPXKIBVYGJCWOA"),

    # Swiss K (stepped together, no notches)
    "I-K": Rotor("PEZUOHXSCVFMTBGLRINQJWAYDK"),
    "II-K": Rotor("ZOUESYDKFWPCIQXHMVBLGNJRAT"),
    "III-K": Rotor("EHRVXGAOBQUSIMZFLYNWKTPDJC"),
    "UKW-K": Rotor("IMETCGFRAYSQBZXWLHKDVUPOJN"),
    "ETW-K": Rotor("QWERTZUIOASDFGHJKPYXCVBNML"),

    # Enigma I
    "I": Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),

    # M3 Army
    "IV": Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),

    # M3 & M4 Naval
    "VI": Rotor("JPGVOUMFYQBENHZRDKASXLICTW", "ZM"),
    "VII": Rotor("NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM"),
    "VIII": Rotor("FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM"),
  }

  hist_reflectors: dict[str, Reflector] = { # historical settings from wikipedia

    # Model Name & Number unknown
    "A": Reflector("EJMZALYXVBWFCRQUONTSPIKHGD"),
    "B": Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT"),
    "C": Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL"),

    # M4 R1 (M3 + Thin)
    "B Thin": Reflector("ENKQAUYWJICOPBLMDXZVFTHRGS"),
    "C Thin": Reflector("RDOBJNTKVEHMLFCWZAXGYIPSUQ"),

    # Enigma I
    "ETW": Reflector("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
  }

  def __init__(self,
               hist_rotors: bool,
               rotors: list[str] or list[list[int]],
               start_positions: str,
               hist_reflectors: bool,
               reflector: list[int] or str,
               plugboard: list[str] or None,
               key: str) -> None:

    # === initialize rotors ===

    # validate start positions
    if len(start_positions) != len(rotors):
      raise Exception(f"Not enough start positions for rotors {start_positions!r}\nExpected {len(rotors)}, got {len(start_positions)}")

    # historical settings using dictionary
    if hist_rotors and check_type(rotors, [list, str]):
      self.rotors: list[Enigma.Rotor] = [] # init rotor list
      for rotor in rotors:
        self.rotors.append(copy.deepcopy(Enigma.hist_rotors[rotor])) # deepcopy for a new instance

    # custom settings as list[list[int]] for signals
    elif not hist_rotors and check_type(rotors, [list, list, int]):
      self.rotors: list[Enigma.Rotor] = [] # init rotor list
      for rotor in rotors:
        self.rotors.append(Enigma.Rotor(rotor)) # append rotor

    # Rotor also accepts list[str] for signals
    elif not hist_rotors and check_type(rotors, [list, str]):
      self.rotors: list[Enigma.Rotor] = [] # init rotor list
      for rotor in rotors:
        self.rotors.append(Enigma.Rotor(rotor)) # append rotor

    # invalid
    else:
      raise Exception(f"Invalid rotor assignment with {rotors!r}\nExpected type list[list[int]] or list[str]")

    # store initial rotor positions
    self.initial_positions = [alpha_to_index(pos) - 1 for pos in start_positions]

    # store initial wirings for reset function
    self.initial_wirings = []
    self.initial_reverse_wirings = []
    for rotor in self.rotors:
      self.initial_wirings.append(rotor.wiring)
      self.initial_reverse_wirings.append(rotor.reverse_wiring)

    # rotate to start positions
    for i, rotor in enumerate(self.rotors):
      rotor.rotate_to_letter(start_positions[i])

    # === initialise reflector ===

    # historical settings
    if hist_reflectors and check_type(reflector, [str]):
      self.reflector: Enigma.Reflector = copy.deepcopy(Enigma.hist_reflectors[reflector]) # deepcopy for a new instance

    # custom settings
    elif not hist_reflectors and (check_type(reflector, [str]) # Allowed types:
    or check_type(reflector, [list, int])):                    # str, list[int]
      self.reflector: Enigma.Reflector = Enigma.Reflector(reflector)

    # invalid
    else:
      raise Exception(f"Invalid reflector assignment: {reflector!r}\nExpected type str or list[int]")

    # === initialise plugboard ===
    if check_type(plugboard, [list, str]) or plugboard == None: # Accept types list[str] or None
      self.plugboard: Enigma.Plugboard = Enigma.Plugboard(plugboard)

    # invalid
    else:
      raise Exception(f"Invalid plugboard assignment: {plugboard!r}\nExcepted type list[str] or None")

    # === initialize keyboard ===
    self.keyboard = Enigma.Keyboard()

  def reset(self) -> None:
    '''
    resets rotors to starting positions
    '''
    for i, rotor in enumerate(self.rotors):
      rotor.position = 0 # reset position
      rotor.wiring = copy.deepcopy(self.initial_wirings[i]) # set wiring
      rotor.reverse_wiring = copy.deepcopy(self.initial_reverse_wirings[i]) # & reverse wiring
      rotor.rotate(self.initial_positions[i]) # rotate to init pos

  def set_key(self, key: str) -> None:
    '''
    sets rotors to begin with key
    '''
    # ensure we have enough keys (sanity check)
    if len(key) != len(self.rotors):
      raise Exception(f"Key length ({len(key)}) does not equal number of rotors ({len(self.rotors)})")

    for i, letter in enumerate(key):
      # i is key index, letter is letter at index
      self.rotors[i].rotate_to_letter(letter)

  def set_rings(self, rings: str):
    '''
    moves the notch of a rotor through rotor shifting
    '''
    # ensure we have enough rings (sanity check)
    if len(rings) != len(self.rotors):
      raise Exception(f"provided rings ({rings!r}, length: {len(rings)}) does not equal number of rotors ({len(self.rotors)})")

    for i, ring in enumerate(rings):
      # i is ring index, ring is ring at index
      position = alpha_to_index(ring)
      self.rotors[i].set_ring(position)

  def step_rotors(self, n = 1) -> None:
    '''
    step rotors n times, cascading if applicable
    '''
    for _ in range(n):
      rotor_length = len(self.rotors)

      # list of rotors that should step
      do_step = [False] * rotor_length

      # rightmost rotor always steps
      do_step[-1] = True

      # traverse do_step right to left
      # checking which rotors should step.
      # if rtr i is stepping and is at
      # notch, rtr i-1 steps too.
      for i in range(rotor_length-1, 0, -1):
        if (do_step[i] and self.rotors[i].notch) and self.rotors[i].position in self.rotors[i].notch: # at notch and stepping
          do_step[i-1] = True

      #print(f"[DEBUG] Rotor Stepping Flags: {do_step}")  # << Add this

      # apply rotor stepping
      for index, rotor in enumerate(self.rotors):
        if do_step[index]:
          rotor.rotate()

  def pass_message(self, message: str, key: str):
    '''
    passes a provided message through the enigma
    '''
    result: str = ""

    # position rotors for message key
    self.set_key(key)

    for char in message:
      char = char.upper()
      #print(f"[DEBUG] Input Char: {char}, Rotor Positions Before Step: {[r.position for r in self.rotors]}")
      # step rotors
      self.step_rotors()
      #print(f"[DEBUG] Rotor Positions After Step: {[r.position for r in self.rotors]}")
      if char not in ALPHABET:
        result += char

      else:
        signal = self.keyboard.forward(char)                 # keyboard first
        signal = self.plugboard.forward_and_backward(signal) # then plugboard

        for rotor in self.rotors[::-1]:                      # left to right rotors
          signal = rotor.forward(signal)

        signal = self.reflector.reflect(signal)              # reflector

        for rotor in self.rotors:                            # rotors again (right to left)
          signal = rotor.backward(signal)
        signal = self.plugboard.forward_and_backward(signal) # plugboard again
        result += self.keyboard.backward(signal)             # finally append to result

    return result

def gen_random_strs(amount: int, length: int) -> list[str]:
  '''
  Generates {amount} random strings of length {length}
  '''
  random_strs: list[str] = []
  for _ in range(amount): # generate {amount} strings
    random_strs.append(srandstr(length))

  return random_strs

def populate_mod_list(length: int) -> ModResults:
  '''
  depricated
  '''
  return [[0, 0] for i in range(length)]

def get_key_letters(keys: list[str], index: int) -> list[int]:
  '''
  Returns each letter in keys at the specified index
  '''

  return [char_to_ascii(keys[i][index]) for i in range(len(keys))]

def do_math(keys: list[str], message: str, mod_results: ModResults) -> EncryptedMessage:
  '''

  '''
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
  key = "A" * 5
  machine = Enigma(True, rotors, key, True, reflector, plugboard, key)
  plaintext = "Hello. I like rice."
  encrypted_text = machine.pass_message(plaintext, key)
  decrypted_text = machine.pass_message(encrypted_text, key)

  print(f"Plain Text: {plaintext}")
  print(f"Encrypted Text: {encrypted_text}")
  print(f"Decrypted Text: {decrypted_text}")

# Citations:
# Enigma Historical Settings: https://en.m.wikipedia.org/wiki/Enigma_rotor_details
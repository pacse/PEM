# PEM Version Gamma – WORKS
import secrets
from dataclasses import dataclass
from typing import List, TypeAlias

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

def char_to_ascii(char: str) -> int:
  '''
  converts a character to it's ASCII value
  '''
  return ord(char) - ASCII_MIN

def ascii_to_char(char: int) -> str:
  '''
  converts an ASCII value to it's character
  '''
  return chr(char + ASCII_MIN)

def srandascii(mas_de_0: bool = True) -> str:
  '''
  Securely generates a random ascii character
  if mas_de_0, the number must be greater than 0
  '''
  if not mas_de_0:
    char = secrets.randbelow(ASCII_RANGE) + ASCII_MIN
  else:
    char = 32
    while char == 32:
      char = secrets.randbelow(ASCII_RANGE) + ASCII_MIN

  return chr(char)

def srandstr(length: int, allow_whitespace: bool = False) -> str:
  '''
  Securely generates a random string of length {length}
  If allow_whitespace, the strings can contain ' '
  '''
  string = ""
  for _ in range(length):
    char = srandascii(False) if allow_whitespace else srandascii()
    string += char

  return string

def gen_random_strs(amount: int, length: int) -> list[str]:
  '''
  Generates {amount} random strings of length {length}
  '''
  random_strs: list[str] = []
  for _ in range(amount): # generate {amount} strings
    random_strs.append(srandstr(length))

  return random_strs

def populate_mod_list(length: int) -> ModResults:
  return [[0, 0] for _ in range(length)]

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
  main()
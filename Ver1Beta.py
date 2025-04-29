# PEM Version Beta – NOT FUNCTIONAL
import secrets
from math import sin, cos

HASH_LEN = 500 # character limit for messages

#message: str = "Hello. I like rice."
#ciphertext: str = ""
#decrypted_text: str = ""

ASCII_MIN = 32 # first unicode ascii character
ASCII_MAX = 127 # last unicode ascii character
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

def gen_random_strs(amount: int, length: int = HASH_LEN) -> list[str]:
  '''
  Generates {amount} random strings of length {length}
  '''
  random_strs: list[str] = []
  for _ in range(amount):   # generate {amount} strings
    tmp_str: str = ""

    for _ in range(length): # of length {length}
      tmp_str += chr(secrets.randbelow(ASCII_RANGE) + ASCII_MIN) # append random character

    random_strs.append(tmp_str)

  return random_strs

'''
Quadratic map for encryption:
xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y + a[6] * sin(x) + a[7] * cos(y)
ynew = a[8] + a[9]*x + a[10]*x*x + a[11]*y + a[12]*y*y + a[13]*x*y + a[14] * sin(y) + a[15] * cos(x)
'''

def encrypt_message(plaintext: str, encrypt_strings: list[str] = gen_random_strs(17)) -> str:
  encrypted_message: str = ""
  new_plaintext: str = ""

  # first ensure message is the proper length
  for i in range(len(encrypt_strings[1])):
    try:
      plaintext_char = char_to_ascii(plaintext[i])
      hash_char = char_to_ascii(encrypt_strings[1][i])
      cipher_char = (plaintext_char + hash_char) % ASCII_RANGE

      new_plaintext += ascii_to_char(cipher_char)
    except IndexError:
      new_plaintext += encrypt_strings[1][i]

  # now properly encrypt
  for i in range(0, len(new_plaintext)-1, 2): # for every other character

    # x & y are char we're focusing on and char we're 'skipping'
    x, y = char_to_ascii(new_plaintext[i]), char_to_ascii(new_plaintext[i+1])

    # a is the ith or ith+1 character in encrypt_strings[1]-[15]
    a: list[int] = []
    for j in range(1, 17):
      # alternate between focused and 'skipped' char
      if j % 2 == 1:
        a.append(char_to_ascii(encrypt_strings[j][i]))
      else:
        a.append(char_to_ascii(encrypt_strings[j][i+1]))

    # quadratic map time!
    xnew = a[0] + a[1]*x + a[2]*x*x + a[3]*y + a[4]*y*y + a[5]*x*y + a[6] * sin(x) + a[7] * cos(y)
    ynew = a[8] + a[9]*x + a[10]*x*x + a[11]*y + a[12]*y*y + a[13]*x*y + a[14] * sin(y) + a[15] * cos(x)

    # update encrypted_message
    encrypted_message += ascii_to_char(round(xnew) % ASCII_RANGE)
    encrypted_message += ascii_to_char(round(ynew) % ASCII_RANGE)

  return encrypted_message

def decrypt_message(encrypted_message: str, encrypt_strings: list[str]) -> str:
  decrypted_message: str = ""

  # undo proper encryption
  for i in range(0, len(encrypted_message)-1, 2): # for every other character

    # x & y are char we're focusing on and char we're 'skipping'
    x, y = char_to_ascii(encrypted_message[i]), char_to_ascii(encrypted_message[i+1])

    # a is the ith or ith+1 character in encrypt_strings[1]-[15]
    a: list[int] = []
    for j in range(0, 16):
      # alternate between focused and 'skipped' char
      if j % 2 == 0:
        a.append(char_to_ascii(encrypt_strings[j][i]))
      else:
        a.append(char_to_ascii(encrypt_strings[j][i+1]))

    # quadratic map time!
    xnew = a[0] - a[1]*x - a[2]*x*x - a[3]*y - a[4]*y*y - a[5]*x*y - a[6] * sin(x) - a[7] * cos(y)
    ynew = a[8] - a[9]*x - a[10]*x*x - a[11]*y - a[12]*y*y - a[13]*x*y - a[14] * sin(y) - a[15] * cos(x)

    # update encrypted_message
    decrypted_message += ascii_to_char(round(xnew) % ASCII_RANGE)
    decrypted_message += ascii_to_char(round(ynew) % ASCII_RANGE)

  # final decryption
  final_decrypt = ""
  for i in range(len(decrypted_message)):
    try:
      cipher_char = char_to_ascii(decrypted_message[i])
      hash_char = char_to_ascii(encrypt_strings[1][i])
      decrypted_char = (cipher_char - hash_char) % ASCII_RANGE

      final_decrypt += ascii_to_char(decrypted_char)

    except IndexError:
      break

  return final_decrypt

def main() -> None:
  encryption_strings = gen_random_strs(17)

  message: str = "Hello. I like rice."
  ciphertext = encrypt_message(message, encryption_strings)

  decrypted_text = decrypt_message(ciphertext, encryption_strings)

  print(f"Message: {message}")
  print(f"Cipher text: {ciphertext}")
  print(f"Decrypted text: {decrypted_text}")

if __name__ == "__main__":
  main()
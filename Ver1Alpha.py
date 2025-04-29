# PEM V Alpha – WORKS
import secrets

HASH_LEN = 400
hash: str = ""

plaintext: str = "Hello. I like rice."
ciphertext: str = ""
decrypted_text: str = ""

ASCII_MIN = 32 # first unicode ascii character
ASCII_MAX = 127 # last unicode ascii character
ASCII_RANGE = ASCII_MAX - ASCII_MIN + 1 # total unicode ascii characters

# generate hash with printable ascii
for i in range(HASH_LEN):
  hash += chr(secrets.randbelow(ASCII_RANGE) + ASCII_MIN)

# hash plaintext
for i in range(HASH_LEN):
  try:
    hash_char = ord(hash[i]) - ASCII_MIN
    plaintext_char = ord(plaintext[i]) - ASCII_MIN
    cipher_char = (hash_char + plaintext_char) % ASCII_RANGE

    ciphertext += chr(cipher_char + ASCII_MIN)

  except IndexError:
    ciphertext += hash[i]

print(ciphertext)

# decrypt
for i in range(HASH_LEN):
  hash_char = ord(hash[i]) - ASCII_MIN
  encrypted_char = ord(ciphertext[i]) - ASCII_MIN
  decrypted_char = (encrypted_char - hash_char) % ASCII_RANGE

  decrypted_text += chr(decrypted_char + ASCII_MIN)

print(f"\nDecrypted Text: {decrypted_text}")
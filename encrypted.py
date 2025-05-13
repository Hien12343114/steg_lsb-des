from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import binascii

def encrypt_des(message, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(message.encode(), DES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text

message = "Secret message"
key = b"8bytekey"  # Khóa DES phải dài 8 byte
encrypted = encrypt_des(message, key)
print("Encrypted:", binascii.hexlify(encrypted))

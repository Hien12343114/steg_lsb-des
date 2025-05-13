from PIL import Image
import numpy as np
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad

def extract_message(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)
    bits = ""
    
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):
                bits += str(pixels[i, j, k] & 1)
                if len(bits) >= 136:
                    extracted_bits = bits[:128]
                    terminator = bits[128:136]
                    if terminator == "00000000":
                        return extracted_bits
                    else:
                        return ""
    return ""

def decrypt_des(encrypted, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted)
    return unpad(decrypted, DES.block_size).decode()

try:
    bits = extract_message("output.png")
    if not bits:
        print("Error: No message found in the image.")
        exit(1)
    
    if len(bits) % 8 != 0:
        print("Error: Bit length is not a multiple of 8. Cannot convert to bytes.")
        exit(1)
    
    encrypted = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    key = b"8bytekey"
    decrypted = decrypt_des(encrypted, key)
    
    print("Decrypted message:", decrypted)

except FileNotFoundError:
    print("Error: output.png not found.")
except Exception as e:
    print("Error during extraction or decryption:", str(e))

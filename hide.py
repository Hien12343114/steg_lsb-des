from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from PIL import Image
import numpy as np

def encrypt_des(message, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(message.encode(), DES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text

def message_to_bin(message):
    return ''.join(format(byte, '08b') for byte in message)

def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)
    message_bits = message_to_bin(message) + '00000000'
    bit_index = 0

    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):
                if bit_index < len(message_bits):
                    pixels[i, j, k] = (pixels[i, j, k] & ~1) | int(message_bits[bit_index])
                    bit_index += 1
                else:
                    break
            if bit_index >= len(message_bits):
                break
        if bit_index >= len(message_bits):
            break

    Image.fromarray(pixels).save(output_path)
    print("Message hidden in", output_path)

message = "Secret message"
key = b"8bytekey"
encrypted = encrypt_des(message, key)
hide_message("input.png", encrypted, "output.png")

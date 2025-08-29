from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# pads string s with b'\x20' to specific length
def pad(s):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(s)
    padded_data += padder.finalize()
    return padded_data


if __name__ == "__main__":
    plaintext = "Keep it secret. Keep it safe."
    key = "bd3dd3bbf6cec43fc354c3bf1a86d0bd84809f8fa93772c8f8b719f0a08c8449"
    iv = "7f6989cb19f65b3e6fd13648f4e97fd5"
    ciphertext = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"

    # input type check
    if type(ciphertext) is not bytes:
        ciphertext = bytes.fromhex(ciphertext)
    if type(plaintext) is not bytes:
        plaintext = plaintext.encode()
    if type(key) is not bytes:
        key = bytes.fromhex(key)
    if type(iv) is not bytes:
        iv = bytes.fromhex(iv)

    print(f"ciphertext: {ciphertext}")
    print(f"plaintext: {plaintext}")
    print(f"key: {key}")
    print(f"iv: {iv}")

    plaintext = pad(plaintext)
    
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ct = encryptor.update(plaintext)
    print(f'CIPHER TEXT: {ct}')
    ct += encryptor.finalize()
    print(f'CIPHER TEXT: {ct}')

# def find_key_from_ciphertext(plaintext, ciphertext, all_keys, iv = b'\x00'*16):
#     pt_len = len(plaintext)
#     # check every key for matching ciphertext and plaintext
#     for key in all_keys:
#         # decript ciphertext with current key and iv
#         decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
#         pt = decryptor.update(ciphertext) + decryptor.finalize()
#         # checks for matching plaintext and decrypted plaintext(pt) disregarding values after plaintext
#         if plaintext[:pt_len] == pt[:pt_len]:
#             return key
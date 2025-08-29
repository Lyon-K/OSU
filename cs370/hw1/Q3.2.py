from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# fetches every word and pad/cuts it into an array of byte-like objects
def get_dictionary():
    words = []
    with open('words.txt', 'r') as f:
        for word in f:
            words.append(pad(word[:-1]))
    return words

# pads string s with b'\x20' to specific length
def pad(s, length = 16):
    return s[:length].encode() + b"\x20"*(length - len(s))

# finds matching plaintext and ciphertext using all_keys and iv
def find_key_from_ciphertext(plaintext, ciphertext, all_keys, iv = b'\x00'*16):
    pt_len = len(plaintext)
    # check every key for matching ciphertext and plaintext
    for key in all_keys:
        # decript ciphertext with current key and iv
        decryptor = Cipher(algorithms.AES128(key), modes.CBC(iv)).decryptor()
        pt = decryptor.update(ciphertext) + decryptor.finalize()
        # checks for matching plaintext and decrypted plaintext(pt) disregarding values after plaintext
        if plaintext[:pt_len] == pt[:pt_len]:
            return key


if __name__ == "__main__":
    plaintext = "This is a top secret."
    ciphertext = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"

    # input type check
    if type(ciphertext) is not bytes:
        ciphertext = bytes.fromhex(ciphertext)
    if type(plaintext) is not bytes:
        plaintext = plaintext.encode()

    # finds key using find_key_from_ciphertext
    key = find_key_from_ciphertext(plaintext, ciphertext, keys=get_dictionary())

    # print result of find_key_from_ciphertext
    if key:
        print(f"KEY FOUND: key for ({plaintext}): {key}")
    else:
        print("KEY NOT FOUND IN DICTIONARY")

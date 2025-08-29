import base64
from argparse import ArgumentParser
import secrets
import string
import qrcode
import time
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import getpass

seeds = {
    "HmacSHA1": "3132333435363738393031323334353637383930",
    "HmacSHA256": "3132333435363738393031323334353637383930313233343536373839303132",
    "HmacSHA512": "31323334353637383930313233343536373839303132333435363738393031323334353637383930313233343536373839303132333435363738393031323334"
}
cryptoHashes = { "HmacSHA1": hashes.SHA1, "HmacSHA256": hashes.SHA256, "HmacSHA512": hashes.SHA512 }
DIGITS_POWER = [1,10,100,1000,10000,100000,1000000,10000000,100000000]
iv = b'\x00'*16

def getArgs():
    parser = ArgumentParser()
    parser.add_argument("--generate-qr", action='store_true', default=False, help="generate the secret key and encode it in a QR code.")
    parser.add_argument("--get-otp", action='store_true', default=False, help="generate an OTP corresponding to the secret in the secret.txt.")
    parser.add_argument("--totp-table", action='store_true', default=False, help="Generate the TOTP table in rfc6238 with the shared secret.")
    return parser.parse_args()

def getSecret():
    try:
        with open('secret.txt', 'rb') as f:
            file = f.readlines()
            file = [b''.join(file[:-1]), file[-1]]
    except IOError:
        print("Unable to open secret.txt file")
        exit()
    if len(file) == 1:
        print("Secret.txt is not password protected!")
        return file[0].decode()
    password = getpass.getpass(prompt="Enter secret.txt password: ").zfill(16)
    digest = hashes.Hash(hashes.SHA512())
    digest.update(password.encode())
    passwordHash = digest.finalize()
    if passwordHash != file[0][:-1]:
        print("INVALID PASSWORD")
        exit()
    decryptor = Cipher(algorithms.AES(password.encode()), modes.CBC(iv)).decryptor()
    secret = decryptor.update(file[1]) + decryptor.finalize()
    return secret.decode()

def setSecret(secret):
    password = ''
    while True:
        password = getpass.getpass(prompt="Enter a password of at most 16 characters to encrypt the secret.txt file (Leave blank to not encrypt): ")
        if password == '':
            break
        if len(password) > 16:
            print(f"Password length exceeded 16! Length: {len(password)}")
            continue
        confirmPassword = getpass.getpass(prompt="Re-enter your password to confirm: ")
        if password == confirmPassword:
            break
        else:
            print("Password did not match. Please try again.")
    password = password.zfill(16)
    # save secret to file
    with open('secret.txt', 'wb') as f:
        # Not encrypted
        if password == '0'*16:
            return f.write(secret.encode())
        # hash password
        digest = hashes.Hash(hashes.SHA512())
        digest.update(password.encode())
        passwordHash = digest.finalize()
        # encrypt secret with password as key
        print(f'password.encode(): {password.encode()}')
        encryptor = Cipher(algorithms.AES(password.encode()), modes.CBC(iv)).encryptor()
        secret = encryptor.update(secret.encode()) + encryptor.finalize()
        print(f'secret: {secret}')
        # write to file
        f.writelines([passwordHash, b'\n', secret])

def getRandomKey(length=16):
    return base64.b32encode(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length)).encode()).decode().replace('=','')[:length]

def generateQR(secret = getRandomKey(), email = "keel@oregonstate.edu", issuer = "OSU"):
    if issuer: qr = qrcode.make(data=f"otpauth://totp/{issuer}:{email}?secret={secret}&issuer={issuer}")
    else: qr = qrcode.make(data=f"otpauth://totp/{email}?secret={secret}")
    setSecret(secret)
    qr.save("QR.jpg")

def getOTP(k, T, returnDigits = 6, crypto = "HmacSHA1"):
    if type(k) is not bytes:
        if len(k) % 2:
            k = '0' + k
        k = bytes.fromhex(k.upper())
    msg = bytes.fromhex(str(T).zfill(16))
    h = hmac.HMAC(k, cryptoHashes[crypto]())
    h.update(msg)
    hash = h.finalize()
    # calculate OTP
    offset = hash[len(hash) - 1]%16
    binary = ((hash[offset] & int('7f', 16)) << 24) | ((hash[offset + 1] & int('ff', 16)) << 16) | ((hash[offset + 2] & int('ff', 16)) << 8) | (hash[offset + 3] & int('ff', 16))
    return str(binary % DIGITS_POWER[returnDigits]).zfill(returnDigits)

def TOTPTable():
    testTime = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]
    print(f'Time (sec)  | UTC Time            | Value of T (hex) | TOTP     | Mode   ')
    print(f'-------------------------------------------------------------------------')
    for t in testTime:
        T = hex(int((t - 0) / 30))[2:]
        for algo in cryptoHashes.keys():
            totp = getOTP(seeds[algo], T, 8, algo)
            print(f'{t:<11} | {time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(t))} | {str(T).zfill(16).upper()} | {totp:<8} | {algo}')

def startOTP():
    T = hex(int((time.time() - 0) / 30))[2:]
    secret = getSecret()
    key = ''.join([hex(b).lstrip('0x') for b in base64.b32decode(secret)])
    print(f'OTP: {getOTP(key, T, 6, "HmacSHA1")} (valid for {30 - time.time() % 30:.2f}s)')
    time.sleep(max(0, 29 - time.time() % 30))
    while True:
        if time.time() % 30 == 0:
            T = hex(int((time.time() - 0) / 30))[2:]
            print(f'OTP: {getOTP(key, T, 6, "HmacSHA1")} (valid for {30 - time.time() % 30:.2f}s)')
            time.sleep(29)


if __name__ == "__main__":
    args = getArgs()
    if args.generate_qr:
        generateQR()
    if args.get_otp:
        startOTP()
    if args.totp_table:
        TOTPTable()
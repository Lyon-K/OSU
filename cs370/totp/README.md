# READ ME

usage: 
```sh
totp.py [-h] [--generate-qr] [--get-otp] [--totp-table]
```

Example: 
```sh
python ./totp.py --generate-qr
```

###### **COMMAND LINE OPTIONS**

1. `-h`, `--help`
    - This shows the help menu and exits

2. `--generate-qr`
    - This generates a secret key and encode it in a QR code. The corresponding secret key is encoded then saved in secret.txt. A password will be asked for excryption.
    - secret.txt not encrypted
      - If you do not want secret.txt encrypted, enter no password and you will be able to see the random generated key in secret.txt
    - secret.txt password protected encrypted(extra credit)
      - If you want secret.txt to be encrypted, enter a password and you will notice that secret.txt is no longer readible.
      - You will notice that secret.txt is now 2 lines instead of 1:
         - Line 1: This is a hash of the entered password
         - Line 2: This is the secret key in AES encryption 


3. `--get-otp`
    - This generates an OTP corresponding to the secret in the secret.txt.
    - secret.txt not encrypted (No password)
      - If a password was not entered during the `--generate-qr` phase, a password 
    - secret.txt password protected encrypted(extra credit)
      - When the secret.txt file is password protected, the user must enter a password to access decrypt the secret key.
          1. The password entered must match the SHA256 hash so even if they copied the value in secret.txt it would not work as it would hash to a different value.
          2. The password will then be used as a key to decrypt the secret value in the file, so even an attacker is able to obtain a password that matches the hash, it will not decrypt to the actual secret key because a matching hash doesnt mean a matching password.

4. `--totp-table`
   - This generates the TOTP table in rfc6238 with the shared secret.

## Notes
- This is ran and tested on `Python 3.10.12`
- The secret key stored in secret.txt is encrypted with AES
- The password is hashed and stored
- Secret.txt format when it is encrypted:
  - H(password)||{secret}_password
    > It is seen that we need password which is not obtainable in the txt, and even if we are able to match H(password), we are unable to use that to obtain secret.
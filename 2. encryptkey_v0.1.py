import os
import random
import string
from cryptography.fernet import Fernet

# Function to load the encryption key from a file
# Ensure the "secret.key" file exists in the same directory or update the path
def load_key():
    return open("secret.key", "rb").read()  # <--- Update this path if necessary

# Function to encrypt the password using the loaded key
def encrypt_password(password):
    key = load_key()  # Load the encryption key
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())  # Encrypt the password
    return encrypted_password

# Function to replace the plaintext password in the script with the encrypted one
def overwrite_password_in_script(script_path, new_password):
    with open(script_path, 'r') as file:
        script_lines = file.readlines()

    # Find the line containing the password and replace it with the scrambled version
    for i, line in enumerate(script_lines):
        if line.strip().startswith("my_password ="):
            # Replace with the scrambled password
            script_lines[i] = f'my_password = "{new_password}"  # Password has been scrambled\n'
            break

    # Write the updated lines back to the script
    with open(script_path, 'w') as file:
        file.writelines(script_lines)

# Encrypt the password
# Replace 'my_password' with the actual password before running the script
my_password = "YourPasswordHere"  # <--- Update this with your actual password
encrypted_password = encrypt_password(my_password)  # Encrypt the password
print("Encrypted password:", encrypted_password)

# Scramble the original password or replace it with a random string of the same length
scrambled_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(my_password)))

# Get the current script file path
script_path = os.path.abspath(__file__)  # Automatically gets the path of this script

# Overwrite the password in the script with the scrambled version
overwrite_password_in_script(script_path, scrambled_password)

from cryptography.fernet import Fernet

# Function to generate and store the encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Run this function once to create the key file
generate_key()



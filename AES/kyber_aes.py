import liboqs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Generate Kyber public and private key pair
def generate_kyber_keys():
    kem = liboqs.KEM("Kyber512")
    public_key, private_key = kem.generate_keypair()
    return public_key, private_key

# Encrypt message with AES using a shared secret
def encrypt_aes(plaintext, secret):
    # Use SHA-256 of the shared secret as the AES key
    from hashlib import sha256
    key = sha256(secret).digest()
    
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    
    # Return IV and ciphertext
    return cipher.iv, ciphertext

# Decrypt message with AES using a shared secret
def decrypt_aes(ciphertext, iv, secret):
    from hashlib import sha256
    key = sha256(secret).digest()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()

# Perform the Kyber encapsulation and decapsulation
def key_exchange_and_communicate():
    # Step 1: Alice generates public/private key pair
    alice_public, alice_private = generate_kyber_keys()

    # Step 2: Bob generates public/private key pair
    bob_public, bob_private = generate_kyber_keys()

    # Step 3: Alice encapsulates a message with Bob's public key
    kem = liboqs.KEM("Kyber512")
    shared_secret_alice, ciphertext_alice = kem.encapsulate(bob_public)

    # Step 4: Bob decapsulates the ciphertext with his private key
    shared_secret_bob = kem.decapsulate(ciphertext_alice, bob_private)

    # Ensure the shared secrets match (they should)
    assert shared_secret_alice == shared_secret_bob

    print(f"Shared Secret: {shared_secret_alice.hex()}")

    # Step 5: Encrypt and decrypt a message using AES
    message = "Hello, world! This is a secret message."
    iv, ciphertext = encrypt_aes(message, shared_secret_alice)
    print(f"Ciphertext: {ciphertext.hex()}")

    decrypted_message = decrypt_aes(ciphertext, iv, shared_secret_bob)
    print(f"Decrypted Message: {decrypted_message}")

# Run the communication protocol
if __name__ == "__main__":
    key_exchange_and_communicate()
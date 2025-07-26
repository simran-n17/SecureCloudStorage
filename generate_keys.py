from Crypto.PublicKey import RSA
import os

# Ensure keys folder exists
os.makedirs("keys", exist_ok=True)

# Generate RSA key pair
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Save private key
with open("keys/private_key.pem", "wb") as prv_file:
    prv_file.write(private_key)

# Save public key
with open("keys/public_key.pem", "wb") as pub_file:
    pub_file.write(public_key)

print("RSA Key pair generated successfully.")

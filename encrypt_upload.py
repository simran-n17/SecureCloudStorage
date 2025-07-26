import boto3
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
from config import AWS_BUCKET_NAME, REGION_NAME, PUBLIC_KEY_PATH

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

def encrypt_file(file_path):
    # Generate a random 32-byte AES key
    aes_key = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)  # 128-bit IV for AES

    # Read file content
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    # Encrypt file using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    encrypted_file_path = f"uploads/encrypted_{os.path.basename(file_path)}"
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + ciphertext)

    # Load RSA public key
    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Encrypt AES key using RSA
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    encrypted_key_path = f"uploads/key_{os.path.basename(file_path)}.bin"
    with open(encrypted_key_path, 'wb') as f:
        f.write(encrypted_key)

    return encrypted_file_path, encrypted_key_path

def upload_to_s3(file_path, key_name):
    s3 = boto3.client('s3', region_name=REGION_NAME)
    s3.upload_file(file_path, AWS_BUCKET_NAME, key_name)
    print(f"✅ Uploaded {key_name} to S3.")

if __name__ == "__main__":
    file_to_encrypt = input("Enter path to file to encrypt & upload: ").strip()
    encrypted_file, encrypted_key = encrypt_file(file_to_encrypt)

    # Upload both to S3
    upload_to_s3(encrypted_file, os.path.basename(encrypted_file))
    upload_to_s3(encrypted_key, os.path.basename(encrypted_key))

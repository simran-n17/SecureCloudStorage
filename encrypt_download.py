import boto3
import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from config import AWS_BUCKET_NAME, REGION_NAME, PRIVATE_KEY_PATH

def download_from_s3(s3_key, download_path):
    s3 = boto3.client('s3', region_name=REGION_NAME)
    s3.download_file(AWS_BUCKET_NAME, s3_key, download_path)
    print(f"✅ Downloaded {s3_key} from S3.")

def decrypt_file(encrypted_file_path, encrypted_key_path):
    # Load private key
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # Decrypt AES key
    with open(encrypted_key_path, 'rb') as f:
        encrypted_key = f.read()

    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Read encrypted file
    with open(encrypted_file_path, 'rb') as f:
        iv_ciphertext = f.read()
        iv = iv_ciphertext[:16]
        ciphertext = iv_ciphertext[16:]

    # Decrypt file
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_path = f"uploads/decrypted_{os.path.basename(encrypted_file_path).replace('encrypted_', '')}"
    with open(decrypted_path, 'wb') as f:
        f.write(plaintext)

    print(f"✅ Decrypted file saved as: {decrypted_path}")

if __name__ == "__main__":
    encrypted_file_s3 = input("Enter the name of the encrypted file on S3: ").strip()
    encrypted_key_s3 = input("Enter the name of the encrypted AES key on S3: ").strip()

    os.makedirs("uploads", exist_ok=True)

    enc_file_path = f"uploads/{encrypted_file_s3}"
    enc_key_path = f"uploads/{encrypted_key_s3}"

    download_from_s3(encrypted_file_s3, enc_file_path)
    download_from_s3(encrypted_key_s3, enc_key_path)

    decrypt_file(enc_file_path, enc_key_path)

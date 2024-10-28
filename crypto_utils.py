from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class CryptoWallet:
    def __init__(self):
        self.balance = 0

    def mine(self, amount):
        self.balance += amount
        print(f"Mined {amount} coins. New balance: {self.balance}")

class EncryptionManager:
    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def encrypt_message(self, message, recipient_public_key):
        return recipient_public_key.encrypt(
            message.encode(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

    def decrypt_message(self, encrypted_message):
        return self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        ).decode()

    def get_public_key(self):
        return self.public_key

from cryptography.fernet import Fernet
from config import config


class EncryptionManager:
    def __init__(self, encryption_key: str):
        self.encryption_key = encryption_key.encode()
        self.cipher_suite = Fernet(self.encryption_key)

    def encrypt(self, data: str) -> bytes:
        """
        Encrypts a string and returns the encrypted data as bytes.

        :param data: String to encrypt
        :return: Encrypted data as bytes
        """
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data: bytes) -> str:
        """
        Decrypts data as bytes and returns the original string.

        :param encrypted_data: Encrypted data as bytes
        :return: Original string
        """
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

    @staticmethod
    def generate_new_key() -> str:
        """
        Generates and returns a new encryption key.

        :return: New encryption key as a string
        """
        new_key = Fernet.generate_key()
        return new_key.decode()


encryption_manager = EncryptionManager(config.encryption.encryption_key)

if __name__ == '__main__':
    print(EncryptionManager.generate_new_key())

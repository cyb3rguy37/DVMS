from cryptography.fernet import Fernet

from app.core.config import settings

fernet = Fernet(settings.encryption_key.encode())

#convert plaintext to ciphertext
def encrypt_value(value: str | None) -> str | None:
    if value is None or value == "":
        return None

    encrypted = fernet.encrypt(value.encode())

    return encrypted.decode()

#convert ciphertext to plaintext
def decrypt_value(ciphertext: str | None) -> str | None:
    if ciphertext is None:
        return None

    if ciphertext == "[DELETED]":
        return None

    decrypted = fernet.decrypt(ciphertext.encode())

    return decrypted.decode()
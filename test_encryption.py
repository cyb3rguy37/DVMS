from app.utils.encryption import encrypt_value, decrypt_value

name = "Gitau"

ciphertext = encrypt_value(name)
plaintext = decrypt_value(ciphertext)

print("Original:", name)
print("Encrypted:", ciphertext)
print("Decrypted:", plaintext)
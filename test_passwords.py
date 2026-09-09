from app.core.security import hash_password, verify_password

password = "KamungePass123!"

hashed = hash_password(password)

print("Original:", password)
print("Hash:", hashed)

print("Correct password:", verify_password("DavidPass123!", hashed))
print("Wrong password:", verify_password("WrongPassword", hashed))
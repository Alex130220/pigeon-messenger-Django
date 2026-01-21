from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt(message: str) -> bytes:
    return cipher.encrypt(message.encode())

def decrypt(token: bytes) -> str:
    return cipher.decrypt(token).decode()
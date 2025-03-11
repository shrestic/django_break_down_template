from argon2 import PasswordHasher

def hash_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)

def verify_password(stored_hash: str, input_password: str) -> bool:
    ph = PasswordHasher()
    try:
        return ph.verify(stored_hash, input_password)
    except:
        return False

# Test
if __name__ == "__main__":
    password = "mypassword123"
    hashed = hash_password(password)
    is_valid = verify_password(hashed, "mypassword123")
    print("Valid!" if is_valid else "Invalid!")
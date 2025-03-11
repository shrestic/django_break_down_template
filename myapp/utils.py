from argon2 import PasswordHasher


def hash_password(password: str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)


# Test cơ bản
if __name__ == "__main__":
    password = "mypassword123"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")

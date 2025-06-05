from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=["bcrypt"], # Use bcrypt for password hashing algorithm
)


def generate_hash_password(password: str) -> str:
    """Generate a hashed password using bcrypt."""
    hash = passwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return passwd_context.verify(plain_password, hashed_password)
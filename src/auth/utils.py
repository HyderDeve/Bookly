from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging

passwd_context = CryptContext(
    schemes=["bcrypt"], # Use bcrypt for password hashing algorithm
)


ACCESS_TOKEN_EXPIRY = 3600 # Default access token expiry time in seconds (1 hour) 

def generate_hash_password(password: str) -> str:
    """Generate a hashed password using bcrypt."""
    hash = passwd_context.hash(password)
    return hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)) #1 hour expiry time by default
    payload['jti'] = str(uuid.uuid4)  # Generate a unique identifier for the token
    payload['refresh'] = refresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET,
        algorithm = Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
            
        token_data = jwt.decode(
            jwt = token,
            key = Config.JWT_SECRET,
            algorithms = Config.JWT_ALGORITHM  
        )

        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

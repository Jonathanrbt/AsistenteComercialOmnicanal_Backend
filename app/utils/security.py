import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

KeySecret = os.getenv('KEY_SECRET', "")
JwtAlgorithm = os.getenv('JWT_ALGORITHM', "HS256")
TokenExpiryMinutes = int(os.getenv('TOKEN_EXPIRY_MINUTES', 60))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def generate_access_token(payload_data: dict) -> str:
    token_data = payload_data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=TokenExpiryMinutes)
    token_data.update({"exp": expiration_time})
    jwt_token = jwt.encode(token_data, KeySecret, algorithm=JwtAlgorithm)
    return jwt_token

def verify_access_token(token: str) -> dict:
    try:
        decoded_payload = jwt.decode(token, KeySecret, algorithms=[JwtAlgorithm])
        return decoded_payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado."
        )

def get_authenticated_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = verify_access_token(token)
    return payload
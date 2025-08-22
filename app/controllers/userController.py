from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from datetime import datetime, timedelta
import uuid

from app.models.userModel import User
from app.schemas.userSchema import UserCreate, UserLogin, Token
from app.utils.security import (
    create_access_token, 
    verify_token, 
    oauth2_scheme,
    verify_password,
    get_password_hash
)
from app.utils.dbConn import get_session

def handle_registration(user_data: UserCreate, session: Session) -> User:
    existing_user = session.exec(
        select(User).where(User.email_address == user_data.email_address)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    new_user = User(
        user_id=str(uuid.uuid4()),
        full_name=user_data.full_name,
        email_address=user_data.email_address,
        channel=user_data.channel,
        hashed_password=get_password_hash(user_data.password)
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

def handle_login(login_data: UserLogin, session: Session):
    user = session.exec(
        select(User).where(User.email_address == login_data["email_address"])
    ).first()
    
    if not user or not verify_password(login_data["password"], user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario desactivado"
        )
    
    user.last_login = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email_address, "user_id": user.user_id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

def get_authenticated_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado."
        )
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )
    
    user = session.exec(
        select(User).where(User.email_address == email)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_authenticated_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user
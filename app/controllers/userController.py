from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from app.models.userModel import User
from app.schemas.userSchema import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password, generate_access_token, verify_access_token, oauth2_scheme
from app.utils.dbConn import get_session

def handle_registration(user_data: UserCreate, session: Session) -> User:
    existing_user = session.exec(select(User).where(User.email_address == user_data.email_address)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado.")
    
    new_user = User(
        full_name=user_data.full_name,
        email_address=user_data.email_address,
        hashed_password=hash_password(user_data.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def handle_login(login_data: UserLogin, session: Session):
    user = session.exec(select(User).where(User.email_address == login_data.email_address)).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas.")

    token_payload = {
        "sub": str(user.id),
        "email": user.email_address
    }
    access_token = generate_access_token(token_payload)
    return {"access_token": access_token, "token_type": "bearer"}

def get_authenticated_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado.")
    
    user_id = int(payload.get("sub"))
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return user
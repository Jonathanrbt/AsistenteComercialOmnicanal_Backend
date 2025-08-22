from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta

from app.schemas.userSchema import UserCreate, UserPublic, Token
from app.controllers.userController import (
    handle_registration, 
    handle_login,
    get_current_active_user
)
from app.utils.dbConn import get_session
from app.models.userModel import User

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserPublic)
def register_new_user(new_user: UserCreate, db_session: Session = Depends(get_session)):
    return handle_registration(new_user, db_session)

@auth_router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_session)
):
    """
    Autentica un usuario y devuelve un token JWT
    """
    return handle_login({
        "email_address": form_data.username,
        "password": form_data.password
    }, db_session)

@auth_router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Obtiene la información del usuario actualmente autenticado
    """
    return current_user

@auth_router.post("/refresh-token", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_active_user)):
    """
    Refresca el token de acceso del usuario
    """
    from app.utils.security import create_access_token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": current_user.email_address, "user_id": current_user.user_id},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
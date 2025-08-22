from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List

from app.schemas.userSchema import UserCreate, UserPublic, Token
from app.controllers.userController import (
    handle_registration, 
    handle_login,
    get_current_active_user,
    get_current_admin_user,
    get_authenticated_user
)
from app.utils.dbConn import get_session
from app.models.userModel import User, UserRole

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserPublic)
def register_new_user(new_user: UserCreate, db_session: Session = Depends(get_session)):
    return handle_registration(new_user, db_session)

@auth_router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_session)
):
    return handle_login({
        "email_address": form_data.username,
        "password": form_data.password,
        "scope": form_data.scopes
    }, db_session)

@auth_router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@auth_router.get("/admin/users", response_model=List[UserPublic])
def get_all_users(
    db_session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    users = db_session.exec(select(User)).all()
    return users

@auth_router.patch("/admin/users/{user_id}/role")
def update_user_role(
    user_id: str,
    new_role: UserRole,
    db_session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    user = db_session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.role = new_role
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return {"message": f"Rol de usuario actualizado a {new_role.value}"}

@auth_router.patch("/admin/users/{user_id}/status")
def toggle_user_status(
    user_id: str,
    db_session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user)
):
    user = db_session.exec(select(User).where(User.user_id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.is_active = not user.is_active
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    status_msg = "activado" if user.is_active else "desactivado"
    return {"message": f"Usuario {status_msg} correctamente"}
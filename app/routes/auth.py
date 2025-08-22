from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.userSchema import UserCreate, UserLogin, UserPublic
from app.controllers.userController import handle_registration, handle_login
from app.utils.dbConn import get_session

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserPublic)
def register_new_user(new_user: UserCreate, db_session: Session = Depends(get_session)):
    return handle_registration(new_user, db_session)

@auth_router.post("/login")
def authenticate_user(credentials: UserLogin, db_session: Session = Depends(get_session)):
    return handle_login(credentials, db_session)
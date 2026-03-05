from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import hash_password
from app.schemas.token import Token
from app.services.auth_service import hash_password, verify_password
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordBearer
from app.core.security import oauth2_scheme, verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        password_hash=hashed_pw,
        role="owner"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme)):

    username = verify_token(token)

    return username

@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):

    return {
        "username": current_user
    }
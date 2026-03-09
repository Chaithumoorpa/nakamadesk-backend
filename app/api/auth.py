import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, oauth2_scheme, verify_token
from app.db.deps import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import hash_password, verify_password

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)

    new_user = User(username=user.username, password_hash=hashed_pw, role="owner")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        logger.warning(f"Authentication failure: user '{form_data.username}' not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password_hash):
        logger.warning(
            f"Authentication failure: invalid password for user '{form_data.username}'"
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):

    username = verify_token(token)

    return username


@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):

    return {"username": current_user}

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.core.security import decode_access_token
from app.schemas.auth import (
    SignupRequest, SignupResponse,
    LoginRequest, LoginResponse,
    RefreshRequest
)
from app.services.auth_service import (
    signup_user, login_user,
    refresh_access_token, logout_user
)


authrouter = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency
def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    
    # 1. Decode the token -> get email
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    # 2. Fetch user from DB
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # 3. Check active status
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    return user

# Signup
@authrouter.post("/signup", response_model=SignupResponse, status_code=201)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    return signup_user(data, db)

# Login
@authrouter.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(data, db)

# Refresh
@authrouter.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return refresh_access_token(data.refresh_token, db)

# Logout
@authrouter.post("/logout")
def logout(current_user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    return logout_user(current_user, db)

# Me
@authrouter.get("/me", response_model=SignupResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Just add this one dependency → route is locked 🔒
@authrouter.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):
    return {"msg": f"Welcome {current_user.email}"}
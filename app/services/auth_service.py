from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.models import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.security import (
    hash_password, verify_password, 
    create_access_token, create_refresh_token,
    decode_access_token)


# Sign Up
def signup_user(data: SignupRequest, db: Session) -> User:
    
    # 1. Check if email already exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Hash the password
    hashed = hash_password(data.password)

    # 3. Create user object
    new_user = User(email=data.email, hashed_password=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Log In
def login_user(data: LoginRequest, db: Session) -> dict:

    # 1. Find user by email
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # 2. Verify password
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    access_token = create_access_token(data={"sub":user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    user.refresh_token = refresh_token
    db.commit()

    return {"access_token":access_token, "refresh_token": refresh_token, "token_type":"bearer"}

# Refresh Access Token
def refresh_access_token(refresh_token: str, db: Session) -> dict:

    # 1. Decode refresh token -> get email
    email = decode_access_token(refresh_token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # 2. Find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # 3. Check refresh token matches DB
    if user.refresh_token != refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token mismatch"
        )
    
    # 4. Issue new access token
    new_access_token = create_access_token(data={"sub":user.email})

    return {
        "access_token" : new_access_token,
        "token_type" : "bearer"
    }

# Logout
def logout_user(current_user: User, db: Session) -> dict:
    current_user.refresh_token = None
    return {"message":"Logged out successfully"}
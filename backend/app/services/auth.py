from app.models.user import User, UserCreate
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock user database
users_db = {}

async def create_user(user_data: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    if user_data.email in users_db:
        raise ValueError("Email already registered")
    
    # Hash password
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create user
    user = User(
        id=str(len(users_db) + 1),
        email=user_data.email,
        name=user_data.name
    )
    
    # Store user in mock database
    users_db[user_data.email] = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "hashed_password": hashed_password
    }
    
    return user

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user"""
    # Check if user exists
    if email not in users_db:
        return None
    
    # Get user from mock database
    user_data = users_db[email]
    
    # Verify password
    if not pwd_context.verify(password, user_data["hashed_password"]):
        return None
    
    # Return user
    return User(
        id=user_data["id"],
        email=user_data["email"],
        name=user_data["name"]
    )

def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
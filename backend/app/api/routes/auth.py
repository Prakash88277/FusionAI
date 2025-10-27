from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User, UserCreate, UserLogin
from app.services.auth import create_user, authenticate_user, create_access_token

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_data: UserCreate):
    """
    Register a new user
    """
    try:
        user = await create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin):
    """
    Authenticate a user and return a JWT token
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
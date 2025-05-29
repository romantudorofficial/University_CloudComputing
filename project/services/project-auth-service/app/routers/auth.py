from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from app.core.security import create_access_token, create_refresh_token



# Create a router for authentication endpoints.
router = APIRouter(prefix = "/auth", tags = ["auth"])



@router.post("/signup", response_model = schemas.UserOut)

def signup (user_in: schemas.UserCreate, db: Session = Depends(get_db)):

    '''
        Sign up a new user.
        Input:
            - user_in: The user data to create a new user
        Output:
            - The created user data
    '''

    # Check if the username or email already exists.
    if crud.get_user_by_username (db, user_in.username):
        raise HTTPException(status_code = 400, detail = "Username already taken")
    
    # Check if the email is already registered.
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code = 400, detail = "Email already registered")
    
    # Create the user in the database.
    user = crud.create_user(db, user_in)
    
    # Return the created user data.
    return user



@router.post("/login", response_model = schemas.Token)

def login (form_data: schemas.UserCreate, db: Session = Depends(get_db)):

    '''
        Log in a user and return access and refresh tokens.
        Input:
            - form_data: The user credentials (username and password)
        Output:
            - A dictionary containing the access token, refresh token, and token type
    '''

    # Authenticate the user using the provided username and password.
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    
    # If the user is not found or the password is incorrect, raise an HTTP exception.
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    
    # Create access and refresh tokens for the authenticated user.
    access_token = create_access_token(subject = user.username, roles = ["OWNER" if user.is_owner else "SIMPLE_USER"])
    refresh_token = create_refresh_token(subject = user.username)
    
    # Return the tokens in a dictionary.
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
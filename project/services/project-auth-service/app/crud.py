from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash, verify_password



def get_user_by_username (db: Session, username: str):

    '''
        Retrieve a user by their username.
        Input:
            - db: The database session
            - username: The username of the user to retrieve
        Output:
            - The user object if found, otherwise None
    '''

    # Check if the user exists in the database by username.
    return db.query(models.User).filter(models.User.username == username).first()



def get_user_by_email (db: Session, email: str):

    '''
        Retrieve a user by their email.
        Input:
            - db: The database session
            - email: The email of the user to retrieve
        Output:
            - The user object if found, otherwise None
    '''

    # Check if the user exists in the database by email.
    return db.query(models.User).filter(models.User.email == email).first()



def create_user (db: Session, user: schemas.UserCreate):

    '''
        Create a new user in the database.
        Input:
            - db: The database session
            - user: The user data to create
        Output:
            - The created user object
    '''

    # Check if the username or email already exists.
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(username = user.username, email = user.email, hashed_password = hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Commit the changes to the database and refresh the user object.
    return db_user



def authenticate_user (db: Session, username: str, password: str):

    '''
        Authenticate a user by username and password.
        Input:
            - db: The database session
            - username: The username of the user to authenticate
            - password: The password of the user to authenticate
        Output:
            - The user object if authentication is successful, otherwise False
    '''

    # Retrieve the user by username.
    user = get_user_by_username(db, username)

    # If the user does not exist or the password is incorrect, return False.
    if not user:
        return False
    
    # Verify the provided password against the stored hashed password.
    if not verify_password(password, user.hashed_password):
        return False
    
    # If the user exists and the password is correct, return the user object.
    return user
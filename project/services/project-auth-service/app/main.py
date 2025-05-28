from fastapi import FastAPI
from app.routers import auth, users
from app.database import engine, Base

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication Service")
app.include_router(auth.router)
# app.include_router(users.router)  # endpoints to manage users
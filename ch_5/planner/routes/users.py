from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from models.users import User, UserSingIn


user_router = APIRouter(tags=["users"])

users: dict[EmailStr, User] ={} 

@user_router.post("/signup")
async def sign_new_user( newUser: User ) -> dict:
    if newUser.email in users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    users[newUser.email] = newUser
    return {"message": "User successfully created"}


@user_router.post("/signin")
async def sign_user_in( user: UserSingIn ) -> dict:
    if user.email not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if users[user.email].password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")

    return {"message": "User successfully logged in"}



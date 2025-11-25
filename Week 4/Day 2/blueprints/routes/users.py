from fastapi import APIRouter


user = APIRouter()


@user.get("/users/", tags=["user"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@user.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "FAKEusername"}


@user.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

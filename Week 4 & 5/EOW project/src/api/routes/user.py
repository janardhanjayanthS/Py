from fastapi import APIRouter


user = APIRouter()



@user.get('/user')
async def get_user():
    return {'user': 'working properly'}

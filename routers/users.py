from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"message": "Not found"}})
# entidad tipo users
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_fake_db = [
    User(id=1, name="brais", surname="Moured", url="https://braismoured.com", age=30),
    User(id=2, name="brais", surname="Moured", url="https://braismoured.com", age=30),
    User(id=3, name="brais", surname="Moured", url="https://braismoured.com", age=30),
]


@router.get("/users")
async def users():
    return users_fake_db


@router.get("/user/{id}/")
async def user(id: int):
    return search_user(id)


@router.get("/user")
async def user(id: int):
    return search_user(id)


@router.post("/user", response_model=User,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe")
    
    users_fake_db.append(user)
    return user

@router.put("/user")
async def user(user: User):
    
    found = False
    
    for index,saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True
            
    if not found:
        return {"error": "User not actualized"}
    
    return user

@router.delete("/user/{id}")
async def user(id: int):
    
    found = False
    
    for index,saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True
        
    if not found:
        return {"error": "User not delete"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_fake_db)
    try:
        return list(users)[0]
    except IndexError:
        return {"error": "User not found"}

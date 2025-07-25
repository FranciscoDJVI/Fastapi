from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemes.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Not found"}})

users_fake_db = []


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())



@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/")
async def user(id: int):
    return search_user("_id",ObjectId(id))


@router.post("/", response_model=User,status_code=201)
async def user(user: User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]  
    
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return User(**new_user)

@router.put("/")
async def user(user: User):
    
    found = False
    
    for index,saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True
            
    if not found:
        return {"error": "User not actualized"}
    
    return user

@router.delete("/{id}")
async def user(id: int):
    
    found = False
    
    for index,saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True
        
    if not found:
        return {"error": "User not delete"}


def search_user(field: str, key):
    
    try:
        user = db_client.local.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "User not found"}

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

# Instancia de OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="Login")

# Entidad usuario que viajara a travex de la red.
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Usuario que se va a crear en la base de datos
class UserBD(User):
    password: str


# diccionario de usuarios
users_db ={
    "mouredev":{
        "username": "mouredev",
        "full_name": "Brais Moured",
        "email": "mouredev@example.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moured 2",
        "email": "mouredev2@example.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserBD(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidad",
            headers={"wwww-Authenticate": "Bearer"})
        
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo",
            )
        
    return user

@router.post("/Login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario incorrecto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña es incorrecta")
    
    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
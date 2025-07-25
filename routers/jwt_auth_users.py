from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Algoritmo de hasheo
ALGORITHM ="HS256"
ACCESS_TOKEN_DURATION = 1
# Opessl
SECRET = "843fd3a6a20eb7b20f5f5ce2e1891bdf99279e64de23d6a6aef0715c43caf2a6"

router = APIRouter()

# Instancia de OAuth2PasswordBearer
oauth2 = OAuth2PasswordBearer(tokenUrl="Login")

# Contexto de encrptacion
crypt = CryptContext(schemes=["bcrypt"])


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
        # bcrypt online
        "password": "$2a$12$VJcE49F2rpq96hMUWWFTpO8bg5.jaJ7qWEz2gp0wyWMEbZFxKnQbe"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moured 2",
        "email": "mouredev2@example.com",
        "disabled": True,
        "password": "$2a$12$JUmAjJaXMBXJND4LRiXTnOVSjNzvb.13NARa8ny2e11OyZZdw.xzO"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserBD(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticacion invalidad",
            headers={"wwww-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
            
    except JWTError:
        raise exception

    return search_user(username)
        
        
# Criterio de dependencia
async def current_user(user: User = Depends(auth_user)):  
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
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña es incorrecta")
    
    
    access_token = {
        "sub":user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM, ), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
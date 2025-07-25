from pydantic import BaseModel

# entidad tipo users
class User(BaseModel):
    id: str | None 
    username: str
    email: str
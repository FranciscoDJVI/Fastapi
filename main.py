from fastapi import FastAPI
from routers import products, basic_auth_users, jwt_auth_users, users, users_db

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.include_router(jwt_auth_users.router)



@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}
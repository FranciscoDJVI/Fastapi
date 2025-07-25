from fastapi import APIRouter

router = APIRouter(prefix="/products",
                   tags=["products"], 
                   responses={404:{"message":"No encontrado"}})


list_products = [
    "product1", 
    "product2", 
    "product3", 
    "product4", 
    "product5"]

@router.get("/")
async def products():
    return ["product1", "product2", "product3", "product4", "product5"]

@router.get("/{id}")
async def products(id: int):
    return  list_products[id]

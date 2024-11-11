from itertools import product
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate, response
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.schema.product import Product, ProductCreate, ProductPatch, ProductUpdate

from app.api.deps import get_db
from app import crud

# Create an APIRouter Instance
router = APIRouter()

# Define a route to create a new Product
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],product_in: ProductCreate):
    # Use the CRUD (Create, Read, Update, Delete)
    # to create a new product or return an existing one if it already exists
    product, createed = await crud.product.get_or_create(
        db=db, defaults=product_in.dict()
    )
    if not createed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product Exists'
        )
    # Return the created or existing product
    return Product
@router.get("/{productId}", response_model=Product, status_code=HTTP_200_OK)
async def get_product(
        db:Annotated[AsyncSession, Depends(get_db)],
        productId: str):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id = productId)
    if not product:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Product not found')
    return product
# Define a route to retrieve a paginated list of Products
@router.get('/', response_model=Page[Product], status_code=status.HTTP_200_OK)
async def get_products(db:Annotated[AsyncSession, Depends(get_db)], skip: int=0, limit:int=20):
    products = await crud.product.get_multi(db=db, skip=skip, limit=limit)
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
    return paginate(products)
# Define a route to partially update the Product
@router.patch("/{productId}", status_code=status.HTTP_200_OK)
async def patch_product(db: Annotated[AsyncSession, Depends(get_db)], product_Id: str, product_in: ProductPatch):
    # Use the CRUD operations to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=product_Id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    product_patched = await crud.product.patch(db=db, obj_id=product_Id, obj_in=product_in.dict())
    return product_patched
# Define a route to fully update a product
@router.put("/{productId}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(db: Annotated[AsyncSession, Depends(get_db)],productId: str, product_in: ProductUpdate):
    proudct = await crud.product.get(db=db, obj_id=productId)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product Not found. ')
    # Use the CRUD operation to fully update the product
    product_updated = await crud.product.update(db=db, obj_current=product, obj_new=product_in)
    return product_updated
# Define a route to delete a product
@router.delete("/{productId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(db: Annotated[AsyncSession, Depends(get_db)], productId:str):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=productId)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Product not found.")
    await crud.product.remove(db=db, obj_id=productId)
    return




